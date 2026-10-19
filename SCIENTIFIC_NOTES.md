# Scientific notes: simplified teaching demonstration

Based on Chen et al. (2025), *Journal of Hazardous Materials* 496, 139353, https://doi.org/10.1016/j.jhazmat.2025.139353 and https://github.com/choulab210/Micro-Nanoplastics, frozen commit `6f786a275d1598bd5a7e3bb61c125529744e7dc4`.

## What is preserved

The checkpoint-compatible DNN is 7→256→128→48→1, with hidden ReLU and sigmoid output. Both shared layers and both head linear layers receive pretrained weights. Only the head is fine-tuned. Source training is never repeated. The tutorial uses CPU and seed 42.

N=100 is total observations, not unique particles or training-only samples. The historical sampling strata are PET/PVC/PP Negative=27, Positive=5, PS/PE Negative=33, Positive=35. The exact polymer concatenation order, independent seed-42 stratum samples, seed-42 shuffle and unstratified seed-42 80/20 split are preserved. The 80 training observations have encoded class counts 0=35, 1=45; the 20 test observations have 0=5, 1=15.

The original notebook references a missing `Xu 2022_micro-nanoplastics dataset.csv`. The supplied `MNP dataset.csv` matches the existing reproduction's counts, sampled rows and outputs, but byte identity with the missing file is not established. The extra MNP dataset is not used. The larger source nanoparticle dataset has 1,500 raw rows and 818 retained under the original filtering; the target CSV has 1,824 observations across 33 reference DOIs. These counts come from the frozen local scientific audit, not a new experimental dataset.

## Source–target feature compatibility

| Position | Source | Target |
|---|---|---|
| 1 | coating indicator | Pristine=0; other=1 |
| 2 | diameter ≥100 nm indicator | Spherical=0; other=1 |
| 3 | log10 concentration (micromolar) | log10 dose (micrograms/mL) |
| 4 | zeta potential | log10 size (nm) |
| 5 | exposure time | hours divided by 24 |
| 6 | Fermi energy | polymer HOMO constant |
| 7 | band gap | polymer LUMO constant |

Parameter shapes match, but physical meanings do not all match. Five polymer orbital pairs are copied from the original notebook; its eV comments lack verified upstream unit/calculation provenance. Each domain uses its own full-data min-max ranges; no saved source scaler accompanies the checkpoint. The target's five continuous features are scaled over all 100 observations BEFORE splitting, so test extrema affect preprocessing. This is deliberately retained historical behavior, not a leakage-free evaluation.

## Label meaning and dependence

Source class 1 is viability <80%; target class 1 is the literal string `Negative` (class 0 is `Positive`). The target file does not provide a verified biological dictionary or equivalent viability threshold. Do not call class 1 definitively toxic. ROC-AUC treats encoded 1 as positive. Classification uses p>0.5. Confusion matrices use rows=true [0,1], columns=predicted [0,1].

The historical 80/20 split shares 10 reference DOIs, 12 particle IDs and 2 distinct feature vectors; these are distinct-value intersections, not row-duplication counts. It is not an independent-study test. Sampled class balance is not population prevalence.

## What is simplified

All three tutorial models fit the same 80 observations. Both DNNs have the same fixed architecture and settings: 50 epochs, batch 22, Adam 0.01, penalty 0.001 × sum of tensor L2 norms, not squared-weight decay. Scratch trains all parameters from random initialization; TL freezes the shared layers. RF uses 100 trees and default sklearn settings otherwise. There is no hyperparameter search, early stopping, or test-based selection.

The published-workflow reproduction selected an inner-fold TL model fitted on 43 rows and an RF fold model fitted on 64 rows at N=100, with extensive search for the baselines. Those procedures are not repeated. Historical N=100 RF/scratch/TL test AUCs were 0.826667/0.853333/0.906667 in the existing executed reproduction, versus the simplified tutorial's 0.800/0.773/0.867. The original saved scratch notebook reported 0.773; equality after rounding is not evidence of identical training. Original dependency versions/execution state were not fully pinned, and historical scratch discrepancies remain unresolved.

Historical N=50/100/200 comparison figures are not included here. No historical data are mixed into the six newly generated tutorial figures.

## Interpreting results

Training AUC alone does not establish predictive utility, and its difference from test AUC is not definitive proof of overfitting. One small split cannot establish general TL superiority. No confidence intervals or significance claims are supplied. The DNN has no dropout; repeated deterministic predictions do not measure epistemic uncertainty, and probability dispersion across observations is not an AUC interval. Historical repeated-fold statistics and RF inter-tree variability are not imported as uncertainty estimates.

AUC, balanced accuracy and MCC are missing/undefined with a single true class. MCC is also undefined for a constant predicted class because its denominator is zero; sklearn's conventional zero is not substituted. Constant probabilities and collapsed classifications are separately flagged.

A fully corrected evaluation would require resolving source/target descriptors and label provenance, likely source-domain retraining, plus appropriate train-only preprocessing and study-grouped evaluation. Those changes are outside this tutorial and were not silently introduced. This is a parameter-transfer demonstration, not external validation.
