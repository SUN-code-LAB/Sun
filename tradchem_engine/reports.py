"""
Report generators and quality audit logs for Trad-Chem-LLM.
"""
import csv
import json
from pathlib import Path
from typing import Any, Dict, List
from tradchem_engine.models import BatchItemResult, InputRow

SUMMARY_HEADERS = [
    "input_no", "input_name", "normalized_name", "supplied_smiles", "canonical_smiles",
    "pubchem_cid", "identity_status", "candidates_found", "experimental_targets",
    "literature_targets", "predicted_targets", "exported_targets", "evidence_quality",
    "missing_fields", "chemical_folder", "checker_status", "validation_status", "warning_or_error"
]


def write_batch_summary_csv(results: List[BatchItemResult], output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(SUMMARY_HEADERS)
        for r in results:
            writer.writerow([
                r.input_no,
                r.input_name,
                r.normalized_name,
                r.supplied_smiles,
                r.canonical_smiles,
                r.pubchem_cid,
                r.identity_status,
                r.candidates_found,
                r.experimental_targets,
                r.literature_targets,
                r.predicted_targets,
                r.exported_targets,
                r.evidence_quality,
                "; ".join(r.missing_fields),
                r.chemical_folder,
                r.checker_status,
                r.validation_status,
                r.warning_or_error
            ])


def write_input_quality_report(input_rows: List[InputRow], output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    headers = [
        "raw_no", "raw_name", "raw_smiles", "is_valid_smiles", "is_mixture", "is_salt",
        "has_ambiguous_stereochemistry", "doubled_backslash_found", "mojibake_proposals",
        "warnings", "errors"
    ]
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in input_rows:
            writer.writerow([
                row.raw_no,
                row.raw_name,
                row.raw_smiles,
                "YES" if row.is_valid_smiles else "NO",
                "YES" if row.is_mixture else "NO",
                "YES" if row.is_salt else "NO",
                "YES" if row.has_ambiguous_stereochemistry else "NO",
                "YES" if row.doubled_backslash_found else "NO",
                json.dumps(row.mojibake_proposals),
                "; ".join(row.warnings),
                "; ".join(row.errors)
            ])


def write_source_audit_json(results: List[BatchItemResult], output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    audit = {}
    for r in results:
        t_list = []
        if r.record:
            for t in r.record.targets:
                t_list.append({
                    "rank": t.rank,
                    "uniprot_id": t.uniprot_id,
                    "protein_name": t.protein_name,
                    "evidence_tier": t.evidence_tier,
                    "evidence_category": t.evidence_category,
                    "method": t.method,
                    "score": t.score,
                    "source_ref": t.source_ref,
                    "best_structure": t.best_structure,
                    "other_structures": t.other_structures
                })
        audit[r.input_no] = {
            "chemical_name": r.normalized_name,
            "smiles": r.canonical_smiles,
            "pubchem_cid": r.pubchem_cid,
            "targets": t_list,
            "warnings": r.warning_or_error
        }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)


def write_unresolved_chemicals_csv(results: List[BatchItemResult], output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    unresolved = [r for r in results if r.checker_status in ("REVIEW_REQUIRED", "INCOMPLETE", "FAILED")]
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["input_no", "input_name", "supplied_smiles", "status", "reasons"])
        for u in unresolved:
            writer.writerow([u.input_no, u.input_name, u.supplied_smiles, u.checker_status, u.warning_or_error])


def write_validation_results_json(results: List[BatchItemResult], output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    val_data = []
    for r in results:
        val_data.append({
            "input_no": r.input_no,
            "chemical_name": r.normalized_name,
            "folder": r.chemical_folder,
            "identity_status": r.identity_status,
            "checker_status": r.checker_status,
            "validation_status": r.validation_status,
            "exported_targets": r.exported_targets,
            "warnings_or_errors": r.warning_or_error
        })
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(val_data, f, indent=2)


def write_run_configuration_json(config: Dict[str, Any], output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
