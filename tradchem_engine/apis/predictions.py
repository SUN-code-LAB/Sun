"""
Prediction tools client and authentic export file parser.
"""
import csv
import io
from typing import Any, Dict, List, Optional
from tradchem_engine.models import TargetProtein


class PredictionAdapter:
    @staticmethod
    def parse_swisstargetprediction_csv(content: str, run_date: str = "2025-01-01") -> List[TargetProtein]:
        targets = []
        reader = csv.DictReader(io.StringIO(content))
        for row in reader:
            uniprot_id = row.get("Uniprot ID") or row.get("uniprot_id") or row.get("UniProt")
            if not uniprot_id or not uniprot_id.strip():
                continue
            uniprot_id = uniprot_id.strip().split()[0]
            prob_str = row.get("Probability*") or row.get("Probability") or row.get("score") or ""
            prob = 0.0
            try:
                prob = float(prob_str.strip())
            except ValueError:
                pass

            p_name = row.get("Common name") or row.get("Target") or ""
            acronym = row.get("Gene Symbol") or ""

            tp = TargetProtein(
                uniprot_id=uniprot_id,
                protein_name=p_name.strip(),
                protein_acronym=acronym.strip(),
                method="SwissTargetPrediction",
                score=f"{prob:.3f}" if prob > 0 else "",
                source_ref=f"SwissTargetPrediction (run date: {run_date})",
                evidence_tier=4,
                evidence_category="computational_prediction",
                raw_score=prob
            )
            targets.append(tp)
        return targets
