from abc import ABC, abstractmethod


class BaseMarketService(ABC):

    @abstractmethod
    def get_price(self, symbol: str):
        pass

    @abstractmethod
    def get_24h(self, symbol: str):
        pass

    @abstractmethod
    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100
    ):
        pass
