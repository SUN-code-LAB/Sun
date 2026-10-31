"""
Offline deterministic tests for research pipeline, evidence tiering, and best structure selection.
"""
import unittest
from unittest.mock import MagicMock
from tradchem_engine.models import InputRow, TargetProtein
from tradchem_engine.researcher import ChemicalResearcher
from tradchem_engine.apis.structures import StructureClient


class TestResearcher(unittest.TestCase):

    def setUp(self):
        self.researcher = ChemicalResearcher(cache_db=":memory:")
        self.researcher.pubchem = MagicMock()
        self.researcher.chembl = MagicMock()
        self.researcher.uniprot = MagicMock()
        self.researcher.structures = MagicMock()
        self.researcher.literature = MagicMock()

    def test_pubchem_cid_matching(self):
        row = InputRow(
            raw_no="1", raw_name="Curcumin", raw_smiles="COC1=CC=CC=C1",
            cleaned_name="Curcumin", cleaned_smiles="COC1=CC=CC=C1",
            canonical_smiles="COC1=CC=CC=C1", is_valid_smiles=True
        )
        self.researcher.pubchem.search_by_smiles.return_value = 969516
        self.researcher.pubchem.search_by_name.return_value = 969516

        status, cid, warnings = self.researcher.identify_chemical(row)
        self.assertEqual(status, "VERIFIED")
        self.assertEqual(cid, 969516)

    def test_pubchem_name_structure_conflict(self):
        row = InputRow(
            raw_no="2", raw_name="Gallic acid", raw_smiles="CC(=O)O",
            cleaned_name="Gallic acid", cleaned_smiles="CC(=O)O",
            canonical_smiles="CC(=O)O", is_valid_smiles=True
        )
        self.researcher.pubchem.search_by_smiles.return_value = 176
        self.researcher.pubchem.search_by_name.return_value = 370

        status, cid, warnings = self.researcher.identify_chemical(row)
        self.assertEqual(status, "REVIEW_REQUIRED")
        self.assertEqual(cid, 176)

    def test_best_structure_selection_pdb_resolution(self):
        struct_client = StructureClient(cache=MagicMock())
        struct_client.get_pdb_resolution = MagicMock(side_effect=lambda pdb: 2.1 if pdb == "5IKR" else 1.5)
        struct_client.get_alphafold_model = MagicMock(return_value="AF-P35354-F1")

        best, others = struct_client.select_best_structure(["5IKR", "1ABC"], "P35354")
        self.assertEqual(best, "PDB:1ABC")
        self.assertIn("PDB:5IKR", others)
        self.assertIn("AlphaFold:AF-P35354-F1", others)

    def test_best_structure_fallback_to_alphafold(self):
        struct_client = StructureClient(cache=MagicMock())
        struct_client.get_pdb_resolution = MagicMock(return_value=None)
        struct_client.get_alphafold_model = MagicMock(return_value="AF-P03372-F1")

        best, others = struct_client.select_best_structure([], "P03372")
        self.assertEqual(best, "AlphaFold:AF-P03372-F1")

    def test_evidence_tiering_and_target_capping(self):
        self.researcher.chembl.search_molecule_by_inchikey.return_value = {"molecule_chembl_id": "CHEMBL1"}
        self.researcher.chembl.get_target.return_value = {
            "target_type": "SINGLE PROTEIN",
            "target_components": [{"accession": "P35354"}]
        }
        self.researcher.chembl.get_activities_for_molecule.return_value = [
            {"target_chembl_id": f"CHEMBL_T_{i}", "standard_type": "IC50", "standard_value": float(i*10), "standard_units": "nM", "pubmed_id": f"100{i}"}
            for i in range(15)
        ]
        self.researcher.chembl.get_target.side_effect = lambda tid: {
            "target_type": "SINGLE PROTEIN",
            "target_components": [{"accession": f"P{10000+int(tid.split('_')[-1])}"}]
        }
        self.researcher.uniprot.get_entry.return_value = None
        self.researcher.structures.select_best_structure.return_value = ("AlphaFold:AF-P10000-F1", [])

        row = InputRow(
            raw_no="1", raw_name="Test", raw_smiles="CC", cleaned_name="Test", cleaned_smiles="CC",
            canonical_smiles="CC", inchikey="INCHIKEY1", is_valid_smiles=True
        )
        targets = self.researcher.gather_targets(row, max_targets=10)
        self.assertEqual(len(targets), 10)
        self.assertEqual([t.rank for t in targets], list(range(1, 11)))


if __name__ == "__main__":
    unittest.main()
