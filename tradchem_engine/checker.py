"""
Repository submission checker wrapper for Trad-Chem-LLM.
"""
import ast
import csv
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from tradchem_engine.exporters import CHEM_FIELDS, TARGET_FIELDS, LIST_FIELDS

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
UNIPROT_RE = re.compile(r"^([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})$")
STRUCTURE_RE = re.compile(r"^(PDB:[0-9][A-Za-z0-9]{3}|AlphaFold:AF-[A-Z0-9]+-F[0-9]+|SWISS-MODEL:\S+)$")
GO_RE = re.compile(r"^GO:[0-9]{7}(\s|$)")


def check_submission_locally(folder_path: str) -> Tuple[int, List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    folder = Path(folder_path)

    if not folder.is_dir():
        return 1, [f"Directory {folder} does not exist"], []

    chem_name = folder.name
    if not NAME_RE.match(chem_name):
        errors.append(f"Folder name '{chem_name}' must be lower-case words joined by '-'")

    init_path = folder / "__init__.py"
    if not init_path.is_file():
        errors.append(f"missing __init__.py in {folder}")

    files = {
        "csv": folder / f"{chem_name}.csv",
        "json": folder / f"{chem_name}.json",
        "py": folder / f"{chem_name}.py"
    }

    for ext, fpath in files.items():
        if not fpath.is_file():
            errors.append(f"missing .{ext} file (every contribution needs CSV + JSON + Python)")

    if errors:
        return 1, errors, warnings

    csv_rows = []
    with open(files["csv"], "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            csv_rows.append(r)

    with open(files["json"], "r", encoding="utf-8-sig") as f:
        json_data = json.load(f)

    py_text = files["py"].read_text(encoding="utf-8-sig")
    tree = ast.parse(py_text)
    py_chemical = None
    py_targets = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id == "CHEMICAL":
                py_chemical = ast.literal_eval(node.value)
            elif node.targets[0].id == "TARGETS":
                if isinstance(node.value, ast.List):
                    py_targets = []
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Call):
                            slot_kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in elt.keywords if kw.arg}
                            py_targets.append(slot_kwargs)

    if py_chemical is None or py_targets is None:
        errors.append("Python file must define CHEMICAL and TARGETS safely")
        return 1, errors, warnings

    for field in CHEM_FIELDS:
        j_val = json_data.get(field, "")
        p_val = py_chemical.get(field, "")
        if field in LIST_FIELDS:
            j_set = set(j_val) if isinstance(j_val, list) else set()
            p_set = set(p_val) if isinstance(p_val, list) else set()
            if j_set != p_set:
                errors.append(f"Field '{field}' differs between JSON and Python")
        else:
            if str(j_val).strip() != str(p_val).strip():
                errors.append(f"Field '{field}' differs between JSON and Python ({j_val} vs {p_val})")

    if len(csv_rows) != len(json_data.get("targets", [])):
        errors.append(f"CSV target count ({len(csv_rows)}) differs from JSON ({len(json_data.get('targets', []))})")

    targets = json_data.get("targets", [])
    if not targets:
        errors.append("no chemical->protein hits found: add at least one protein")
    elif len(targets) != 10:
        warnings.append(f"{chem_name} has {len(targets)} protein(s); the project expects the top 10")

    has_go = False
    has_disease = bool(json_data.get("diseases"))
    for rank_idx, t in enumerate(targets, start=1):
        uid = t.get("uniprot_id", "")
        if not uid or not UNIPROT_RE.match(uid):
            errors.append(f"rank {rank_idx}: invalid uniprot_id '{uid}'")
        s_ref = t.get("source_ref", "")
        if not s_ref:
            errors.append(f"rank {rank_idx}: source_ref is empty")
        elif "example" in s_ref.lower():
            errors.append(f"rank {rank_idx}: example source_ref still present")
        if not t.get("best_structure"):
            warnings.append(f"{uid}: no best structure marked")
        elif not STRUCTURE_RE.match(t.get("best_structure")):
            errors.append(f"rank {rank_idx}: invalid best_structure format '{t.get('best_structure')}'")
        if not t.get("method"):
            warnings.append(f"rank {rank_idx}: method is empty")
        if t.get("go_terms"):
            has_go = True
        if t.get("protein_diseases"):
            has_disease = True

    if not has_go:
        warnings.append("no GO terms found")
    if not has_disease:
        warnings.append("no diseases found")

    code = 1 if errors else 0
    return code, errors, warnings


def run_repo_checker(repo_root: str, chemical_folder_path: str) -> Tuple[str, List[str], List[str], str]:
    repo_path = Path(repo_root) if repo_root else Path(".")
    checker_script = repo_path / "contributions" / "check_submission.py"
    target_path = Path(chemical_folder_path)
    try:
        rel_path = target_path.relative_to(repo_path)
    except ValueError:
        rel_path = target_path

    if checker_script.is_file() and (repo_path / "contributions" / "import_data.py").is_file():
        cmd = [sys.executable, str(checker_script), str(rel_path)]
        try:
            res = subprocess.run(cmd, cwd=str(repo_path), capture_output=True, text=True, timeout=30)
            stdout = res.stdout
            stderr = res.stderr
            out_combined = f"{stdout}\n{stderr}"
            errors = [line.replace("ERROR:", "").strip() for line in out_combined.splitlines() if "ERROR:" in line]
            warnings = [line.replace("warning:", "").strip() for line in out_combined.splitlines() if "warning:" in line]
            status = "PASS" if res.returncode == 0 else "FAILED"
            return status, errors, warnings, out_combined
        except Exception as e:
            return "FAILED", [f"Checker execution failed: {e}"], [], str(e)
    else:
        code, errs, warns = check_submission_locally(str(target_path))
        status = "STANDALONE_VALID" if code == 0 else "FAILED"
        return status, errs, warns, "Local standalone verification executed; actual repository checker unavailable."
