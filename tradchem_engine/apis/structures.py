"""
RCSB PDB and AlphaFold DB clients for structure resolution and best structure selection.
"""
import logging
from typing import Any, Dict, List, Optional, Tuple
import requests

from tradchem_engine.apis.cache import DiskCache, RateLimiter

logger = logging.getLogger(__name__)


class StructureClient:
    RCSB_DATA_URL = "https://data.rcsb.org/rest/v1/core/entry"
    ALPHAFOLD_URL = "https://alphafold.ebi.ac.uk/api/prediction"

    def __init__(self, cache: Optional[DiskCache] = None, rate_limiter: Optional[RateLimiter] = None):
        self.cache = cache or DiskCache()
        self.rate_limiter = rate_limiter or RateLimiter(calls_per_second=4.0)

    def get_pdb_resolution(self, pdb_id: str) -> Optional[float]:
        clean_pdb = pdb_id.strip().lower()
        cache_key = self.cache.make_key("rcsb", clean_pdb, {})
        cached = self.cache.get(cache_key)
        if cached:
            return cached[1]

        url = f"{self.RCSB_DATA_URL}/{clean_pdb}"
        self.rate_limiter.acquire()
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                resolution = None
                rcsb_entry_info = data.get("rcsb_entry_info", {})
                if "resolution_combined" in rcsb_entry_info:
                    res_list = rcsb_entry_info["resolution_combined"]
                    if res_list:
                        resolution = float(res_list[0])
                self.cache.set(cache_key, "rcsb", 200, resolution)
                return resolution
            else:
                self.cache.set(cache_key, "rcsb", resp.status_code, None)
                return None
        except Exception:
            return None

    def get_alphafold_model(self, uniprot_id: str) -> Optional[str]:
        clean_uid = uniprot_id.strip()
        cache_key = self.cache.make_key("alphafold", clean_uid, {})
        cached = self.cache.get(cache_key)
        if cached:
            return cached[1]

        url = f"{self.ALPHAFOLD_URL}/{clean_uid}"
        self.rate_limiter.acquire()
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data and isinstance(data, list) and len(data) > 0:
                    model_id = data[0].get("entryId")
                    if model_id:
                        self.cache.set(cache_key, "alphafold", 200, model_id)
                        return model_id
                model_id = f"AF-{clean_uid}-F1"
                self.cache.set(cache_key, "alphafold", 200, model_id)
                return model_id
            else:
                self.cache.set(cache_key, "alphafold", resp.status_code, None)
                return None
        except Exception:
            return None

    def select_best_structure(self, pdb_ids: List[str], uniprot_id: str) -> Tuple[str, List[str]]:
        pdb_resolutions = []
        for pdb_id in pdb_ids:
            res = self.get_pdb_resolution(pdb_id)
            pdb_resolutions.append((pdb_id, res if res is not None else 999.0))

        pdb_resolutions.sort(key=lambda x: x[1])

        all_structures = []
        if pdb_resolutions:
            best_id = pdb_resolutions[0][0].upper()
            best_structure = f"PDB:{best_id}"
            for p, _ in pdb_resolutions[1:]:
                all_structures.append(f"PDB:{p.upper()}")
            af_model = self.get_alphafold_model(uniprot_id)
            if af_model:
                all_structures.append(f"AlphaFold:{af_model}")
            return best_structure, all_structures

        af_model = self.get_alphafold_model(uniprot_id)
        if af_model:
            return f"AlphaFold:{af_model}", []

        if uniprot_id:
            return f"AlphaFold:AF-{uniprot_id}-F1", []

        return "", []
