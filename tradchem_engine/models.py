"""
Canonical data models for Trad-Chem-LLM.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any


@dataclass
class TargetProtein:
    """Represents a single protein target for a chemical."""
    rank: int = 0
    uniprot_id: str = ""
    protein_name: str = ""
    protein_acronym: str = ""
    species: str = "Homo sapiens"
    taxon_id: int = 9606
    cell_types: List[str] = field(default_factory=list)
    best_structure: str = ""
    other_structures: List[str] = field(default_factory=list)
    go_terms: List[str] = field(default_factory=list)
    protein_diseases: List[str] = field(default_factory=list)
    method: str = ""
    score: str = ""  # string representation of float or empty
    source_ref: str = ""

    # Internal provenance fields (preserved in reports, not in exported contribution)
    evidence_tier: int = 5
    evidence_category: str = ""
    raw_score: Optional[float] = None
    score_units: str = ""
    assay_id: str = ""
    document_id: str = ""
    pmid: str = ""
    doi: str = ""
    notes: List[str] = field(default_factory=list)

    def to_slot_dict(self) -> Dict[str, Any]:
        """Convert to dictionary matching the repository slot(...) signature."""
        return {
            "uniprot_id": self.uniprot_id,
            "protein_name": self.protein_name,
            "protein_acronym": self.protein_acronym,
            "species": self.species,
            "taxon_id": self.taxon_id if self.taxon_id else "",
            "cell_types": list(self.cell_types),
            "best_structure": self.best_structure,
            "other_structures": list(self.other_structures),
            "go_terms": list(self.go_terms),
            "protein_diseases": list(self.protein_diseases),
            "method": self.method,
            "score": float(self.score) if (self.score and self._is_float(self.score)) else (self.score or ""),
            "source_ref": self.source_ref,
        }

    @staticmethod
    def _is_float(val: Any) -> bool:
        try:
            float(val)
            return True
        except (ValueError, TypeError):
            return False


@dataclass
class ChemicalRecord:
    """Canonical chemical record linking medicine/plant context and protein targets."""
    chemical_name: str
    smiles: str
    pubchem_cid: str = ""
    medicine: str = "Example Medicine A"
    system: str = "Ayurveda"
    plant: str = "Curcuma longa"
    plant_type: str = "herb"
    part_used: str = "rhizome"
    family: str = "Zingiberaceae"
    common_name: str = "Turmeric"
    diseases: List[str] = field(default_factory=list)

    # Target proteins (ranked 1..N, max 10)
    targets: List[TargetProtein] = field(default_factory=list)

    # Hierarchy path slugs (lowercase hyphenated)
    system_slug: str = "ayurvedha"
    formulation_slug: str = "example-formulation-1"
    subcomponent_slug: str = "example-sub-component-1"
    chemical_slug: str = ""

    def to_chemical_dict(self) -> Dict[str, Any]:
        """Convert chemical-level fields to dictionary."""
        return {
            "medicine": self.medicine,
            "system": self.system,
            "plant": self.plant,
            "plant_type": self.plant_type,
            "part_used": self.part_used,
            "family": self.family,
            "common_name": self.common_name,
            "chemical_name": self.chemical_name,
            "smiles": self.smiles,
            "pubchem_cid": self.pubchem_cid,
            "diseases": list(self.diseases),
        }


@dataclass
class InputRow:
    """Represents one parsed row from the input CSV."""
    raw_no: str
    raw_name: str
    raw_smiles: str
    cleaned_name: str
    cleaned_smiles: str
    canonical_smiles: str = ""
    inchikey: str = ""
    molecular_formula: str = ""
    pubchem_cid: str = ""
    is_valid_smiles: bool = False
    is_mixture: bool = False
    is_salt: bool = False
    has_ambiguous_stereochemistry: bool = False
    mojibake_proposals: Dict[str, str] = field(default_factory=dict)
    doubled_backslash_found: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    # Optional context attributes
    medicine: Optional[str] = None
    system: Optional[str] = None
    formulation: Optional[str] = None
    plant: Optional[str] = None
    plant_type: Optional[str] = None
    part_used: Optional[str] = None
    family: Optional[str] = None
    common_name: Optional[str] = None
    diseases: List[str] = field(default_factory=list)
    target_taxon_id: Optional[int] = None


@dataclass
class BatchItemResult:
    """Tracks end-to-end processing outcome for a single chemical context."""
    input_no: str
    input_name: str
    normalized_name: str
    supplied_smiles: str
    canonical_smiles: str
    pubchem_cid: str
    identity_status: str  # VERIFIED, REVIEW_REQUIRED, FAILED
    candidates_found: int = 0
    experimental_targets: int = 0
    literature_targets: int = 0
    predicted_targets: int = 0
    exported_targets: int = 0
    evidence_quality: str = "none"
    missing_fields: List[str] = field(default_factory=list)
    chemical_folder: str = ""
    checker_status: str = "NOT_RUN"  # PASS, STANDALONE_VALID, REVIEW_REQUIRED, INCOMPLETE, FAILED
    validation_status: str = "PENDING"
    warning_or_error: str = ""
    record: Optional[ChemicalRecord] = None
    audit_data: Dict[str, Any] = field(default_factory=dict)
