# Video Walkthrough Script: Diarization Leaderboard Design
## Duration: 2 minutes 30 seconds (Paced for clarity & impact)
**Speaker:** Evaluation Design Lead  
**Format:** Screen recording with webcam bubble / slides / UI mockup walkthrough

---

### [0:00 - 0:30] Introduction & The Core Problem
**Visual:** Show Title Slide / Leaderboard UI Wireframe with Voice of India branding.  
**Spoken Script:**
> "Hi everyone. Today I'm excited to present the design for the **Voice of India Diarization Benchmark (VoI-DiarBench)**. 
> 
> Speaker diarization answers the question 'who spoke when'. While AI models can look stellar in controlled Western benchmark demos, in conversational Indian environments—where people speak with rapid turn-taking, regional accents, code-switching between Hindi and English, and significant cross-talk—most commercial systems break down. 
> 
> We designed this benchmark to give engineering teams, call centers, and clinical app developers an honest, transparent evaluation of which diarization systems actually work in the real world."

---

### [0:30 - 1:30] The 2 to 3 Design Choices That Matter Most
**Visual:** Cut to the Methodology Diagram showing Test Data and Metric settings.  
**Spoken Script:**
> "In designing this benchmark from scratch, three critical choices set our methodology apart:
> 
> **First: Overlapping speech is 100% scored.** 
> In natural Indian conversations, people talk over each other between 12% and 22% of the time. Traditional benchmarks often exclude overlap or apply generous tolerance collars, giving a false sense of accuracy. We score overlapping speech strictly so systems that drop secondary speakers are held accountable.
> 
> **Second: An acoustically isolated reference pipeline.** 
> You cannot grade an AI if your ground truth is biased or subjective. We record live in-person conversations using individual close-talking lapel mics for each speaker alongside a shared room microphone. This enables acoustic energy ground truth combined with double-blind human verification, achieving an inter-annotator agreement score above 0.94 Cohen's Kappa.
> 
> **Third: Statistical significance and granular slicing.** 
> Rather than publishing a single misleading score, our leaderboard uses 10,000 paired bootstrap iterations to verify that rank differences are statistically significant ($p < 0.01$). Users can filter by 8kHz telephony vs. room mics, speaker counts from 2 to 8, and across Northern, Southern, Eastern, and Western accent clusters."

---

### [1:30 - 2:05] What We Learned From Existing Benchmarks
**Visual:** Show benchmark comparison slide highlighting DIHARD III, VoxConverse, and CHiME-8.  
**Spoken Script:**
> "In our research, we evaluated benchmarks like AMI, VoxConverse, and CHiME-8, but **DIHARD III (Ryant et al.)** influenced our design the most.
> 
> DIHARD demonstrated that clinical, conversational, and telephony audio break standard clustering assumptions made by classic algorithms. They proved that using a 0.25-second collar masks significant turn-boundary errors. From DIHARD, we adopted multi-domain stress testing and dual-collar reporting (both 0.25s standard and 0.0s strict), while adapting it uniquely for Indian multi-speaker linguistic dynamics."

---

### [2:05 - 2:30] The Product Experience & Conclusion
**Visual:** Scroll through the Leaderboard Wireframe table, showing the drill-down panel for Deepgram Nova-3 and pyannote.audio.  
**Spoken Script:**
> "On the product side, clicking any model exposes a full diagnostic drawer—breaking down total DER into Missed Speech, False Alarm, and Speaker Confusion, alongside real-time factor and cost per 1,000 hours.
> 
> With VoI-DiarBench, teams no longer have to guess or rely on marketing claims. They have the hard evidence to build, buy, or fix their speech intelligence stack. Thank you!"

---

### Presenter Notes & Delivery Tips
- **Pacing:** Speak at a steady, confident pace (~130 words per minute).
- **Tone:** Objective, technical, and constructive.
- **Visuals to display:**
  1. Have the UI wireframe (`Question1_Leaderboard_UI_Specification_and_Wireframe.md`) open or rendered in slides.
  2. Display the 1-page executive summary diagram during the middle section.
