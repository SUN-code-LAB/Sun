"""
Input CSV loader and chemical validator for Trad-Chem-LLM.
"""
import csv
import io
import re
import unicodedata
from typing import Dict, List, Optional, Tuple
from rdkit import Chem

from tradchem_engine.models import InputRow


MOJIBAKE_MAP = {
    "Î±": "α",
    "Î²": "β",
    "Î³": "γ",
    "Î´": "δ",
    "Îµ": "ε",
    "Îº": "κ",
    "Î»": "λ",
    "Î¼": "μ",
    "â€’": "‐",
    "â€“": "–",
    "â€”": "—",
    "Â±": "±",
    "â€²": "′",
    "â€³": "″",
    "Â°": "°",
    "Ã©": "é",
    "Ã¨": "è",
}


def slugify(text: str) -> str:
    """Generate a lowercase hyphenated slug complying with naming regex ^[a-z0-9]+(-[a-z0-9]+)*$."""
    if not text:
        return "unnamed"
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "unnamed"


def detect_mojibake(text: str) -> Dict[str, str]:
    """Detect known mojibake character sequences and return a dictionary of proposed fixes."""
    proposals = {}
    if not text:
        return proposals
    for corrupted, corrected in MOJIBAKE_MAP.items():
        if corrupted in text:
            proposals[corrupted] = corrected
    return proposals


def validate_and_canonicalize_smiles(raw_smiles: str) -> Tuple[Optional[str], Optional[str], Optional[Chem.Mol], List[str], List[str], bool, bool, bool]:
    warnings = []
    errors = []
    is_mixture = False
    is_salt = False
    has_ambiguous_stereo = False

    cleaned = raw_smiles.strip()
    if not cleaned:
        errors.append("SMILES string is empty.")
        return None, None, None, warnings, errors, False, False, False

    has_doubled_backslash = "\\\\" in cleaned
    mol = None

    if has_doubled_backslash:
        warnings.append("SMILES contained doubled backslashes ('\\\\'); auditing structure syntax.")
        mol = Chem.MolFromSmiles(cleaned)
        if mol is None:
            cand = cleaned.replace("\\\\", "\\")
            cand_mol = Chem.MolFromSmiles(cand)
            if cand_mol is not None:
                mol = cand_mol
                cleaned = cand
    else:
        mol = Chem.MolFromSmiles(cleaned)

    if mol is None:
        errors.append(f"Invalid SMILES structure: unable to parse with RDKit: {cleaned}")
        return None, None, None, warnings, errors, False, False, False

    frags = Chem.GetMolFrags(mol, asMols=True)
    if len(frags) > 1:
        is_mixture = True
        warnings.append(f"Structure contains {len(frags)} disconnected components (mixture/salt).")
        atom_counts = [f.GetNumHeavyAtoms() for f in frags]
        if min(atom_counts) <= 4:
            is_salt = True
            warnings.append("Component contains small ion/salt counter-ion.")

    chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
    unassigned = [c for c in chiral_centers if c[1] == "?"]
    if unassigned:
        has_ambiguous_stereo = True
        warnings.append(f"Structure has {len(unassigned)} unassigned stereocenter(s).")

    try:
        canonical_smiles = Chem.MolToSmiles(mol, isomericSmiles=True)
        inchikey = Chem.MolToInchiKey(mol)
    except Exception as e:
        errors.append(f"Failed to generate canonical isomeric SMILES or InChIKey: {e}")
        return None, None, mol, warnings, errors, is_mixture, is_salt, has_ambiguous_stereo

    return canonical_smiles, inchikey, mol, warnings, errors, is_mixture, is_salt, has_ambiguous_stereo


