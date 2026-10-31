"""
PubChem PUG REST client for chemical identification and property cross-matching.
"""
import logging
import urllib.parse
from typing import Any, Dict, List, Optional
import requests

from tradchem_engine.apis.cache import DiskCache, RateLimiter

logger = logging.getLogger(__name__)


class PubChemClient:
    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def __init__(self, cache: Optional[DiskCache] = None, rate_limiter: Optional[RateLimiter] = None):
        self.cache = cache or DiskCache()
        self.rate_limiter = rate_limiter or RateLimiter(calls_per_second=4.0)

    def _request(self, path: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        params = params or {}
        cache_key = self.cache.make_key("pubchem", path, params)
        cached = self.cache.get(cache_key)
        if cached:
            return cached[1]

        url = f"{self.BASE_URL}/{path}"
        self.rate_limiter.acquire()
        try:
            resp = requests.get(url, params=params, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                self.cache.set(cache_key, "pubchem", 200, data)
                return data
            elif resp.status_code == 404:
                self.cache.set(cache_key, "pubchem", 404, None)
                return None
            else:
                return None
        except Exception as e:
            return None

    def search_by_name(self, name: str) -> Optional[int]:
        clean_name = name.strip()
        encoded = urllib.parse.quote(clean_name)
        data = self._request(f"compound/name/{encoded}/cids/JSON")
        if data and "IdentifierList" in data and "CID" in data["IdentifierList"]:
            cids = data["IdentifierList"]["CID"]
            if cids:
                return int(cids[0])
        return None

    def search_by_smiles(self, smiles: str) -> Optional[int]:
        clean_smiles = smiles.strip()
        encoded = urllib.parse.quote(clean_smiles)
        data = self._request(f"compound/smiles/{encoded}/cids/JSON")
        if data and "IdentifierList" in data and "CID" in data["IdentifierList"]:
            cids = data["IdentifierList"]["CID"]
            if cids:
                return int(cids[0])
        return None

    def get_compound_properties(self, cid: int) -> Optional[Dict[str, Any]]:
        props = "CanonicalSMILES,IsomericSMILES,InChIKey,Title,MolecularFormula,IUPACName"
        data = self._request(f"compound/cid/{cid}/property/{props}/JSON")
        if data and "PropertyTable" in data and "Properties" in data["PropertyTable"]:
            records = data["PropertyTable"]["Properties"]
            if records:
                return records[0]
        return None
