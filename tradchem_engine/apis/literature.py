"""
Literature client for PubMed and Europe PMC.
"""
import logging
import urllib.parse
from typing import Any, Dict, List, Optional
import requests

from tradchem_engine.apis.cache import DiskCache, RateLimiter

logger = logging.getLogger(__name__)


class LiteratureClient:
    EUROPE_PMC_SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

    def __init__(self, cache: Optional[DiskCache] = None, rate_limiter: Optional[RateLimiter] = None):
        self.cache = cache or DiskCache()
        self.rate_limiter = rate_limiter or RateLimiter(calls_per_second=3.0)

    def search_europe_pmc(self, chemical_name: str, protein_name: str) -> Optional[Dict[str, str]]:
        query = f'("{chemical_name}") AND ("{protein_name}") AND (inhibitor OR binding OR target OR "ic50" OR "kd" OR "ki" OR affinity)'
        cache_key = self.cache.make_key("europepmc", query, {})
        cached = self.cache.get(cache_key)
        if cached:
            return cached[1]

        self.rate_limiter.acquire()
        try:
            params = {
                "query": query,
                "format": "json",
                "pageSize": 5,
                "resultType": "lite"
            }
            resp = requests.get(self.EUROPE_PMC_SEARCH, params=params, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("resultList", {}).get("result", [])
                if results:
                    best = results[0]
                    doi = best.get("doi", "")
                    pmid = best.get("pmid", "")
                    title = best.get("title", "")
                    source_info = {
                        "doi": f"doi:{doi}" if doi and not doi.startswith("doi:") else doi,
                        "pmid": f"PMID:{pmid}" if pmid else "",
                        "title": title,
                        "verified_target": True
                    }
                    self.cache.set(cache_key, "europepmc", 200, source_info)
                    return source_info
                else:
                    self.cache.set(cache_key, "europepmc", 200, None)
                    return None
            else:
                return None
        except Exception:
            return None
