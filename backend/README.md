# SONORA AI Studio — music backend prototype

This is the first real server-side music-generation component. It exposes:
- `GET /health` — service and model status.
- `POST /api/music/generate` — generates a WAV clip from a text prompt.

## Run locally on a suitable computer/server

```bash
cd backend
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open `/docs` on the server to test the API. First generation downloads the model and can take time. A GPU is strongly recommended; CPU-only generation can be very slow and memory-intensive.

## Important limits and licensing

- This prototype limits each generated clip to 30 seconds. It does **not** yet provide 5-minute music generation or automatic continuation.
- The default `facebook/musicgen-small` model is subject to its model-card and CC-BY-NC terms. Check those terms before any commercial use.
- The Android app has not yet been connected to this API. Do not enter a fake URL and assume generation works; configure a reachable HTTPS endpoint and test it end-to-end first.
- Never put private API keys in the Android app or commit them to GitHub.
- A free hosting tier may sleep, limit memory, or lack a GPU. Unlimited free cloud generation cannot be promised.
