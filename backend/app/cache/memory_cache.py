import threading
import time
from typing import Any, Dict, Optional


class MemoryCache:
    """
    Thread-safe in-memory cache with TTL support.
    """

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def set(
        self,
        key: str,
        value: Any,
        ttl: int = 60
    ) -> None:

        expire_at = time.time() + ttl

        with self._lock:
            self._cache[key] = {
                "value": value,
                "expire_at": expire_at
            }

    def get(
        self,
        key: str
    ) -> Optional[Any]:

        with self._lock:

            item = self._cache.get(key)

            if item is None:
                return None

            if time.time() >= item["expire_at"]:
                del self._cache[key]
                return None

            return item["value"]

    def has(
        self,
        key: str
    ) -> bool:

        return self.get(key) is not None

    def delete(
        self,
        key: str
    ) -> None:

        with self._lock:

            if key in self._cache:
                del self._cache[key]

    def clear(self) -> None:

        with self._lock:
            self._cache.clear()

    def cleanup(self) -> None:
        """
        Remove expired entries.
        """

        now = time.time()

        with self._lock:

            expired = []

            for key, value in self._cache.items():

                if value["expire_at"] <= now:
                    expired.append(key)

            for key in expired:
                del self._cache[key]

    def stats(self) -> Dict[str, Any]:

        self.cleanup()

        with self._lock:

            return {
                "items": len(self._cache),
                "timestamp": int(time.time())
      }
