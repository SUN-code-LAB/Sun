# Trad-Chem-LLM Google Colab Batch Generator (Version 5)

A fast, robust, and repository-compatible computational engine and Google Colab notebook for batch researching chemicals and generating Trad-Chem-LLM contribution datasets.

---

## 1. Architecture Overview
1. **Input Pipeline (`tradchem_engine/csv_loader.py`)**:
   - Parses UTF-8-SIG input CSVs (default `compound list updates1.csv` with columns `No`, `Compound Name`, `PubChem SMILES`).
   - Retains raw values, audits mojibake (e.g. `Î±`, `Î³`) and doubled backslashes, validates SMILES with RDKit, and detects salts, mixtures, and stereochemical ambiguities.
2. **Deterministic Context Slugs**:
   - Sanitizes formulation, sub-component, and chemical names into lowercase hyphenated slugs (`^[a-z0-9]+(-[a-z0-9]+)*$`).
3. **Multi-API Scientific Research Layer (`tradchem_engine/apis/`)**:
   - Queries PubChem PUG REST, ChEMBL, UniProt KB, RCSB PDB, AlphaFold DB, PubMed, and Europe PMC.
   - Built-in SQLite persistent cache, per-service token-bucket rate limiters, and exponential backoff.
4. **Reproducible Evidence Tiering (`tradchem_engine/researcher.py`)**:
   - Tier 1: Direct experimental binding assay (Ki, Kd, IC50).
   - Tier 2: Target-specific functional/biochemical assay.
   - Tier 3: Verified peer-reviewed target relationship (rejects bare literature co-mentions).
   - Tier 4: Authentic computational prediction (SwissTargetPrediction, NetInfer, TrackMyPDB).
   - Tier 5: Docking-only (only when genuinely computed).
   - Deduplicates targets by UniProt ID and ranks up to Top 10 defensible targets.
5. **Canonical Single Record Exporters (`tradchem_engine/exporters.py`)**:
   - Generates identical `<chemical>.csv`, `<chemical>.json`, and `<chemical>.py` (with safe AST literals and repository `slot(...)` signatures), plus an empty `__init__.py`.
6. **Submission Checker Bridge (`tradchem_engine/checker.py`)**:
   - Runs repository submission check (`contributions/check_submission.py`) without `--import`.
   - Distinct statuses: `PASS` (repository checker passed), `STANDALONE_VALID` (offline check passed), `REVIEW_REQUIRED`, `INCOMPLETE`, `FAILED`.
7. **Packaging & Auditing (`tradchem_engine/packaging.py`, `tradchem_engine/reports.py`)**:
   - Enforces 4 files per chemical folder inside `tradchem/data/<system>/formulations/<formulation>/<sub-component>/<chemical>/`.
   - Generates seven comprehensive reports in `reports/`:
     - `batch_summary.csv`
     - `source_audit.json`
     - `validation_results.json`
     - `unresolved_chemicals.csv`
     - `input_quality_report.csv`
     - `run_configuration.json`
     - `test_report.json`

---

## 2. Google Colab Notebook Usage
1. Open Google Colab and upload `tradchem_batch_generator.ipynb`.
2. Run **Step 1: One-Click Environment Setup** to install dependencies (`rdkit`, `requests`), unpack the embedded `tradchem_engine`, and clone the official repository.
3. Configure optional run parameters in **Step 2** (target organism, taxon ID, maximum targets, traditional medicine context defaults).
4. Run **Step 3: Upload Input CSV & Process Batch**:
   - Upload your chemical list CSV (e.g. `compound list updates1.csv`).
   - The notebook automatically processes all compounds, verifies chemistry, runs the submission checker, and downloads the final `tradchem_contributions.zip` bundle.

---

## 3. Offline Deterministic Test Suite
Run the test suite using `pytest`:
```bash
PYTHONPATH=. pytest tests/ -v
```
All 18 deterministic unit and integration tests verify:
- UTF-8 BOM, quoted names with commas, whitespace trimming.
- Mojibake character proposals without silent identity change.
- Doubled-backslash handling and syntax auditing.
- Salt and mixture detection via RDKit heavy atom counts.
- PubChem CID cross-checking and structure-name conflict resolution.
- Best structure selection (PDB resolution vs. AlphaFold model).
- Evidence tiering and Top 10 target ranking.
- Format agreement across CSV, JSON, and Python outputs.
- Subprocess checker invocation without `--import`.
- ZIP packaging structure and file isolation.
