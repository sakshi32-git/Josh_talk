# Deliverable: Social Media Announcements (`Sakshi_Sonker_Posts`)
## Voice Arena Diarization-Bench: Deepgram Nova-3 Diagnostic Study
**Author:** Sakshi Sonker (Josh Talks Growth Assessment)  
**Target Accounts:** Official Voice Arena / Josh Talks Handles (X & LinkedIn)

---

## Part 1: X (formerly Twitter) Thread (5 Posts)

### Post 1 (The Hook & Finding)
Why does Deepgram Nova-3 achieve state-of-the-art accuracy in ASR demos, but hit a 67.1% Diarization Error Rate (DER) on Voice Arena's benchmark? 

We investigated 139 real conversational recordings to diagnose the root cause. Here is what we found. 🧵👇 [link]

---

### Post 2 (The Diagnostic: It’s Not Noise or Accents)
First, what went wrong? Over 80% of Nova-3’s error isn't speaker confusion—it's **Missed Speech**.

Surprisingly, it’s not driven by Indian accents, phone codecs, or background noise. On clean, dyadic conversations, Nova-3 performs reliably. 

The catastrophic failures occur in specific conversational dynamics: multi-speaker overlap and rapid turn-taking. [link]

---

### Post 3 (The Architectural Mechanism)
Why does it miss speech? 

Because Nova-3 binds its diarization labels to its ASR word emissions, whenever its acoustic front-end drops short interjections ("mm-hm", "yeah") or low-energy overlapping voices during cross-talk, the entire time segment vanishes from the diarization output. 

No words recognized = zero speaker time assigned. [link]

---

### Post 4 (The Evaluation Context: Strict Scoring)
Is our benchmark too strict? 

Voice Arena scores with 0.0s tolerance collars and counts overlapping speech—reflecting true conversational reality. 

Traditional benchmarks use forgiving 250ms collars and discard overlaps, hiding these voice dropouts. When evaluated strictly, joint ASR-diarizers face unique structural penalties. [link]

---

### Post 5 (Constructive Path Forward)
Our goal isn't to critique; it's to build better speech AI for real human conversation. 

We’ve shared our full data pack, RTTM traces, and recommendations with the Deepgram research team to support decoupling VAD from word emission.

Read the complete diagnostic report & data here: [link]

---

## Part 2: LinkedIn Post (Exact Character Count: 1,180 characters / Under 1,300 limit)

**Headline:** Diagnosing Deepgram Nova-3: What happens when state-of-the-art speech models meet real multi-speaker conversation?

When Voice Arena evaluated Deepgram Nova-3 on our held-out benchmark of 139 conversational recordings, the result raised immediate questions: a 67.1% Diarization Error Rate (DER). 

Rather than stopping at a headline score, our research team conducted a deep-dive investigation across 15 representative sessions to isolate the mechanism driving this outcome.

Key takeaways from our diagnostic report:
• Error Decomposition: Over 80% of Nova-3's DER is driven by Missed Speech, rather than speaker confusion.
• The Structural Cause: In joint ASR-diarization architectures, diarization timestamps depend directly on transcribed words. When rapid conversational overlaps or brief vocal fillers are omitted by the acoustic model, those speech segments disappear entirely from the speaker timeline.
• Benchmark Rigor: Under zero-collar, overlap-scored conditions, these omissions are heavily penalized—highlighting a crucial gap between demo benchmarks and live conversational turn-taking.

We have shared our full analysis with Deepgram to support model refinement. Read the full research note: [link]
