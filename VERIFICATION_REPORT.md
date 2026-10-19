# Verification report

## Colab environment fix — 2026-10-18

Baseline: `e7c4bf559e4162a7d7f9132086a61588224db2e1`. Part 0.1 now validates existing imports and required operations without invoking pip. A version difference from the local pins does not trigger installation. Import/API failures stop with explicit recovery and runtime-restart instructions. The original pinned requirements and reference results are unchanged. Earlier installation claims below describe earlier notebook revisions, not this revision.

### Execution scope and checks

Two local CPU runs executed all eight notebook code cells sequentially in fresh kernels and empty working directories. The reference run used the existing pinned environment; the alternate run used a newly created virtual environment without inherited packages, installed from scratch with pip caching disabled **before** starting its kernel. Both used Python 3.13.3 on Windows 11. Neither run is an execution on Google's Colab service. The alternate stack tests version flexibility; it is not claimed to duplicate Colab's current default stack.

| Package | Reference environment | Fresh alternate environment |
|---|---|---|
| PyTorch | 2.13.0 | 2.7.1 |
| NumPy | 2.4.6 | 2.2.6 |
| pandas | 2.3.3 | 2.2.3 |
| scikit-learn | 1.9.0 | 1.6.1 |
| matplotlib | 3.11.1 | 3.10.3 |

| Requested check | Result in both environments |
|---|---|
| Dependency imports and operations | PASS; installed versions unchanged by execution |
| Dataset download | PASS; new download, unchanged frozen URL and SHA-256; N=100, train=80, test=20 |
| Checkpoint download | PASS; new download, unchanged frozen URL and SHA-256 |
| Strict loading | PASS; all eight checkpoint tensors checked and loaded strictly |
| Frozen layers | PASS; 34,944 frozen / 6,241 trainable; optimizer only contains trainable head parameters |
| Fine-tuning | PASS; 50 epochs; frozen shared tensors bitwise unchanged; all four head tensors updated; finite loss and predictions |
| Evaluation | PASS; AUC, balanced accuracy and MCC independently recalculated from all 300 probabilities |
| Figures | PASS; six decoded 4800×2700 PNGs and six parsed SVGs; ROC coordinates/areas and bar values checked against calculated metrics |
| Failure-path regression tests | PASS; five tests in each environment cover healthy imports, missing package, reported NumPy import error, loaded/installed version mismatch and missing required PyTorch API |
| Notebook schema and scientific preservation | PASS; 25 cells and eight code cells; seven scientific code cells byte-identical to baseline; positions, IDs, helper-collapse metadata, source modules, requirements and existing figures/results unchanged |
| Live Google Colab CPU execution | NOT TESTED; available browser signed out, no authenticated Google runtime |

The new environment also passed `pip check`. Tests use nbformat 5.11.1, nbclient 0.11.0 and ipykernel 7.4.0. An additional verification-only cell checked epoch count, finiteness and frozen/head tensors; it is not included in the published notebook.

### Numerical comparison and investigation

| Model | Reference test AUC | Alternate test AUC | Maximum absolute probability difference, train / test |
|---|---|---|---|
| Random Forest | 0.800000 | 0.800000 | 0 / 0 |
| Scratch DNN | 0.773333 | 0.786667 | 0.0782160 / 0.0814255 |
| Transfer Learning | 0.866667 | 0.866667 | 1.19209e-7 / 5.96046e-8 |

The reference environment reproduced all 300 saved probabilities exactly. The alternate environment did **not** reproduce exact scratch probabilities: scratch training AUC also changed from 0.942857 to 0.940952. All models' classifications, balanced accuracy and MCC remained unchanged on both partitions. Mean absolute scratch probability differences were 0.00991365 (train) and 0.01349865 (test). These are measured results, not values substituted into the analysis.

A diagnostic replay using the unchanged reusable model/training functions compared the two environments. Preprocessed arrays, labels, splits, initial parameter tensors, all 50 epoch batch orders and initial forward predictions matched exactly. The first optimizer update produced a maximum parameter difference of 3.72529e-9. Final scratch loss was 0.371316 versus 0.368471 and maximum final parameter difference was 0.204467; replayed probability differences matched the notebook runs. This localizes the divergence to numerical training behavior with different PyTorch builds, rather than sampling, initialization or evaluation changes. It does not identify a particular backend kernel as the cause. Deterministic settings within an environment do not establish bitwise equality across versions. No method, seed, hyperparameter or dependency was tuned to recover the reference AUC. The 20-observation test set contains 75 positive-negative pairs; the AUC change of 0.013333 equals one pair's contribution.

The published historical CSVs and figures remain intact. Future compatible Colab versions may yield different probabilities or metrics; successful imports are not a guarantee of exact numerical reproduction. Use the original local pins for the reference environment. No source-model pretraining was performed.

**Audit notes:** An initial local harness typo failed before notebook execution and was corrected in a separate harness file. Both completed notebook runs had no cell failures. Local Jupyter TCP/shutdown warnings and matplotlib/pyparsing deprecation warnings did not prevent execution. Private executed notebooks, raw outputs and diagnostic arrays are retained outside the repository; no downloaded dataset or checkpoint is committed. The exact cause of the user's failed Colab installation remains unconfirmed. See [environment setup and recovery](ENVIRONMENT_SETUP.md).

---

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
