# Video Walkthrough Script: Deepgram Nova-3 Failure Diagnosis
## Duration: 2 minutes 45 seconds
**Speaker / Presenter:** Sakshi Sonker  
**Focus:** Explaining the 67.1% DER root cause, evidence from the data pack, and recommendations.

---

### [0:00 - 0:35] The Mystery: Why Did Nova-3 Score 67.1% DER?
**Visual:** Show the Voice Arena Leaderboard and the headline 67.1% DER score, with a side-by-side comparison to peer systems.  
**Spoken Script:**
> "Hi everyone. When Voice Arena evaluated Deepgram Nova-3 on our held-out benchmark of 139 conversational recordings, the result shocked the community: a 67.1% Diarization Error Rate, placing it far behind other leading systems.
> 
> Nova-3 is widely celebrated as one of the fastest, most accurate transcription models in the world. So how could it fail so severely on speaker diarization? 
> 
> We conducted a forensic diagnosis across 15 benchmark recordings, running deep comparative analysis, playground tests, and acoustic correlation checks. Here is what we found."

---

### [0:35 - 1:20] What Actually Goes Wrong: The Anatomy of Missed Speech
**Visual:** Show `deepgram_error_decomposition_chart.png` showing the red bars (Missed Speech) dominating the error.  
**Spoken Script:**
> "The first key finding is in the error decomposition. Nova-3’s error is **not** caused by speaker confusion. Its Speaker Confusion rate is only 6.6%, and its False Alarm rate is under 5%. Nova-3 knows *who* is speaking when it detects speech.
> 
> Instead, **over 80% of its error is pure Missed Speech**.
> 
> In our 15 analyzed sessions, the data splits into two dramatic clusters:
> - On clean, two-person interviews with low overlap—like `REC_01_GOOD`—Nova-3 scores an impressive 12.4% DER.
> - But as soon as we move to boardroom discussions and panels with 4 to 6 speakers and conversational overlap above 15%—like `REC_06_POOR` and `REC_10_POOR`—the DER rockets past 70%, with speech coverage dropping as low as 35%."

---

### [1:20 - 1:55] What We Ruled Out vs. The True Root Cause
**Visual:** Show `deepgram_overlap_vs_der_chart.png` highlighting the +0.979 correlation between overlap % and DER, and contrast with the near-zero SNR correlation.  
**Spoken Script:**
> "We tested and ruled out three common assumptions:
> - First, **background noise**: The correlation between Signal-to-Noise Ratio and DER is basically zero ($r = -0.007$). Noisy phone calls did fine, while pristine studio panels with cross-talk failed.
> - Second, **accents**: High DER occurred equally across US, European, and Indian speakers.
> - Third, **audio clipping or formatting**: Audio quality checks showed zero digital clipping.
> 
> **So what is the root cause?**
> Nova-3 is a joint ASR-diarization engine. It binds speaker timestamps directly to transcribed words. In natural conversations, people interrupt with short interjections ('uh-huh', 'haan', 'correct') or talk simultaneously. Nova-3's acoustic decoder suppresses the secondary overlapping speaker to preserve transcript sanity. 
> 
> But because no words are emitted for that secondary speaker, **zero speaker duration is registered**. The model essentially turns simultaneous human speech into silence."

---

### [1:55 - 2:30] The Evaluation Context & Recommendations
**Visual:** Show slide detailing the Voice Arena 0.0s collar setting and recommendations for Deepgram.  
**Spoken Script:**
> "This architectural vulnerability is exacerbated by Voice Arena’s strict benchmark settings: a 0.0-second tolerance collar and full overlap scoring. Legacy benchmarks with 250ms collars and ignored overlap masked this dropout, but strict real-world scoring exposes it.
> 
> **Our recommendations are twofold:**
> For Deepgram: Decouple acoustic VAD and speaker segmentation from lexical word decoding. Emit acoustic speaker turns even when overlapping words cannot be confidently transcribed.
> 
> For Voice Arena: Dual-report both 0.25s standard and 0.0s strict collars, and offer separate sub-leaderboards for dyadic vs. multi-party overlapping audio."

---

### [2:30 - 2:45] Conclusion
**Visual:** Closing slide with links to the full research report, working scripts, and data pack.  
**Spoken Script:**
> "This investigation shows that benchmarking isn't about declaring winners and losers—it's about uncovering the exact boundaries where technology needs to evolve. All our data, scripts, and playground proof runs are linked below. Thank you!"

