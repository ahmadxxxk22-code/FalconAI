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
            "get_price must be implemented"
        )


    def get_24h(
        self,
        symbol: str,
        market: str = "crypto"
    ):
        raise NotImplementedError(
            "get_24h must be implemented"
        )


    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100,
        market: str = "crypto"
    ):
        raise NotImplementedError(
            "get_candles must be implemented"
        )
