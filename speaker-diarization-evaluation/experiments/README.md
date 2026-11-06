# Experiments

This folder contains one-off experiments, analysis notebooks, and exploratory scripts.

## Structure

```
experiments/
├── README.md           ← This file
├── exp_001/            ← One folder per experiment
│   ├── README.md       ← Hypothesis, setup, findings
│   ├── run.py          ← Experiment script
│   └── results/        ← Output CSVs, charts
└── ...
```

## How to Add an Experiment

1. Create a numbered folder: `experiments/exp_NNN/`
2. Write a `README.md` with:
   - **Hypothesis** — what you're testing
   - **Setup** — models, recordings, settings used
   - **Results** — DER table, charts
   - **Findings** — interpretation
3. Run the experiment from the project root:
   ```bash
   python experiments/exp_NNN/run.py
   ```
4. Save all outputs to `experiments/exp_NNN/results/`

## Completed Experiments

| ID | Hypothesis | Status |
|----|-----------|--------|
| (none yet) | — | — |

> Experiments are exploratory and do not replace the official leaderboard benchmark.

