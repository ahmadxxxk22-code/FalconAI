import time


class ProviderHealth:

    def __init__(self):

        self.providers = {}

    def mark_success(self, provider):

        self.providers[provider] = {

            "status": "ONLINE",

            "last_check": time.time()

        }

    def mark_failed(self, provider):

        self.providers[provider] = {

            "status": "OFFLINE",

            "last_check": time.time()

        }

    def status(self, provider):

        return self.providers.get(

            provider,

            {

                "status": "UNKNOWN",

                "last_check": None

            }

        )

    def all(self):

        return self.providers
