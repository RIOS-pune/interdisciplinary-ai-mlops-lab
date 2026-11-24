# Reproducible research method

## Research sequence
Problem definition → cohort inclusion → consent/access rules → sample mapping → data QC → split → preprocessing within folds → baseline → tuned model → independent testing → interpretation → literature review → limitations.

## Preventing leakage
- Perform patient-level partition before fitting imputation, scaling, differential expression/feature selection, PCA, or gene-ranking transforms.
- In cross-validation, put all learned transforms inside pipelines and re-fit on each training fold.
- Never treat multiple specimens from one person as independent training/test examples.
- Check batch/site/hospital confounding; evaluate external generalization where feasible.
- Predeclare target label and thresholds; report balanced accuracy, macro F1, per-class recall, confusion matrix and AUROC when appropriate.

## Interpretation
Correlation/importance is not biological causation. Differential expression is not the same as classifier feature importance. Use pathway resources, multiplicity correction and independent biological literature checks. Do not present a prototype classifier as a clinical diagnostic tool.

## Multi-omics
Use participant-matched samples; account for missing modalities; compare expression-only, mutation-only, CNV-only and fused models on **identical patient test partitions**. Assess ablation and batch effects.
