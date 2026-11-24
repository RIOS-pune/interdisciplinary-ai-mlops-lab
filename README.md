# Interdisciplinary AI & MLOps Lab

A script-first, step-by-step teaching and research starter for **Computer Science + Domain Science** teams. Inspired by the learning sequence (not copied code) of [StackSimplify's credit card fraud project](https://github.com/stacksimplify/mlops-01-ccfd-project).

> **Research-use only.** Synthetic examples are not real patient data; classifier outputs are **not** medical diagnoses, biomarkers or clinical predictions. Validate all methods on independently sourced, properly labelled real datasets before research claims.

## Learning path

| Section | Domain students | CS/AI students | Output |
|---|---|---|---|
| 00 Research orientation | Question, ethics, terminology | ML workflow | Problem statement |
| 01 Domain fundamentals | Disease / geology / chemistry | Translate to features and labels | Glossary |
| 02 Python setup | Data dictionary | Reproducible environment | Working Python |
| 03 Dataset acquisition | Provenance and biological definitions | Download, schema and integrity | Data manifest |
| 04 Exploratory data analysis | Interpret distributions | Leakage and missingness checks | EDA report |
| 05 Preprocessing | Normalization appropriateness | Fit transforms on training folds | Clean data |
| 06 Feature engineering | Plausible scientific features | Selection with leakage safeguards | Feature specification |
| 07 Baselines & evaluation | Interpret errors | Stratified split, metrics | Baseline report |
| 08 Hyperparameter tuning | Scientific plausibility | Cross validation and tuning | Tuned model |
| 09 Domain interpretation | Scientific interpretation | Feature importance and stability | Research narrative |
| 10 Prediction API | Explain limits | FastAPI + Pydantic | Local API |
| 11 Research collaboration | Scientific review | Reproducibility, CI, issues | Team evidence |
| 12 Final report | Discussion/limitations | Packaging/model card | Deliverables |

## Projects and groups

| Group | Discipline | Project | Data | Target |
|---|---|---|---|---|
| G1 | Biology + CS | Lung cancer mutation/CNV profiling | TCGA GDC mutation & CNV | Feature matrix; driver gene report |
| G2 | Biology + CS | LUAD vs LUSC gene expression | TCGA GDC RNA-seq | Baseline classification and gene ranking |
| G3 | Biology + CS | Multi-omics fusion | G1 + G2 matched TCGA cases | Comparison with expression-only |
| G4 | Biology + CS | Interpretation and validation | G1-G3 outputs | Pathway discussion, leakage audit |
| G5 | Geology + CS | Deccan basalt groundwater potential | Geological Survey / groundwater / satellite data | Spatial validation and map |
| G6 | Chemistry + CS | Molecular property prediction | MoleculeNet/ChEMBL | QSAR baseline and scaffold split |
| G7 | MLT + CS | Blood-cell image screening | Licensed public image datasets | Patient-aware evaluation |

## Quickstart: fully synthetic classroom demonstration

Requires Python 3.10+ (3.11 recommended). From repository root:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m lab.generate_synthetic
python -m lab.train --data data/synthetic/expression_demo.csv --out artifacts
python -m lab.evaluate --data data/synthetic/expression_demo.csv --model artifacts/model.joblib
uvicorn lab.api:app --reload
```

Open http://127.0.0.1:8000/docs and POST to `/predict` with e.g. `{"features": {"GENE_A": 7.1, "GENE_B": 3.2, "GENE_C": 4.0, "GENE_D": 5.0, "GENE_E": 2.2, "GENE_F": 4.4}}`. The API is a classroom demo only.

### Real TCGA data

Start with [NCI Genomic Data Commons](https://portal.gdc.cancer.gov/), selecting TCGA-LUAD and TCGA-LUSC; see [docs/DATASETS.md](docs/DATASETS.md) and [projects/lung-cancer/README.md](projects/lung-cancer/README.md). The repo intentionally **does not download controlled-access files**, auto-pull large cohorts, or pretend synthetic features represent actual cancer biomarkers.

To use actual expression matrices: build one row per participant; create `sample_id`, label `LUAD` or `LUSC`, and numeric expression features. Keep a sealed external cohort for truly independent validation. Never include labels or identifiers among predictors. Select normalization compatible with counts/TPM and study design, document batch effects, and ensure all learned transforms are fit within training folds only.

### Testing

```bash
pytest -q
```

## Suggested grading

- Domain question, terminology and provenance: 20%
- Data quality, cleaning and leakage control: 20%
- Baselines, validation and fair metrics: 25%
- Scientific interpretation and limitations: 20%
- Reproducibility, README and demo: 15%

## Publication to GitHub

```bash
git init
git add .
git commit -m "Initial interdisciplinary AI MLOps teaching repository"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/interdisciplinary-ai-mlops-lab.git
git push -u origin main
```

Create an empty GitHub repository first, then substitute your user/organization. No GitHub repository is created automatically by this ZIP.

## License and attribution

Original educational starter code, MIT licensed. Structural inspiration: StackSimplify's MLOps learning project (linked above). No third-party source code or proprietary datasets included.