def parse_csv_file(file_content_or_path: str, is_path: bool = False, default_context: Optional[Dict[str, str]] = None) -> Tuple[List[InputRow], List[str]]:
    global_warnings = []
    default_context = default_context or {}

    if is_path:
        with open(file_content_or_path, "r", encoding="utf-8-sig", newline="") as f:
            content = f.read()
    else:
        content = file_content_or_path
    if content.startswith("\ufeff"):
        content = content[1:]

    reader = csv.DictReader(io.StringIO(content))
    fieldnames = reader.fieldnames or []
    header_map = {h.strip().lower(): h for h in fieldnames}

    no_col = header_map.get("no")
    name_col = header_map.get("compound name") or header_map.get("compound_name") or header_map.get("chemical_name") or header_map.get("name")
    smiles_col = header_map.get("pubchem smiles") or header_map.get("smiles") or header_map.get("pubchem_smiles")

    if not (no_col and name_col and smiles_col):
        if len(fieldnames) >= 3 and not name_col and not smiles_col:
            no_col, name_col, smiles_col = fieldnames[0], fieldnames[1], fieldnames[2]
            global_warnings.append(f"Header mismatch, falling back to positional columns: {no_col}, {name_col}, {smiles_col}")
        else:
            raise ValueError(f"CSV missing required columns: 'No', 'Compound Name', 'PubChem SMILES'. Found: {fieldnames}")

    rows: List[InputRow] = []

    for row_idx, r in enumerate(reader, start=2):
        raw_no = str(r.get(no_col, f"{row_idx}")).strip()
        raw_name = str(r.get(name_col, "")).strip()
        raw_smiles = str(r.get(smiles_col, "")).strip()

        mojibake = detect_mojibake(raw_name)
        cleaned_name = raw_name
        doubled_backslash_found = "\\\\" in raw_smiles

        can_smiles, inchikey, mol, w_list, e_list, is_mix, is_salt, amb_stereo = validate_and_canonicalize_smiles(raw_smiles)

        medicine = r.get(header_map.get("medicine", ""), default_context.get("medicine"))
        system = r.get(header_map.get("system", ""), default_context.get("system", "Ayurveda"))
        formulation = r.get(header_map.get("formulation", ""), default_context.get("formulation"))
        plant = r.get(header_map.get("plant", ""), default_context.get("plant"))
        plant_type = r.get(header_map.get("plant_type", ""), default_context.get("plant_type"))
        part_used = r.get(header_map.get("part_used", ""), default_context.get("part_used"))
        family = r.get(header_map.get("family", ""), default_context.get("family"))
        common_name = r.get(header_map.get("common_name", ""), default_context.get("common_name"))

        diseases_val = r.get(header_map.get("diseases", "")) or default_context.get("diseases", "")
        if isinstance(diseases_val, str) and diseases_val.strip():
            diseases = [d.strip() for d in diseases_val.split(";") if d.strip()]
        elif isinstance(diseases_val, list):
            diseases = diseases_val
        else:
            diseases = []

        target_taxon_id_val = r.get(header_map.get("target_taxon_id", ""), default_context.get("target_taxon_id"))
        taxon_id = None
        if target_taxon_id_val:
            try:
                taxon_id = int(str(target_taxon_id_val).strip())
            except ValueError:
                w_list.append(f"Invalid taxon_id '{target_taxon_id_val}' ignored.")

        item = InputRow(
            raw_no=raw_no,
            raw_name=raw_name,
            raw_smiles=raw_smiles,
            cleaned_name=cleaned_name,
            cleaned_smiles=raw_smiles.strip(),
            canonical_smiles=can_smiles or "",
            inchikey=inchikey or "",
            pubchem_cid="",
            is_valid_smiles=bool(can_smiles),
            is_mixture=is_mix,
            is_salt=is_salt,
            has_ambiguous_stereochemistry=amb_stereo,
            mojibake_proposals=mojibake,
            doubled_backslash_found=doubled_backslash_found,
            warnings=w_list,
            errors=e_list,
            medicine=medicine,
            system=system,
            formulation=formulation,
            plant=plant,
            plant_type=plant_type,
            part_used=part_used,
            family=family,
            common_name=common_name,
            diseases=diseases,
            target_taxon_id=taxon_id,
        )
        rows.append(item)

    return rows, global_warnings
