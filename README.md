# SOT 2027 CE: Transfer Learning for Toxicity Prediction

## Addressing Data Scarcity in Environmental Risk Assessment

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/choulab210/SOT-2027-CE-Course/blob/main/MNP_Transfer_Learning_Colab.ipynb)

**Initialize Network → Load Pretrained Weights → Freeze Shared Layers → Fine-Tune → Evaluate ROC-AUC**

A beginner-friendly CPU tutorial based on Chen et al. (2025), *Transfer learning enables robust prediction of cellular toxicity from environmental micro- and nanoplastics*, *Journal of Hazardous Materials* 496, 139353. [Paper](https://doi.org/10.1016/j.jhazmat.2025.139353) · [Original research repository](https://github.com/choulab210/Micro-Nanoplastics).

## Run in Google Colab

1. Click **Open in Colab** above; sign in to Google if prompted.
2. Select **Runtime → Run all**. A CPU runtime is sufficient.
3. Wait for dependency checks, automatic downloads and 50-epoch fine-tuning.
4. Examine the four conceptual figures and calculated ROC-AUC results.

No Google Drive mount, manual upload, paid GPU, or clone is required. Supporting functions are embedded in the notebook (the long setup cell is collapsed); the five teaching sections remain concise. Every execution creates a new output folder. Dataset and checkpoint downloads use frozen original commit `6f786a275d1598bd5a7e3bb61c125529744e7dc4` and SHA-256 verification. Colab uses its preinstalled scientific environment when imports and required interfaces work. Run all does not pip-install or replace packages. Version differences alone are not errors. If an older notebook changed packages in your session, restart before using this version; see [environment recovery](ENVIRONMENT_SETUP.md).

The source model learned from the nanoparticle dataset. The target is the existing MNP cytotoxicity dataset. We transfer all tensors into the original 7→256→128→48→1 architecture, freeze the first two layers, and adapt the 48-unit hidden head plus one-unit sigmoid output. The source model is never retrained.

## Read the results

N=100 **total observations**, not unique particles: 80 train, 20 test. RF, scratch DNN and TL use the same observations. Scratch and RF are target-only baselines. See [slide/code alignment](SLIDE_CODE_ALIGNMENT.md).

| Model | Training ROC-AUC | Test ROC-AUC |
|---|---:|---:|
| Random Forest | 0.999 | 0.800 |
| Scratch DNN | 0.943 | 0.773 |
| Transfer Learning | 0.895 | 0.867 |

These are the previously verified simplified tutorial results, recalculated during the publication test. The notebook computes its own predictions and metrics; it does not hard-code this table. See [verification](VERIFICATION_REPORT.md) for tested versions and numerical tolerances.

Figure 5 compares training and test AUC; Figure 6 plots the actual held-out ROC curves. Balanced accuracy, MCC, class counts, confusion matrices, constant probabilities and collapsed classifications are also reported. Training performance alone does not establish predictive utility; its gap from test performance alone is not definitive evidence of overfitting.

## Scientific limitations

This is an educational mechanics demonstration, **not independent external validation**. Source/target descriptor meanings differ, `Negative` is encoded as class 1 without verified toxic-positive semantics, historical scaling occurs before splitting, and studies/particles overlap across train and test. Simplified fixed training differs from the published model-selection workflow. Historical N=50/100/200 results are not generated or mixed into this notebook. Read [SCIENTIFIC_NOTES.md](SCIENTIFIC_NOTES.md).

## Local use

Install [requirements.txt](requirements.txt) into a new virtual environment from a terminal before launching Jupyter, then open the notebook and Run All. The pinned file is unchanged and supports the original local reference environment; the notebook only validates imports and required interfaces. Python 3.13.3 was used for the original local publication test. Reusable definitions are in src/. The public notebook is standalone and can be tested from an otherwise empty working folder.

The six figures are provided in PNG and SVG. The results directory contains publication-test predictions/metrics and the previous verified comparison baseline; these are all simplified N=100 results, not historical published-workflow outputs. No pretrained binary, raw dataset, temporary execution folder or virtual environment is committed.

## Licensing

- **MIT** ([LICENSE](LICENSE)): original Python source code, scripts, and Google Colab notebooks.
- **CC BY 4.0** ([LICENSE-CONTENT.md](LICENSE-CONTENT.md)): original standalone educational figures, teaching slides when included, and documentation.
- Original research datasets, pretrained model weights, published figures and third-party materials retain their applicable rights. Neither new license covers them. The original repository has no declared license; no general redistribution permission is inferred from public availability. Dataset/weights are fetched from their original location rather than redistributed here. See [THIRD_PARTY_PROVENANCE.md](THIRD_PARTY_PROVENANCE.md).

## Citation and attribution

Please cite Chen et al. (2025), *Journal of Hazardous Materials* 496, 139353, https://doi.org/10.1016/j.jhazmat.2025.139353, and acknowledge the [Micro-Nanoplastics repository](https://github.com/choulab210/Micro-Nanoplastics). For these educational materials, acknowledge Wei-Chun Chou and SOT 2027 CE Course contributors, link to this repository, and identify modifications. Retain applicable license notices.

## Notebook organization

**Part 0. Environment Setup and Data Preparation (Run Once)** groups scientific environment checks (0.1), supporting functions (0.2), and verified dataset download/preparation (0.3). Run it before the teaching steps; it does not pretrain the nanoparticle source model. The dataset output shows total/train/test counts and class distributions.

**Part 1. Hands-On Transfer Learning Tutorial** contains the five slide-aligned steps. Code, figures, settings and scientific limitations are preserved. The helper cell requests hidden source through Colab form metadata and a `#@title` comment; use Show code to inspect it. Other notebook viewers may render it differently. See [verification](VERIFICATION_REPORT.md) for the actual browser and execution checks.

Dependency versions can change optimization rounding and, in some cases, predictions. Consult [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md) for measured comparisons; the historical reference CSVs and figures are preserved.
