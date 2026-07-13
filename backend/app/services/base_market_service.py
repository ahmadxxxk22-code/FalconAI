from abc import ABC


class BaseMarketService(ABC):

    @property
    def provider_name(self):
        return self.__class__.__name__


    def get_price(
        self,
        symbol: str,
        market: str = "crypto"
    ):
        raise NotImplementedError(
            "Provider must implement get_price()"
        )


    def get_24h(
        self,
        symbol: str,
        market: str = "crypto"
    ):
        raise NotImplementedError(
            "Provider must implement get_24h()"
        )


    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100,
        market: str = "crypto"
    ):
        raise NotImplementedError(
            "Provider must implement get_candles()"
        )
