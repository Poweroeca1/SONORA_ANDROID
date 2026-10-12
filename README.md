# SONORA AI Studio — Android project starter

SONORA is a native Android app concept combining:
- Music generation prompt composer (AI provider hook point)
- Image/video lyric clip editor
- Multi-image scene timeline
- 5-minute maximum export configuration
- Local media import and project save

## Important honest limitation
This repository is an Android Studio source project, not a compiled APK. No Android SDK/Gradle build toolchain is present in the creation environment, so a real APK could not be compiled and verified here. The generation buttons show provider setup placeholders; no Suno or Renderforest API is secretly included. Suno and Renderforest services are proprietary. Free/open source models can be self-hosted, but MusicGen's weights are CC-BY-NC 4.0 and not approved for commercial use without considering its terms; AnimateDiff needs a suitable computer/GPU and model-specific licenses.

## Build APK
Open this project with Android Studio, allow Gradle sync, then Build > Build APK(s). The GitHub Actions workflow also defines an Android build if placed in a repository.

## Model plan
- MusicGen: local/self-host music generation service prototype; check model license before use.
- AnimateDiff / Stable Video Diffusion: optional self-host image-to-video service; needs GPU resources.
- FFmpeg: final clip muxing and hard cap at 300 seconds.

The app itself can remain free/open source; hosted generation has ongoing compute costs, so genuinely unlimited cloud generation cannot be promised for free.
