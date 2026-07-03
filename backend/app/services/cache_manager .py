import time


class CacheManager:

    def __init__(self):

        self.cache = {}

    def set(
        self,
        key,
        value,
        ttl=30
    ):

        self.cache[key] = {

            "value": value,

            "expires": time.time() + ttl

        }

    def get(self, key):

        if key not in self.cache:

            return None

        item = self.cache[key]

        if time.time() > item["expires"]:

            del self.cache[key]

            return None

        return item["value"]

    def delete(self, key):

        if key in self.cache:

            del self.cache[key]

    def clear(self):

        self.cache.clear()
