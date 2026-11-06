# Executive Brief: Voice of India Speaker Diarization Benchmark
**Author:** Sakshi Sonker (Josh Talks Growth Assessment)  
**One-Page Summary for Engineering & Product Leadership**  
*Read Time: ~2 Minutes*

---

### The Problem & Benchmark Mission
Speaker diarization answers **"who spoke when"** in conversational audio. While major foundation models advertise single-digit error rates on clean benchmark datasets like LibriSpeech or AMI, deployed speech AI applications in India degrade catastrophically due to high cross-talk (15–30% overlap), code-switching (Hinglish/Tanglish), dynamic ambient noise, and diverse Indian regional accents. 

Josh Talks and Voice of India established this benchmark to provide an independent, reproducible comparison of 10 industry diarization systems across 60 hours of unreleased, held-out conversational audio.

---

### Core Setup at a Glance

| Component | Standard / Specification |
|---|---|
| **Audio Dataset** | 60 hours, 240 sessions across 4 domains: in-person meetings, virtual calls, contact center telephony, and field interviews. |
| **Acoustic Standardization** | Single-channel 16 kHz WAV, peak-normalized to -1 dBFS, EBU R128 (-23 LUFS). Identical audio fed to all models. |
| **Reference Ground Truth** | Multi-track close-microphone recordings segment-tagged in ELAN by primary annotators; verified by a senior phonetician ($\kappa > 0.92$). |
| **Systems Evaluated (10)** | Open-source (pyannote 3.1, NVIDIA NeMo MSDD, SpeechBrain, Kaldi/VBx), integrated commercial ASRs (Deepgram Nova-3, Google Cloud Speech v2, AWS Transcribe, Azure Speech, AssemblyAI, Rev.ai). |
| **Primary Metric** | **Diarization Error Rate (DER)** = $\frac{\text{Miss} + \text{False Alarm} + \text{Confusion}}{\text{Reference Duration}}$ with **0.25s collar**, overlapping speech scored, blind speaker count. |

---

### 3 Core Architectural Design Choices

1. **Mandatory Overlap Scoring (No "Easy" Mode):**  
   Many vendor evaluations omit overlapping segments, masking where 60–80% of attribution errors originate. We strictly score overlapping speech. Models that collapse on simultaneous speaker turns are accurately penalized.

2. **Zero Oracle Knowledge (Autonomous Cluster Discovery):**  
   Real callers and meeting participants do not announce headcounts. Systems are evaluated blind ($k \in [1, 10]$). Providing the oracle speaker count artificially inflates performance by 15–35% and does not reflect production realities.

3. **Multi-Track Isolated Human Reference:**  
   Single-microphone human annotations introduce up to 10% subjective error on overlapping turns. We recorded participants on synchronized, dedicated lapel mics, creating an indisputable acoustic ground truth.

---

### Headline Leaderboard Results & Key Takeaways

```
Rank  Model                           DER (%)   Overlap DER  Miss (%)  Conf (%)   Cost/Hr   RTF
─────────────────────────────────────────────────────────────────────────────────────────────
1     pyannote/speaker-diarization-3.1 14.2%       24.8%       4.8%      7.3%     $0.08    0.04
2     NVIDIA NeMo MSDD FastConformer   15.1%       26.1%       5.2%      7.0%     $0.12    0.06
3     Azure Conversation Transcription 17.8%       31.4%       7.1%      8.9%     $1.20    0.15
4     Google Cloud Speech-to-Text v2   19.4%       34.2%       6.5%      9.5%     $1.44    0.20
5     AssemblyAI Universal-2           21.3%       38.9%       9.8%      9.3%     $0.90    0.18
6     Deepgram Nova-3                  67.1% (!)   84.3%      59.4% (!)  6.5%     $0.31    0.02
─────────────────────────────────────────────────────────────────────────────────────────────
```

### The Executive Takeaway
1. **Open-Source Self-Hosted Models Lead in Raw Diarization Quality:** `pyannote 3.1` and `NVIDIA NeMo MSDD` significantly outperform managed commercial APIs on multi-speaker overlap separation at a fraction of the per-hour inference cost.
2. **The Deepgram Nova-3 Anomaly:** Nova-3 exhibits an anomalous 67.1% DER driven almost exclusively by a **59.4% Missed Speech rate**, resulting from an aggressive energy-based VAD truncating low-amplitude interjections and conversational backchannels.
3. **Selection Rule:** For asynchronous batch meetings where quality is paramount, deploy self-hosted `pyannote 3.1` or `Azure`. For high-throughput contact center telephony where latency and cost matter most, evaluate `Google Speech v2` or `AssemblyAI`.

