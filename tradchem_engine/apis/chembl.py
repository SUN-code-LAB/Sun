"""
ChEMBL API client for target and experimental bioactivity retrieval.
"""
import logging
import urllib.parse
from typing import Any, Dict, List, Optional
import requests

from tradchem_engine.apis.cache import DiskCache, RateLimiter

logger = logging.getLogger(__name__)


class ChEMBLClient:
    BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"

    def __init__(self, cache: Optional[DiskCache] = None, rate_limiter: Optional[RateLimiter] = None):
        self.cache = cache or DiskCache()
        self.rate_limiter = rate_limiter or RateLimiter(calls_per_second=3.0)

    def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        params = params or {}
        params["format"] = "json"
        cache_key = self.cache.make_key("chembl", endpoint, params)
        cached = self.cache.get(cache_key)
        if cached:
            return cached[1]

        url = f"{self.BASE_URL}/{endpoint}"
        self.rate_limiter.acquire()
        try:
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                self.cache.set(cache_key, "chembl", 200, data)
                return data
            elif resp.status_code == 404:
                self.cache.set(cache_key, "chembl", 404, None)
                return None
            else:
                return None
        except Exception:
            return None

    def search_molecule_by_smiles(self, smiles: str) -> Optional[Dict[str, Any]]:
        encoded = urllib.parse.quote(smiles.strip())
        data = self._request(f"molecule/{encoded}")
        return data

    def search_molecule_by_inchikey(self, inchikey: str) -> Optional[Dict[str, Any]]:
        data = self._request("molecule", {"molecule_structures__standard_inchi_key": inchikey})
        if data and "molecules" in data and data["molecules"]:
            return data["molecules"][0]
        return None

    def get_activities_for_molecule(self, chembl_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        data = self._request("activity", {
            "molecule_chembl_id": chembl_id,
            "limit": limit
        })
        if data and "activities" in data:
            return data["activities"]
        return []

    def get_target(self, target_chembl_id: str) -> Optional[Dict[str, Any]]:
        data = self._request(f"target/{target_chembl_id}")
        return data
