# SONORA AI Studio

SONORA is a native Android music and lyric-video studio concept. The plan is to provide:
- Music prompt composer with real server-side generation
- Local audio/image import and saved projects
- Lyric-video timeline with text overlays and scene ordering
- Video export capped at 300 seconds (5 minutes)
- Multilingual interface and dark, premium music-studio visual design

## Current status (honest)

- The original Android project is packaged in `SONORA_Android.zip`.
- A first FastAPI music-backend prototype is now in `backend/`. It exposes `GET /health` and `POST /api/music/generate`, using the Hugging Face Transformers MusicGen model by default.
- **The Android app is not yet connected to the backend.** The API has not yet been deployed or end-to-end tested, and this commit is not proof that generation works on a live server.
- The backend currently generates short clips (up to 30 seconds per request); it does not yet create a complete five-minute song/video.
- A server with enough memory is needed; a GPU is strongly recommended. Free hosting may sleep or lack the resources required.

## Backend prototype

See [backend/README.md](backend/README.md). To run it on a suitable server:

```bash
cd backend
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Check `/health` and `/docs` on the server before connecting the Android app. Do not put API keys in the APK or commit secrets to GitHub.

## Model and licensing

The default model is `facebook/musicgen-small`. Its model-card and CC-BY-NC terms must be reviewed before commercial use. Check the exact license of any model before distributing or monetizing the app. Suno and Renderforest are proprietary services; this project does not include their private APIs.

## Next milestones

1. Verify the backend dependency install and health endpoint on an actual host.
2. Add a configurable HTTPS backend URL to Android and wire the generation screen to the real API.
3. Save generated audio to the device and display it in the song library.
4. Build the lyric-video timeline and export flow, enforcing a 300-second maximum.
5. Test the complete flow on a physical Android device before calling it complete.

The app can be free/open source, but hosted inference has real compute costs. Unlimited cloud generation cannot be promised for free.
