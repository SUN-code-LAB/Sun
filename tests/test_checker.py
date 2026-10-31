"""
Offline deterministic tests for checker invocation, subprocess safety, and ZIP packaging.
"""
import tempfile
import unittest
import zipfile
from pathlib import Path

from tradchem_engine.models import ChemicalRecord, TargetProtein, BatchItemResult
from tradchem_engine.exporters import write_chemical_folder
from tradchem_engine.checker import check_submission_locally, run_repo_checker
from tradchem_engine.packaging import package_contribution_zip
from tradchem_engine.reports import write_batch_summary_csv


class TestCheckerAndPackaging(unittest.TestCase):

    def setUp(self):
        self.record = ChemicalRecord(
            chemical_name="gallic-acid",
            smiles="C1=C(C=C(C(=C1O)O)O)C(=O)O",
            pubchem_cid="370",
            medicine="Triphala",
            system="Ayurveda",
            plant="Terminalia chebula",
            plant_type="tree",
            part_used="fruit",
            family="Combretaceae",
            common_name="Haritaki",
            diseases=["inflammation"],
            targets=[
                TargetProtein(
                    rank=1, uniprot_id="P35354", protein_name="PTGS2", protein_acronym="PTGS2",
                    species="Homo sapiens", taxon_id=9606, cell_types=["macrophage"],
                    best_structure="PDB:5IKR", other_structures=["AlphaFold:AF-P35354-F1"],
                    go_terms=["GO:0006954 inflammatory response"], protein_diseases=["inflammation"],
                    method="literature", score="", source_ref="doi:10.1000/test"
                )
            ],
            system_slug="ayurvedha",
            formulation_slug="triphala",
            subcomponent_slug="terminalia-chebula",
            chemical_slug="gallic-acid"
        )

    def test_checker_rejects_example_source_ref(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad_record = self.record
            bad_record.targets[0].source_ref = "EXAMPLE ONLY - please replace"
            folder = write_chemical_folder(tmp, bad_record)
            code, errors, warnings = check_submission_locally(folder)
            self.assertEqual(code, 1)
            self.assertTrue(any("example source_ref" in e for e in errors))

    def test_checker_warns_on_fewer_than_10_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.record.targets[0].source_ref = "doi:10.1000/real_source"
            folder = write_chemical_folder(tmp, self.record)
            code, errors, warnings = check_submission_locally(folder)
            self.assertEqual(code, 0)
            self.assertTrue(any("expects the top 10" in w for w in warnings))

    def test_packaging_zip_contains_only_four_entries_in_chemical_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.record.targets[0].source_ref = "doi:10.1000/real_source"
            folder = write_chemical_folder(tmp, self.record)

            reports_dir = Path(tmp) / "reports"
            reports_dir.mkdir(parents=True, exist_ok=True)
            summary_path = str(reports_dir / "batch_summary.csv")
            write_batch_summary_csv([], summary_path)

            zip_dest = str(Path(tmp) / "output.zip")
            package_contribution_zip(tmp, zip_dest)

            with zipfile.ZipFile(zip_dest, "r") as zf:
                names = zf.namelist()
                self.assertIn("reports/batch_summary.csv", names)
                chem_folder_prefix = "tradchem/data/ayurvedha/formulations/triphala/terminalia-chebula/gallic-acid/"
                chem_files = [n for n in names if n.startswith(chem_folder_prefix)]
                chem_filenames = sorted([Path(n).name for n in chem_files])
                self.assertEqual(chem_filenames, ["__init__.py", "gallic-acid.csv", "gallic-acid.json", "gallic-acid.py"])


if __name__ == "__main__":
    unittest.main()
