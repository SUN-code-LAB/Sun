"""
Cache and shared rate limiter for Trad-Chem-LLM API clients.
"""
import hashlib
import json
import sqlite3
import threading
import time
from typing import Any, Dict, Optional, Tuple


class RateLimiter:
    def __init__(self, calls_per_second: float = 3.0):
        self.interval = 1.0 / max(calls_per_second, 0.1)
        self.last_call = 0.0
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_call
            if elapsed < self.interval:
                time.sleep(self.interval - elapsed)
            self.last_call = time.time()


class DiskCache:
    def __init__(self, cache_db_path: str = ":memory:"):
        self.db_path = cache_db_path
        self.lock = threading.Lock()
        if self.db_path == ":memory:":
            self._shared_con = sqlite3.connect(":memory:", check_same_thread=False)
            self._init_con(self._shared_con)
        else:
            self._shared_con = None
            con = sqlite3.connect(self.db_path)
            self._init_con(con)
            con.close()

    def _init_con(self, con: sqlite3.Connection):
        with self.lock:
            con.execute("""
                CREATE TABLE IF NOT EXISTS api_cache (
                    cache_key TEXT PRIMARY KEY,
                    service TEXT,
                    created_at REAL,
                    status_code INTEGER,
                    response_json TEXT
                )
            """)
            con.commit()

    def _get_con(self) -> sqlite3.Connection:
        if self._shared_con is not None:
            return self._shared_con
        return sqlite3.connect(self.db_path)

    @staticmethod
    def make_key(service: str, endpoint: str, params: Dict[str, Any]) -> str:
        serialized = json.dumps(params, sort_keys=True)
        raw = f"{service}:{endpoint}:{serialized}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, cache_key: str, max_age_seconds: Optional[float] = None) -> Optional[Tuple[int, Any]]:
        with self.lock:
            con = self._get_con()
            cur = con.execute("SELECT created_at, status_code, response_json FROM api_cache WHERE cache_key = ?", (cache_key,))
            row = cur.fetchone()
            if self._shared_con is None:
                con.close()
            if not row:
                return None
            created_at, status_code, response_json = row
            if max_age_seconds and (time.time() - created_at > max_age_seconds):
                return None
            try:
                data = json.loads(response_json)
                return status_code, data
            except Exception:
                return None

    def set(self, cache_key: str, service: str, status_code: int, data: Any):
        with self.lock:
            con = self._get_con()
            con.execute("""
                INSERT OR REPLACE INTO api_cache (cache_key, service, created_at, status_code, response_json)
                VALUES (?, ?, ?, ?, ?)
            """, (cache_key, service, time.time(), status_code, json.dumps(data)))
            con.commit()
            if self._shared_con is None:
                con.close()
