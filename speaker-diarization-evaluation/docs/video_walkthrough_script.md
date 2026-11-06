# Video Walkthrough Script: Speaker Diarization Benchmark
**Duration:** 2 minutes 45 seconds (Target: 2:30 – 3:00)  
**Deliverable:** Question 1, Deliverable 4 (Compulsory Video Walkthrough)  
**Presenter:** Sakshi Sonker (Josh Talks Growth Assessment)  

---

### Timing & Storyboard Overview

| Timestamp | Visual on Screen | Key Talking Point / Subject |
|---|---|---|
| **0:00 – 0:30** | Title Slide / Live Leaderboard Interface | Problem context: why existing public benchmarks fail in Indian real-world deployment. |
| **0:30 – 1:30** | Architecture Diagram / Methodology Spec | The 2 or 3 design choices that matter most and why (Overlap, Blind $k$, Multi-track ground truth). |
| **1:30 – 2:15** | Benchmark Influences Slide (DIHARD III & CHiME-8) | What we learned from state-of-the-art benchmarks and papers. |
| **2:15 – 2:45** | Live Platform UI (Evaluate Page & Model Inspector) | Working prototype walkthrough & closing summary. |

---

### Detailed Teleprompter Script

#### [0:00 – 0:30] Introduction & The Evaluation Gap
> *"Hello, everyone. Today I'm walking you through our evaluation methodology for the Voice of India Speaker Diarization Benchmark.  
> 
> Speaker diarization answers 'who spoke when'. While modern AI foundation models advertise impressive single-digit word error rates, when deployed in real-world Indian conditions—with heavy cross-talk, code-switching between Hindi and English, noisy conference rooms, and telephone audio—many systems degrade severely.  
> 
> A good benchmark isn't just a single score. It's an objective measurement system that helps engineering teams decide what to build, buy, or fix."*

#### [0:30 – 1:30] The 2 to 3 Design Choices That Matter Most
> *"In designing our 60-hour unreleased benchmark across 10 leading open-source and commercial systems, three foundational design choices define our platform:
> 
> **First: Mandatory Overlapping Speech Scoring.**  
> Many public benchmarks exclude overlapping speech segments to make models look good. In Indian meetings, people talk over each other constantly—overlap accounts for 15 to 25% of audio time. By evaluating overlap with a standardized 0.25-second collar, we measure what users actually experience.
> 
> **Second: Strictly Blind Speaker Counts.**  
> In real call centers and meeting notes, you are never told the ground truth number of speakers in advance. Providing an oracle speaker count inflates scores by up to 30%. Our benchmark requires every model to discover the number of speaker clusters autonomously.
> 
> **Third: Multi-Track Close-Mic Human Ground Truth.**  
> Human annotation on a single mixed room track is prone to subjective error. We recorded speakers on dedicated, acoustically isolated lavalier microphones, yielding a rigorous, double-checked reference with inter-annotator agreement kappa above 0.92."*

#### [1:30 – 2:15] Learnings from Academic Benchmarks (DIHARD III & CHiME-8)
> *"Our design was deeply influenced by two landmark challenges: **DIHARD III** and **CHiME-8 Task 1**.
> 
> From **DIHARD III**, we learned that clean corpora like AMI give teams a false sense of security. DIHARD introduced intentionally difficult audio—casual dinners, clinical interviews, and street audio. It proved that decomposing DER into Missed Speech, False Alarm, and Speaker Confusion is essential to understand *how* models fail.
> 
> From **CHiME-8**, we learned the value of connecting pure diarization with downstream speech-to-text accuracy using metrics like Concatenated Minimum-Permutation Word Error Rate (`cpWER`). Diarization is rarely an end in itself; it powers transcription and meeting notes."*

#### [2:15 – 2:45] Prototype Platform & Conclusion
> *"To prove this methodology, we also built a working end-to-end software platform using FastAPI, pyannote.metrics, and React. Teams can upload hypothesis RTTM files from their models, compute exact DER and JER breakdowns, inspect statistical confidence intervals, and explore the interactive leaderboard.
> 
> With this methodology, companies can stop relying on demo numbers and make data-driven decisions on speech systems. Thank you!"*

---

### Recording Checklist for Presenter
- [ ] Record in 1080p, 16:9 aspect ratio.
- [ ] Keep screen recording active: toggle between `docs/methodology.md`, the architecture diagrams, and the local React frontend at `http://localhost:5173`.
- [ ] Maintain an energetic, confident, executive presentation cadence.
- [ ] Target time: between 2:15 and 2:45 minutes.

