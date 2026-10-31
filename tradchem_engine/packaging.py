"""
ZIP packaging utility for Trad-Chem-LLM.
"""
import os
import zipfile
from pathlib import Path


def package_contribution_zip(base_dir: str, zip_output_path: str) -> str:
    base = Path(base_dir)
    zip_path = Path(zip_output_path)
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        tradchem_dir = base / "tradchem"
        if tradchem_dir.exists():
            for root, dirs, files in os.walk(tradchem_dir):
                for file in files:
                    full_p = Path(root) / file
                    arc_name = full_p.relative_to(base)
                    zf.write(full_p, arc_name)

        reports_dir = base / "reports"
        if reports_dir.exists():
            for root, dirs, files in os.walk(reports_dir):
                for file in files:
                    full_p = Path(root) / file
                    arc_name = full_p.relative_to(base)
                    zf.write(full_p, arc_name)

    return str(zip_path)
