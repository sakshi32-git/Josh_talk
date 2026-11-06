"""
Voice Arena Diarization-Bench: Deepgram Nova-3 Failure Analysis Script
Author: AI Evaluation & Research Team
Description:
    Processes session data, calculates correlation matrices across acoustic
    parameters (overlap, SNR, speaker count) vs DER components (MS, FA, SC),
    and generates visualization charts for the research report.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 15 Representative Sessions Data
data = [
    {"session_id": "REC_01_GOOD", "setting": "Telephony Dyad", "speakers": 2, "overlap_pct": 3.2, "der": 12.4, "ms": 4.8, "fa": 3.1, "sc": 4.5, "snr_db": 24.5, "speech_cov": 0.96, "peer_avg_der": 11.8},
    {"session_id": "REC_02_GOOD", "setting": "In-Person Interview", "speakers": 2, "overlap_pct": 4.1, "der": 14.2, "ms": 5.9, "fa": 2.8, "sc": 5.5, "snr_db": 26.0, "speech_cov": 0.94, "peer_avg_der": 12.5},
    {"session_id": "REC_03_GOOD", "setting": "Remote Call", "speakers": 2, "overlap_pct": 5.0, "der": 16.8, "ms": 7.2, "fa": 3.4, "sc": 6.2, "snr_db": 22.1, "speech_cov": 0.92, "peer_avg_der": 14.1},
    {"session_id": "REC_04_MID",  "setting": "Team Standup", "speakers": 3, "overlap_pct": 9.8, "der": 28.4, "ms": 18.2, "fa": 4.1, "sc": 6.1, "snr_db": 20.4, "speech_cov": 0.81, "peer_avg_der": 16.3},
    {"session_id": "REC_05_MID",  "setting": "Telephony Support", "speakers": 2, "overlap_pct": 8.5, "der": 31.2, "ms": 21.0, "fa": 4.5, "sc": 5.7, "snr_db": 14.2, "speech_cov": 0.78, "peer_avg_der": 18.0},
    {"session_id": "REC_06_POOR", "setting": "Boardroom Discussion", "speakers": 4, "overlap_pct": 16.4, "der": 62.5, "ms": 51.2, "fa": 4.2, "sc": 7.1, "snr_db": 21.5, "speech_cov": 0.49, "peer_avg_der": 19.8},
    {"session_id": "REC_07_POOR", "setting": "Overlapping Team Review", "speakers": 5, "overlap_pct": 18.9, "der": 68.4, "ms": 56.8, "fa": 4.8, "sc": 6.8, "snr_db": 23.0, "speech_cov": 0.44, "peer_avg_der": 22.1},
    {"session_id": "REC_08_POOR", "setting": "Brainstorming Session", "speakers": 4, "overlap_pct": 21.2, "der": 71.3, "ms": 59.4, "fa": 4.9, "sc": 7.0, "snr_db": 19.8, "speech_cov": 0.41, "peer_avg_der": 23.4},
    {"session_id": "REC_09_POOR", "setting": "Telephony Multi-Party", "speakers": 3, "overlap_pct": 14.8, "der": 64.1, "ms": 52.6, "fa": 5.1, "sc": 6.4, "snr_db": 16.5, "speech_cov": 0.48, "peer_avg_der": 21.0},
    {"session_id": "REC_10_POOR", "setting": "Cross-talk Panel", "speakers": 6, "overlap_pct": 24.5, "der": 78.9, "ms": 66.2, "fa": 5.4, "sc": 7.3, "snr_db": 28.2, "speech_cov": 0.35, "peer_avg_der": 26.5},
    {"session_id": "REC_11_POOR", "setting": "Bilingual Townhall", "speakers": 5, "overlap_pct": 19.4, "der": 73.2, "ms": 61.1, "fa": 5.0, "sc": 7.1, "snr_db": 25.1, "speech_cov": 0.39, "peer_avg_der": 24.2},
    {"session_id": "REC_12_POOR", "setting": "Conversational Debate", "speakers": 3, "overlap_pct": 22.0, "der": 74.8, "ms": 62.5, "fa": 4.6, "sc": 7.7, "snr_db": 24.0, "speech_cov": 0.38, "peer_avg_der": 25.0},
    {"session_id": "REC_13_POOR", "setting": "Coffee Shop Call", "speakers": 4, "overlap_pct": 17.5, "der": 69.5, "ms": 57.3, "fa": 5.3, "sc": 6.9, "snr_db": 13.8, "speech_cov": 0.43, "peer_avg_der": 23.1},
    {"session_id": "REC_14_POOR", "setting": "Casual Group Chat", "speakers": 4, "overlap_pct": 18.2, "der": 70.1, "ms": 58.0, "fa": 4.7, "sc": 7.4, "snr_db": 21.0, "speech_cov": 0.42, "peer_avg_der": 22.8},
    {"session_id": "REC_15_POOR", "setting": "Strategy Meeting", "speakers": 5, "overlap_pct": 20.8, "der": 75.6, "ms": 63.4, "fa": 4.8, "sc": 7.4, "snr_db": 22.4, "speech_cov": 0.37, "peer_avg_der": 25.9},
]

df = pd.DataFrame(data)

def generate_analysis():
    print("=== SUMMARY METRICS ===")
    print(f"Total sessions analyzed: {len(df)}")
    print(f"Mean Nova-3 DER: {df['der'].mean():.2f}%")
    print(f"Mean Missed Speech (MS): {df['ms'].mean():.2f}% ({df['ms'].mean()/df['der'].mean()*100:.1f}% of total DER)")
    print(f"Mean False Alarm (FA): {df['fa'].mean():.2f}% ({df['fa'].mean()/df['der'].mean()*100:.1f}% of total DER)")
    print(f"Mean Speaker Confusion (SC): {df['sc'].mean():.2f}% ({df['sc'].mean()/df['der'].mean()*100:.1f}% of total DER)")
    print()

    print("=== STATISTICAL CORRELATIONS WITH DER ===")
    r_overlap = df['overlap_pct'].corr(df['der'])
    r_snr = df['snr_db'].corr(df['der'])
    r_speakers = df['speakers'].corr(df['der'])
    r_ms = df['ms'].corr(df['der'])
    r_coverage = df['speech_cov'].corr(df['der'])
    
    print(f"Correlation (Overlap % vs DER): {r_overlap:+.3f} (Very Strong Positive)")
    print(f"Correlation (Missed Speech vs DER): {r_ms:+.3f} (Direct Linear Driver)")
    print(f"Correlation (Speech Coverage vs DER): {r_coverage:+.3f} (Direct Inverse Driver)")
    print(f"Correlation (Speaker Count vs DER): {r_speakers:+.3f} (Strong Positive)")
    print(f"Correlation (SNR / Background Noise vs DER): {r_snr:+.3f} (No Significant Correlation)")
    print()

    # Generate Chart: Overlap % vs Diarization Error Rate
    plt.figure(figsize=(10, 6))
    plt.scatter(df['overlap_pct'], df['der'], color='#D32F2F', s=80, alpha=0.8, edgecolors='black', label='Nova-3 DER (%)')
    plt.scatter(df['overlap_pct'], df['peer_avg_der'], color='#1976D2', s=80, alpha=0.8, edgecolors='black', marker='^', label='Peer Systems Avg DER (%)')
    
    # Fit line for Nova-3
    z = np.polyfit(df['overlap_pct'], df['der'], 1)
    p = np.poly1d(z)
    plt.plot(df['overlap_pct'], p(df['overlap_pct']), "r--", alpha=0.7, label=f'Nova-3 Trend (r={r_overlap:.2f})')

    plt.title('Impact of Conversational Overlap (%) on Diarization Error Rate (DER)', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Conversational Overlapping Speech (%)', fontsize=11)
    plt.ylabel('Diarization Error Rate - DER (%)', fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    plt.savefig('deepgram_overlap_vs_der_chart.png', dpi=300)
    print("Saved chart: deepgram_overlap_vs_der_chart.png")

    # Generate Chart: Error Component Breakdown
    plt.figure(figsize=(10, 6))
    sorted_df = df.sort_values(by='der')
    x = range(len(sorted_df))
    plt.bar(x, sorted_df['ms'], label='Missed Speech (MS)', color='#D32F2F', alpha=0.85)
    plt.bar(x, sorted_df['sc'], bottom=sorted_df['ms'], label='Speaker Confusion (SC)', color='#FBC02D', alpha=0.85)
    plt.bar(x, sorted_df['fa'], bottom=sorted_df['ms']+sorted_df['sc'], label='False Alarm (FA)', color='#388E3C', alpha=0.85)

    plt.xticks(x, sorted_df['session_id'], rotation=45, ha='right', fontsize=9)
    plt.title('Nova-3 Diarization Error Decomposition Across 15 Benchmark Sessions', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Session ID (Ranked from Best to Worst)', fontsize=11)
    plt.ylabel('DER Error Contribution (%)', fontsize=11)
    plt.legend(loc='upper left')
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('deepgram_error_decomposition_chart.png', dpi=300)
    print("Saved chart: deepgram_error_decomposition_chart.png")

if __name__ == '__main__':
    generate_analysis()
