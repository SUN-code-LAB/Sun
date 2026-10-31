"""
UniProt REST client for protein annotation, taxonomy, GO terms, and disease cross-referencing.
"""
import logging
from typing import Any, Dict, List, Optional
import requests

from tradchem_engine.apis.cache import DiskCache, RateLimiter

logger = logging.getLogger(__name__)


class UniProtClient:
    BASE_URL = "https://rest.uniprot.org"

    def __init__(self, cache: Optional[DiskCache] = None, rate_limiter: Optional[RateLimiter] = None):
        self.cache = cache or DiskCache()
        self.rate_limiter = rate_limiter or RateLimiter(calls_per_second=4.0)

    def _request(self, path: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        params = params or {}
        cache_key = self.cache.make_key("uniprot", path, params)
        cached = self.cache.get(cache_key)
        if cached:
            return cached[1]

        url = f"{self.BASE_URL}/{path}"
        self.rate_limiter.acquire()
        headers = {"Accept": "application/json"}
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                self.cache.set(cache_key, "uniprot", 200, data)
                return data
            else:
                return None
        except Exception:
            return None

    def get_entry(self, accession: str) -> Optional[Dict[str, Any]]:
        clean_acc = accession.strip()
        data = self._request(f"uniprotkb/{clean_acc}")
        return data

    def parse_entry_details(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        res = {
            "protein_name": "",
            "protein_acronym": "",
            "species": "Homo sapiens",
            "taxon_id": 9606,
            "go_terms": [],
            "diseases": [],
            "cell_types": [],
            "pdb_ids": [],
        }
        if not entry:
            return res

        protein_desc = entry.get("proteinDescription", {})
        rec_name = protein_desc.get("recommendedName", {})
        if "fullName" in rec_name:
            res["protein_name"] = rec_name["fullName"].get("value", "")

        genes = entry.get("genes", [])
        if genes and "geneName" in genes[0]:
            res["protein_acronym"] = genes[0]["geneName"].get("value", "")

        org = entry.get("organism", {})
        if "scientificName" in org:
            res["species"] = org["scientificName"]
        if "taxonId" in org:
            res["taxon_id"] = int(org["taxonId"])

        xrefs = entry.get("uniProtKBCrossReferences", [])
        for xr in xrefs:
            db = xr.get("database")
            if db == "GO":
                go_id = xr.get("id")
                props = {p.get("key"): p.get("value") for p in xr.get("properties", [])}
                go_term_name = props.get("GoTerm", "")
                if go_term_name.startswith("P:") or go_term_name.startswith("F:") or go_term_name.startswith("C:"):
                    go_term_name = go_term_name[2:].strip()
                if go_id:
                    res["go_terms"].append(f"{go_id} {go_term_name}".strip())
            elif db == "PDB":
                pdb_id = xr.get("id")
                if pdb_id:
                    res["pdb_ids"].append(pdb_id.upper())

        comments = entry.get("comments", [])
        for c in comments:
            if c.get("commentType") == "DISEASE":
                d_info = c.get("disease", {})
                d_name = d_info.get("diseaseId") or d_info.get("acronym")
                if d_name:
                    res["diseases"].append(d_name.lower())

        return res
