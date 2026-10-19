# Verification report

## Presentation-only update — 2026-10-18

Baseline: `edbb5ce0a4889f9807c75f1b068ec1495d61b3a4`, retained in Git history.

| Component | Status | Evidence |
|---|---|---|
| Notebook schema and metadata | PASS | 25 notebook cells; eight executable code cells; valid notebook schema |
| Scientific implementation unchanged | PASS | All eight Python ASTs identical to baseline; seven code cells byte-identical; sole code-source addition is a non-executable Colab title comment |
| Clean environment installation | PASS | New Python environment with no inherited scientific packages; notebook installed all five scientific dependencies; pip cache disabled |
| Fresh automatic downloads | PASS | Empty working directory; dataset and checkpoint downloaded from unchanged frozen URLs |
| SHA-256 checks | PASS | Both unchanged expected checksums verified |
| Step 1: architecture/forward pass | PASS | 7→256→128→48→1; five inputs return shape (5,1) |
| Step 2: strict loading | PASS | All eight parameter tensors checked and loaded strictly |
| Step 3: freezing/optimizer | PASS | 34,944 frozen; 6,241 trainable; optimizer contains only head parameters |
| Step 4: training | PASS | 50 epochs; frozen shared tensors unchanged; all four head tensors updated; final loss, parameters and predictions finite |
| Step 5: evaluation | PASS | RF, scratch DNN and TL train/test probabilities; AUC, balanced accuracy and MCC independently recalculated |
| Numerical reproducibility | PASS | All 300 probabilities match baseline exactly; maximum absolute difference 0.0; tolerance 1e-6 |
| Figure exports | PASS | Six PNGs (4800×2700) and six parseable SVGs; ROC points/AUC and bar values agree with calculated metrics |
| Existing source/figures/results | PASS | No changes to src/, figures/, results/, data/, requirements, URLs or checksums |
| Slide-code alignment | PASS | Teaching code cells are now 11, 14, 17, 20 and 23; stable cell IDs retained |
| Actual Google Colab execution | NOT TESTED | Browser is signed out; authenticated runtime unavailable |
| Default collapsed helper display in Colab | PASS | Published notebook opened in Google Colab; helper cell displayed its title and Show code buttons with the source hidden, without manually hiding it |

**Execution scope:** eight notebook code cells ran sequentially from beginning to end in a fresh Windows 11 local environment. A ninth, verification-only cell checked final epoch/loss/parameters; it is not part of the published notebook. No scientific package was installed before notebook execution. The notebook's own installation cell ran, with package caching disabled and no cached dataset/checkpoint available. No manual file upload or Drive mount was used.

**Tested versions:** Python 3.13.3; PyTorch 2.13.0; NumPy 2.4.6; pandas 2.3.3; scikit-learn 1.9.0; matplotlib 3.11.1. Harness: nbformat 5.11.1, nbclient 0.11.0, ipykernel 7.4.0. CPU, deterministic algorithms, seed 42. Live Colab numerical execution remains unverified; local execution is not represented as a Google runtime test.

**Recalculated AUCs:** RF training 0.998730 / test 0.800000; scratch training 0.942857 / test 0.773333; TL training 0.895238 / test 0.866667. These values were calculated from probabilities and compared to the published CSV, not hard-coded into analysis. Balanced accuracy and MCC also agree. No collapsed classifications or constant probabilities occurred.

**Browser presentation check:** The public Colab page rendered both Part 0 and Part 1, all three setup subsections, and the supporting-functions form in hidden-code mode. This verifies the actual Colab presentation, not execution on a Google runtime.

**Warnings:** Jupyter emitted a local TCP transport warning and a kernel parent-exit shutdown warning. Neither caused a cell error. No execution failures or unresolved numerical discrepancies occurred in this update. Google sign-in is required for a live Colab runtime and local notebook upload, so those were not attempted past the sign-in prompt. Default hiding in other notebook viewers is not guaranteed.

The scientific limitations remain unchanged: source–target descriptor incompatibility, unresolved target-label semantics, historical pre-split normalization, observation-level study/particle overlap, and limited independent-study generalizability. No source model pretraining was performed.

---

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
