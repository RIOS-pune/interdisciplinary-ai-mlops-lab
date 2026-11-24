# Cancer subtype classification: LUAD versus LUSC

### G1: Genomics and mutation intelligence
**Domain work:** define somatic variants, CNV, recurrent genes, and cohort inclusion. **AI work:** encode mutation burden, per-gene binary calls, CNV summaries; audit sparsity and patient matching. **Outputs:** QC report and genomics features; no automatic claim that selected genes are clinically actionable.

### G2: Transcriptomics
**Domain work:** interpret RNA-seq units, gene identifiers, biological effects. **AI work:** construct patient-level expression matrix, normalization/EDA, logistic regression and random forest baselines, cross validation and feature stability. **Outputs:** baseline vs tuned metrics, exploratory gene ranking. The included synthetic demo loosely represents this group's coding workflow, not real transcriptomics.

### G3: Multi-omics fusion
**Domain work:** confirm whether specimens and molecular modalities correspond. **AI work:** patient-matched feature concatenation or late-fusion ensemble with fair unimodal baselines, ablation analysis and missing-modality sensitivity. **Outputs:** same-split modality comparison.

### G4: Biological interpretation & reproducibility
**Domain work:** literature-supported interpretation and pathway hypotheses. **AI work:** bootstrap rank stability, SHAP/permutation feature analysis with caveats, leakage review, documentation. **Outputs:** research-ready interpretation and model card.

## Starting the teaching example
See the main README commands; the artificial genes are named `GENE_A...GENE_F`. They are **fictional** and must not be presented as real biomarkers.

## Real data integration
Start at [GDC](https://portal.gdc.cancer.gov/) with TCGA-LUAD and TCGA-LUSC and follow `docs/DATASETS.md`. Replace the teaching CSV only after completing patient-level sample matching, gene-ID harmonization, and preprocessing validation. `lab/train.py` intentionally rejects repeated `patient_id` values: a group-aware split is required before allowing repeat samples.
