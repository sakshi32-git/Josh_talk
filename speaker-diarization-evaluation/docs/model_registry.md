# Model Registry

All models evaluated on the Speaker Diarization Evaluation Platform.

| # | Model Name | Provider | Version | Type | Run Method | Notes |
|---|-----------|----------|---------|------|-----------|-------|
| 1 | `pyannote/speaker-diarization-3.1` | pyannote.audio (HuggingFace) | 3.1 | Open Source | Local Python pipeline | Requires HuggingFace token; uses ECAPA-TDNN + VBx clustering |
| 2 | `NeMo MSDD` | NVIDIA | 1.21+ | Open Source | Local (`nemo_toolkit`) | Multi-Scale Diarization Decoder; state-of-the-art on CHiME-6 |
| 3 | `SpeechBrain ECAPA-TDNN` | SpeechBrain | 1.0 | Open Source | Local (`speechbrain`) | Speaker embedding + agglomerative clustering |
| 4 | `Amazon Transcribe` | Amazon Web Services | v2 (2024) | Commercial API | REST API (`boto3`) | Returns `speaker_label` per word; must reconstruct RTTM |
| 5 | `Google Speech-to-Text v2` | Google Cloud | v2 | Commercial API | REST API (`google-cloud-speech`) | Speaker diarization config: `enable_speaker_diarization=True` |
| 6 | `Azure Speaker Diarization` | Microsoft | Speech SDK 1.37 | Commercial API | REST API (`azure-cognitiveservices-speech`) | Conversation transcription API; supports ≤ 8 speakers |
| 7 | `AssemblyAI` | AssemblyAI | v2 | Commercial API | REST API (HTTP + polling) | `speaker_labels=True`; async polling model |
| 8 | `Rev.ai` | Rev.ai | v1 | Commercial API | REST API (`rev_ai` SDK) | Speaker diarization in human-parity transcription product |
| 9 | `Kaldi/VBx` | Brno Univ. of Technology | 2023 | Open Source | Docker container / CLI | VBx (Variational Bayes x-vectors); DIHARD III top system |
| 10 | `Whisper + pyannote` | OpenAI + pyannote.audio | whisper-large-v3 + pyannote 3.1 | Open Source | Local (two-stage pipeline) | ASR with word timestamps; align to pyannote diarization output |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| ✅ Integrated | Adapter implemented and tested |
| 🔧 In Progress | Adapter under development |
| 📋 Planned | Listed; not yet implemented |
| ❌ Blocked | Cannot integrate (licensing / unavailability) |

> Verify exact API versions and availability before finalizing the report. API versioning for commercial providers changes frequently.

