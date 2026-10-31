"""
Offline deterministic tests for exporters and repository format agreement.
"""
import ast
import json
import tempfile
import unittest
from pathlib import Path
from tradchem_engine.models import ChemicalRecord, TargetProtein
from tradchem_engine.exporters import export_csv, export_json, export_py, write_chemical_folder
from tradchem_engine.checker import check_submission_locally


class TestExporters(unittest.TestCase):

    def setUp(self):
        self.record = ChemicalRecord(
            chemical_name="curcumin",
            smiles="COC1=C(C=CC(=C1)C=CC(=O)CC(=O)C=CC2=CC(=C(C=C2)O)OC)O",
            pubchem_cid="969516",
            medicine="Example Medicine A",
            system="Ayurveda",
            plant="Curcuma longa",
            plant_type="herb",
            part_used="rhizome",
            family="Zingiberaceae",
            common_name="Turmeric",
            diseases=["colorectal cancer", "arthritis"],
            targets=[
                TargetProtein(
                    rank=1, uniprot_id="P35354", protein_name="PTGS2", protein_acronym="PTGS2",
                    species="Homo sapiens", taxon_id=9606, cell_types=["macrophage", "epithelial cell"],
                    best_structure="PDB:5IKR", other_structures=["AlphaFold:AF-P35354-F1"],
                    go_terms=["GO:0006954 inflammatory response"], protein_diseases=["inflammation"],
                    method="literature", score="", source_ref="doi:10.1016/j.bmcl.2020.127500"
                )
            ],
            system_slug="ayurvedha",
            formulation_slug="example-formulation-1",
            subcomponent_slug="example-sub-component-1",
            chemical_slug="curcumin"
        )

    def test_single_canonical_record_generates_all_formats(self):
        csv_str = export_csv(self.record)
        json_str = export_json(self.record)
        py_str = export_py(self.record)

        self.assertIn("chemical_name", csv_str)
        self.assertIn("curcumin", csv_str)
        self.assertIn("P35354", csv_str)

        json_obj = json.loads(json_str)
        self.assertEqual(json_obj["chemical_name"], "curcumin")
        self.assertEqual(len(json_obj["targets"]), 1)
        self.assertEqual(json_obj["targets"][0]["uniprot_id"], "P35354")

        tree = ast.parse(py_str)
        chem_found = False
        targets_found = False
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id == "CHEMICAL":
                    chem_found = True
                elif node.targets[0].id == "TARGETS":
                    targets_found = True
        self.assertTrue(chem_found)
        self.assertTrue(targets_found)

    def test_write_chemical_folder_creates_four_files_and_passes_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = write_chemical_folder(tmp, self.record)
            p = Path(folder)
            files = sorted([f.name for f in p.iterdir()])
            self.assertEqual(files, ["__init__.py", "curcumin.csv", "curcumin.json", "curcumin.py"])

            code, errors, warnings = check_submission_locally(folder)
            self.assertEqual(code, 0, f"Errors: {errors}")


if __name__ == "__main__":
    unittest.main()
