"""
Offline deterministic tests for CSV loader, mojibake detection, stereochemistry, and SMILES validation.
"""
import unittest
from rdkit import Chem
from tradchem_engine.csv_loader import parse_csv_file, detect_mojibake, slugify, validate_and_canonicalize_smiles


class TestCSVLoader(unittest.TestCase):

    def test_utf8_bom_and_exact_headers(self):
        csv_data = "\ufeffNo,Compound Name,PubChem SMILES\n1,Curcumin,COC1=C(C=CC(=C1)C=CC(=O)CC(=O)C=CC2=CC(=C(C=C2)O)OC)O\n"
        rows, warnings = parse_csv_file(csv_data)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].raw_no, "1")
        self.assertEqual(rows[0].raw_name, "Curcumin")
        self.assertTrue(rows[0].is_valid_smiles)

    def test_quoted_names_with_commas_and_brackets(self):
        csv_data = 'No,Compound Name,PubChem SMILES\n2,"Gallic acid, (anhydrous) [hydrate]",C1=C(C=C(C(=C1O)O)O)C(=O)O\n'
        rows, _ = parse_csv_file(csv_data)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].raw_name, "Gallic acid, (anhydrous) [hydrate]")
        self.assertTrue(rows[0].is_valid_smiles)

    def test_whitespace_trimming(self):
        csv_data = "No,Compound Name,PubChem SMILES\n 3 ,  Piperine  ,  C1=CC2=C(C=C1)OCO2  \n"
        rows, _ = parse_csv_file(csv_data)
        self.assertEqual(rows[0].raw_no, "3")
        self.assertEqual(rows[0].cleaned_name, "Piperine")
        self.assertTrue(rows[0].is_valid_smiles)

    def test_mojibake_proposal_and_review(self):
        name = "Î±-Amyrin"
        proposals = detect_mojibake(name)
        self.assertIn("Î±", proposals)
        self.assertEqual(proposals["Î±"], "α")

    def test_doubled_backslash_handling(self):
        smiles_with_doubled = "C/C=C\\\\C"
        can, inchikey, mol, w, e, is_mix, is_salt, amb = validate_and_canonicalize_smiles(smiles_with_doubled)
        self.assertTrue(any("doubled backslashes" in x for x in w))
        self.assertIsNotNone(can)

    def test_invalid_smiles(self):
        bad_smiles = "NOT_A_SMILES_STRING_123"
        can, inchikey, mol, w, e, is_mix, is_salt, amb = validate_and_canonicalize_smiles(bad_smiles)
        self.assertIsNone(can)
        self.assertTrue(len(e) > 0)

    def test_salt_and_mixture_detection(self):
        salt_smiles = "CC(=O)[O-].[Na+]"
        can, inchikey, mol, w, e, is_mix, is_salt, amb = validate_and_canonicalize_smiles(salt_smiles)
        self.assertTrue(is_mix)
        self.assertTrue(is_salt)

    def test_slugify(self):
        self.assertEqual(slugify("Gallic Acid"), "gallic-acid")
        self.assertEqual(slugify("Terminalia chebula (Haritaki)"), "terminalia-chebula-haritaki")
        self.assertEqual(slugify("Curcuma_longa--rhizome"), "curcuma-longa-rhizome")


if __name__ == "__main__":
    unittest.main()
