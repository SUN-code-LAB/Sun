"""
Single canonical record exporters for Trad-Chem-LLM.
"""
import ast
import csv
import io
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
from tradchem_engine.models import ChemicalRecord, TargetProtein

CHEM_FIELDS = [
    "medicine", "system", "plant", "plant_type", "part_used", "family", "common_name",
    "chemical_name", "smiles", "pubchem_cid", "diseases"
]

TARGET_FIELDS = [
    "uniprot_id", "protein_name", "protein_acronym", "species", "taxon_id", "cell_types",
    "best_structure", "other_structures", "go_terms", "protein_diseases", "method", "score",
    "source_ref"
]

LIST_FIELDS = {"diseases", "cell_types", "other_structures", "go_terms", "protein_diseases"}


def _serialize_cell(field: str, val: any) -> str:
    if val is None:
        return ""
    if field in LIST_FIELDS:
        if isinstance(val, (list, tuple)):
            return "; ".join(str(v).strip() for v in val if str(v).strip())
        return str(val).strip()
    return str(val).strip()


def export_csv(record: ChemicalRecord) -> str:
    headers = list(CHEM_FIELDS) + ["rank"] + list(TARGET_FIELDS)
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(headers)

    chem_dict = record.to_chemical_dict()

    if not record.targets:
        row = [_serialize_cell(f, chem_dict.get(f)) for f in CHEM_FIELDS] + ["1"] + ["" for _ in TARGET_FIELDS]
        writer.writerow(row)
    else:
        for target in record.targets:
            t_dict = target.to_slot_dict()
            row = [_serialize_cell(f, chem_dict.get(f)) for f in CHEM_FIELDS]
            row.append(str(target.rank))
            for f in TARGET_FIELDS:
                row.append(_serialize_cell(f, t_dict.get(f)))
            writer.writerow(row)

    return output.getvalue()


def export_json(record: ChemicalRecord) -> str:
    data = record.to_chemical_dict()
    targets_data = []
    for t in record.targets:
        td = t.to_slot_dict()
        targets_data.append(td)
    data["targets"] = targets_data
    return json.dumps(data, indent=2, ensure_ascii=False)


def export_py(record: ChemicalRecord) -> str:
    chem_data = record.to_chemical_dict()

    slots_code = []
    for t in record.targets:
        td = t.to_slot_dict()
        kwargs = []
        for k in TARGET_FIELDS:
            v = td.get(k)
            kwargs.append(f"{k}={v!r}")
        slots_code.append(f"    slot({', '.join(kwargs)}),")

    slots_str = "\n".join(slots_code)

    py_code = f"""#!/usr/bin/env python3
\"\"\"
Trad-Chem-LLM submission record for {record.chemical_name}.
Canonical chemical definition and ranked target proteins.
\"\"\"
import sqlite3
import sys
from pathlib import Path

# import_data.py lives in <repo>/contributions/
sys.path.insert(0, str(Path(__file__).resolve().parents[7] / "contributions"))
try:
    from import_data import import_record, DB_DEFAULT
except ImportError:
    pass

# ------------------------------------------------------------------ the chemical
CHEMICAL = {chem_data!r}


# ------------------------------------------------------------------ one protein slot
def slot(uniprot_id="", protein_name="", protein_acronym="", species="", taxon_id="",
         cell_types=(), best_structure="", other_structures=(), go_terms=(),
         protein_diseases=(), method="", score="", source_ref=""):
    \"\"\"best_structure / other_structures look like  PDB:5IKR  |  AlphaFold:AF-P35354-F1  |  SWISS-MODEL:xxxx
    go_terms look like  \"GO:0006954 inflammatory response\"
    method: literature / SwissTargetPrediction / NetInfer / TrackMyPDB / docking / assay
    score: affinity or probability\"\"\"
    return dict(uniprot_id=uniprot_id, protein_name=protein_name, protein_acronym=protein_acronym,
                species=species, taxon_id=taxon_id, cell_types=list(cell_types),
                best_structure=best_structure, other_structures=list(other_structures),
                go_terms=list(go_terms), protein_diseases=list(protein_diseases),
                method=method, score=score, source_ref=source_ref)


# ------------------------------------------------------------------ top 10 proteins, best first
TARGETS = [
{slots_str}
]
"""
    return py_code


def write_chemical_folder(base_dir: str, record: ChemicalRecord) -> str:
    rel_path = f"tradchem/data/{record.system_slug}/formulations/{record.formulation_slug}/{record.subcomponent_slug}/{record.chemical_slug}"
    folder = Path(base_dir) / rel_path
    folder.mkdir(parents=True, exist_ok=True)

    data_dir = Path(base_dir) / "tradchem" / "data"
    curr = folder
    while curr >= data_dir:
        init_file = curr / "__init__.py"
        if not init_file.exists():
            init_file.write_text("", encoding="utf-8")
        if curr == data_dir:
            break
        curr = curr.parent

    chem_name = record.chemical_slug
    (folder / f"{chem_name}.csv").write_text(export_csv(record), encoding="utf-8-sig")
    (folder / f"{chem_name}.json").write_text(export_json(record), encoding="utf-8-sig")
    (folder / f"{chem_name}.py").write_text(export_py(record), encoding="utf-8-sig")

    return str(folder)
