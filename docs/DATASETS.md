# Public dataset acquisition guidance

**Do not commit raw patient data, tokens, controlled-access datasets or large binary files.** Check each dataset's access terms and licensing.

| Domain | Data portal | Acquisition guidance |
|---|---|---|
| Lung cancer genomics + transcriptomics | [NCI GDC](https://portal.gdc.cancer.gov/) | Projects TCGA-LUAD and TCGA-LUSC; filter workflow and sample types; export manifest; obtain open-access data where permitted; document access constraints |
| Cancer multi-omics exploration | [UCSC Xena](https://xenabrowser.net/datapages/) | Review dataset units, normalization and identifiers before combining cohorts |
| Groundwater / hydrology | [India-WRIS](https://indiawris.gov.in/) | Check data access, date, sampling quality and coverage |
| Terrain data | [USGS EarthExplorer](https://earthexplorer.usgs.gov/) | DEM and remote-sensing inputs, spatial resolution and licensing |
| Chemistry | [MoleculeNet](https://moleculenet.org/) and [ChEMBL](https://www.ebi.ac.uk/chembl/) | Endpoint metadata, units, duplicates, and scaffold splitting |
| Blood cell images | [NIH NLM](https://www.nlm.nih.gov/) and peer-reviewed dataset links | Ensure image licenses, ground-truth provenance and patient-level splitting |

## TCGA minimum checklist

1. Define LUAD and LUSC cohorts, primary tumor inclusion rules and target question.
2. Use one agreed expression workflow; distinguish **raw counts** from normalized measures (TPM/FPKM).
3. Resolve TCGA case/sample/barcode keys across modalities; define handling of repeat aliquots.
4. Exclude variables derived from target labels, duplicate patients, and post-outcome information.
5. Use patient-level split before learned feature selection, scaling and imputation.
6. Account for tissue composition, batch, purity, sequencing protocol, and class prevalence.
7. Freeze a separate validation cohort; report metrics and confidence intervals.
8. Track GDC portal query, manifest hashes, pipeline version, extraction date, and access classification.

**Warning:** This repository does not include an automated GDC harmonization pipeline; the real-data work is a research task, not a plug-and-play download.
