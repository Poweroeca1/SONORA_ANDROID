"""SONORA music-generation API prototype.

The model is loaded only when the first generation request arrives.
This is an initial server-side engine; the Android app still needs to be wired to this API.
"""
import io
import os
import threading
from typing import Literal

import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from scipy.io.wavfile import write as write_wav
from transformers import AutoProcessor, MusicgenForConditionalGeneration

APP_NAME = "SONORA AI Studio API"
MODEL_ID = os.getenv("SONORA_MUSIC_MODEL", "facebook/musicgen-small")
MAX_SECONDS = int(os.getenv("SONORA_MAX_GENERATION_SECONDS", "30"))

app = FastAPI(title=APP_NAME, version="0.1.0")
_model = None
_processor = None
_model_lock = threading.Lock()


class MusicRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=500)
    duration_seconds: int = Field(default=15, ge=1, le=30)
    genre: str = Field(default="pop", max_length=80)
    mood: str = Field(default="energetic", max_length=80)
    instrumental: bool = True


@app.get("/health")
def health():
    return {
        "service": APP_NAME,
        "status": "ok",
        "model": MODEL_ID,
        "model_loaded": _model is not None,
        "max_generation_seconds": min(MAX_SECONDS, 30),
        "device": "cuda" if torch.cuda.is_available() else "cpu",
    }


def get_model():
    global _model, _processor
    if _model is not None and _processor is not None:
        return _processor, _model
    with _model_lock:
        if _model is None:
            try:
                device = "cuda" if torch.cuda.is_available() else "cpu"
                _processor = AutoProcessor.from_pretrained(MODEL_ID)
                _model = MusicgenForConditionalGeneration.from_pretrained(MODEL_ID)
                _model.to(device)
                _model.eval()
            except Exception as exc:
                _processor = None
                _model = None
                raise RuntimeError(f"Could not load model {MODEL_ID}: {exc}") from exc
    return _processor, _model


@app.post("/api/music/generate")
def generate_music(request: MusicRequest):
    seconds = min(request.duration_seconds, MAX_SECONDS, 30)
    if seconds < 1:
        raise HTTPException(status_code=422, detail="duration_seconds must be positive")
    prompt = (
        f"{request.genre} music, {request.mood} mood. "
        f"{request.prompt}. "
        + ("Instrumental, no vocals." if request.instrumental else "Vocals may be included.")
    )
    try:
        processor, model = get_model()
        inputs = processor(text=[prompt], padding=True, return_tensors="pt")
        device = next(model.parameters()).device
        inputs = {key: value.to(device) for key, value in inputs.items()}
        # MusicGen's sampling rate is supplied by the model config.
        sample_rate = int(model.config.audio_encoder.sampling_rate)
        max_new_tokens = max(1, int(seconds * 50))
        with torch.inference_mode():
            audio_values = model.generate(
                **inputs,
                do_sample=True,
                guidance_scale=3,
                max_new_tokens=max_new_tokens,
            )
        audio = audio_values[0, 0].detach().float().cpu().numpy()
        audio = np.clip(audio, -1.0, 1.0)
        pcm = (audio * 32767).astype(np.int16)
        output = io.BytesIO()
        write_wav(output, sample_rate, pcm)
        output.seek(0)
        headers = {
            "Content-Disposition": 'attachment; filename="sonora-generated.wav"',
            "X-SONORA-Model": MODEL_ID,
            "X-SONORA-Duration-Limit": str(seconds),
        }
        return StreamingResponse(output, media_type="audio/wav", headers=headers)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Generation failed: {exc}") from exc
