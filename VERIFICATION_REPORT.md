# Publication verification — 2026-10-18

## Passed

- Notebook schema validation and Python parsing of every code cell.
- Fresh Python 3.13.3 virtual environment, with no inherited site-packages; dependency installation completed and pip check reported no broken requirements.
- Standalone notebook executed all 8 code cells sequentially in an empty working directory, with no repository modules or input files preloaded.
- Fresh public downloads from frozen original commit; dataset and checkpoint SHA-256 verified.
- All eight checkpoint tensors loaded strictly after name, shape, finiteness and seven-input checks.
- 34,944 frozen and 6,241 trainable parameters; only head parameters in the optimizer.
- Shared tensors remained bitwise unchanged; all four head tensors updated.
- Actual RF/scratch/TL predictions and all requested metrics calculated.
- All 300 training/test probabilities match the prior educational tutorial exactly (maximum absolute difference 0.0). Predeclared tolerance: 1e-6 for probabilities and 1e-12 for AUC/balanced accuracy/MCC.
- Six 4800×2700 PNGs at 300 dpi and six SVGs generated; numeric figure inputs are saved alongside the images and validated against prediction-derived metrics before plotting.
- No constant probabilities or collapsed classifications in this run.

## Resolved failures retained in the local audit

The first dependency installation exceeded Windows' path-length limit inside PyTorch; a fresh environment at a shorter path installed successfully. The first fresh notebook execution correctly rejected a CSV checksum mismatch: the original Windows checkout used CRLF and GitHub serves LF. Byte comparison after line-ending normalization and parsed-data comparison confirmed identical data. The publication notebook pins the actual frozen-download SHA-256. The original files were not changed.

## Google Colab boundary

**This is a verified fresh local Colab-compatibility test, not a live Google Colab execution.** The available browser was signed out of Google; no authenticated Google runtime was available. No service-side numerical test is claimed. Python 3.12 Linux wheels were confirmed available for all five pinned scientific packages, but this is not a substitute for a Linux/Google runtime execution.

Tested versions: Python 3.13.3, PyTorch 2.13.0, NumPy 2.4.6, pandas 2.3.3, scikit-learn 1.9.0, matplotlib 3.11.1. Validation tooling: nbformat 5.11.1, nbclient 0.11.0, ipykernel 7.4.0. CPU, one PyTorch thread, deterministic algorithms, seed 42. Supporting scientific dependencies included SciPy 1.18.1 and threadpoolctl 3.7.0.

No source training or hyperparameter search was run. See SCIENTIFIC_NOTES.md for limitations and THIRD_PARTY_PROVENANCE.md for attribution and licensing boundaries. Slide alignment was checked against the supplied five-slide specification; no PowerPoint file was provided.
