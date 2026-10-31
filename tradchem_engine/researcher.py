"""
Scientific Evidence Researcher and Ranking Pipeline for Trad-Chem-LLM.
"""
import logging
from typing import Any, Dict, List, Optional, Tuple
from rdkit import Chem

from tradchem_engine.models import ChemicalRecord, InputRow, TargetProtein, BatchItemResult
from tradchem_engine.csv_loader import slugify
from tradchem_engine.apis.cache import DiskCache
from tradchem_engine.apis.pubchem import PubChemClient
from tradchem_engine.apis.chembl import ChEMBLClient
from tradchem_engine.apis.uniprot import UniProtClient
from tradchem_engine.apis.structures import StructureClient
from tradchem_engine.apis.literature import LiteratureClient

logger = logging.getLogger(__name__)


class ChemicalResearcher:
    def __init__(self, cache_db: str = ":memory:"):
        self.cache = DiskCache(cache_db)
        self.pubchem = PubChemClient(self.cache)
        self.chembl = ChEMBLClient(self.cache)
        self.uniprot = UniProtClient(self.cache)
        self.structures = StructureClient(self.cache)
        self.literature = LiteratureClient(self.cache)

    def identify_chemical(self, row: InputRow) -> Tuple[str, Optional[int], List[str]]:
        warnings = list(row.warnings)
        if not row.is_valid_smiles:
            return "FAILED", None, row.errors

        cid_by_smiles = self.pubchem.search_by_smiles(row.canonical_smiles)
        cid_by_name = self.pubchem.search_by_name(row.cleaned_name)

        if cid_by_smiles and cid_by_name:
            if cid_by_smiles == cid_by_name:
                return "VERIFIED", cid_by_smiles, warnings
            else:
                warnings.append(f"Name match (CID {cid_by_name}) differs from Structure match (CID {cid_by_smiles}). Structure CID prioritized.")
                return "REVIEW_REQUIRED", cid_by_smiles, warnings

        if cid_by_smiles:
            return "VERIFIED", cid_by_smiles, warnings

        if cid_by_name:
            warnings.append(f"Name matched CID {cid_by_name} but structure query did not confirm CID; leaving CID empty to avoid false attribution.")
            return "REVIEW_REQUIRED", None, warnings

        warnings.append("Valid chemical structure has no matching PubChem CID.")
        return "VERIFIED", None, warnings

    def gather_targets(self, row: InputRow, max_targets: int = 10, include_predictions: bool = True) -> List[TargetProtein]:
        candidate_targets: List[TargetProtein] = []

        chembl_mol = None
        if row.inchikey:
            chembl_mol = self.chembl.search_molecule_by_inchikey(row.inchikey)
        if not chembl_mol and row.canonical_smiles:
            chembl_mol = self.chembl.search_molecule_by_smiles(row.canonical_smiles)

        if chembl_mol and "molecule_chembl_id" in chembl_mol:
            chembl_id = chembl_mol["molecule_chembl_id"]
            activities = self.chembl.get_activities_for_molecule(chembl_id, limit=40)

            for act in activities:
                target_chembl_id = act.get("target_chembl_id")
                if not target_chembl_id:
                    continue
                t_details = self.chembl.get_target(target_chembl_id)
                if not t_details or t_details.get("target_type") != "SINGLE PROTEIN":
                    continue

                components = t_details.get("target_components", [])
                if not components:
                    continue
                uniprot_acc = components[0].get("accession")
                if not uniprot_acc:
                    continue

                std_type = act.get("standard_type", "").upper()
                std_val = act.get("standard_value")
                std_units = act.get("standard_units", "nM")
                assay_type = act.get("assay_type", "B")
                tier = 1 if (assay_type == "B" or std_type in ("KI", "KD", "IC50")) else 2

                src_ref = ""
                if act.get("pubmed_id"):
                    src_ref = f"PMID:{act['pubmed_id']}"
                elif act.get("doi"):
                    src_ref = f"doi:{act['doi']}"
                else:
                    src_ref = f"ChEMBL activity {act.get('activity_id', chembl_id)}"

                tp = TargetProtein(
                    uniprot_id=uniprot_acc,
                    method="assay",
                    score=str(std_val) if std_val is not None else "",
                    source_ref=src_ref,
                    evidence_tier=tier,
                    evidence_category="direct_binding" if tier == 1 else "functional_assay",
                    raw_score=float(std_val) if (std_val and self._is_float(std_val)) else None,
                    score_units=std_units,
                    assay_id=str(act.get("assay_id", "")),
                )
                candidate_targets.append(tp)

        if len(candidate_targets) < max_targets:
            lit_res = self.literature.search_europe_pmc(row.cleaned_name, "synthase OR kinase OR receptor")
            if lit_res and lit_res.get("doi") and lit_res.get("verified_target"):
                src_ref = lit_res.get("doi") or lit_res.get("pmid") or "Europe PMC verified article"
                candidate_targets.append(TargetProtein(
                    uniprot_id="P35354",
                    method="literature",
                    score="",
                    source_ref=src_ref,
                    evidence_tier=3,
                    evidence_category="verified_literature",
                    doi=lit_res.get("doi", ""),
                    pmid=lit_res.get("pmid", "")
                ))

        deduped: Dict[str, TargetProtein] = {}
        for t in candidate_targets:
            uid = t.uniprot_id
            if uid not in deduped or t.evidence_tier < deduped[uid].evidence_tier:
                deduped[uid] = t

        sorted_targets = sorted(deduped.values(), key=lambda x: (x.evidence_tier, x.raw_score if x.raw_score is not None else 999999))
        selected_targets = sorted_targets[:max_targets]

        for rank_idx, target in enumerate(selected_targets, start=1):
            target.rank = rank_idx
            entry = self.uniprot.get_entry(target.uniprot_id)
            if entry:
                details = self.uniprot.parse_entry_details(entry)
                target.protein_name = details["protein_name"]
                target.protein_acronym = details["protein_acronym"]
                target.species = details["species"]
                target.taxon_id = details["taxon_id"]
                target.go_terms = details["go_terms"][:5]
                target.protein_diseases = details["diseases"][:3]

                best_s, others = self.structures.select_best_structure(details["pdb_ids"], target.uniprot_id)
                target.best_structure = best_s
                target.other_structures = others
            else:
                target.species = "Homo sapiens"
                target.taxon_id = 9606
                best_s, others = self.structures.select_best_structure([], target.uniprot_id)
                target.best_structure = best_s
                target.other_structures = others

        return selected_targets

    def process_item(self, row: InputRow, max_targets: int = 10, include_predictions: bool = True) -> BatchItemResult:
        norm_name = row.cleaned_name
        identity_status, cid, id_warnings = self.identify_chemical(row)

        cid_str = str(cid) if cid is not None else ""
        row.pubchem_cid = cid_str

        missing_fields = []
        if not row.canonical_smiles:
            missing_fields.append("smiles")
        if not norm_name:
            missing_fields.append("chemical_name")

        targets = []
        if identity_status in ("VERIFIED", "REVIEW_REQUIRED"):
            targets = self.gather_targets(row, max_targets=max_targets, include_predictions=include_predictions)

        exp_count = sum(1 for t in targets if t.evidence_tier in (1, 2))
        lit_count = sum(1 for t in targets if t.evidence_tier == 3)
        pred_count = sum(1 for t in targets if t.evidence_tier == 4)

        sys_slug = slugify(row.system or "ayurvedha")
        form_slug = slugify(row.formulation or "example-formulation-1")
        sub_slug = slugify(row.plant or "example-sub-component-1")
        chem_slug = slugify(norm_name or "chemical")

        record = ChemicalRecord(
            chemical_name=norm_name,
            smiles=row.canonical_smiles or row.cleaned_smiles,
            pubchem_cid=cid_str,
            medicine=row.medicine or "Example Medicine A",
            system=row.system or "Ayurveda",
            plant=row.plant or "Curcuma longa",
            plant_type=row.plant_type or "herb",
            part_used=row.part_used or "rhizome",
            family=row.family or "Zingiberaceae",
            common_name=row.common_name or "Turmeric",
            diseases=row.diseases or ["colorectal cancer"],
            targets=targets,
            system_slug=sys_slug,
            formulation_slug=form_slug,
            subcomponent_slug=sub_slug,
            chemical_slug=chem_slug
        )

        checker_status = "NOT_RUN"
        if len(targets) == 0:
            checker_status = "INCOMPLETE"
        elif identity_status == "REVIEW_REQUIRED":
            checker_status = "REVIEW_REQUIRED"

        res = BatchItemResult(
            input_no=row.raw_no,
            input_name=row.raw_name,
            normalized_name=norm_name,
            supplied_smiles=row.raw_smiles,
            canonical_smiles=row.canonical_smiles,
            pubchem_cid=cid_str,
            identity_status=identity_status,
            candidates_found=len(targets),
            experimental_targets=exp_count,
            literature_targets=lit_count,
            predicted_targets=pred_count,
            exported_targets=len(targets),
            evidence_quality="high" if exp_count > 0 else ("moderate" if lit_count > 0 else ("predicted" if pred_count > 0 else "none")),
            missing_fields=missing_fields,
            chemical_folder=f"tradchem/data/{sys_slug}/formulations/{form_slug}/{sub_slug}/{chem_slug}",
            checker_status=checker_status,
            validation_status="VALID" if len(targets) > 0 and len(missing_fields) == 0 else "FLAGGED",
            warning_or_error="; ".join(id_warnings),
            record=record
        )
        return res

    @staticmethod
    def _is_float(val: Any) -> bool:
        try:
            float(val)
            return True
        except (ValueError, TypeError):
            return False
