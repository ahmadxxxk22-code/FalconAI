from abc import ABC, abstractmethod


class BaseMarketService(ABC):


    @property
    @abstractmethod
    def provider_name(self):

        pass



    @abstractmethod
    def get_price(
        self,
        symbol: str,
        market: str = "crypto"
    ):

        pass



    @abstractmethod
    def get_24h(
        self,
        symbol: str,
        market: str = "crypto"
    ):

        pass



    @abstractmethod
    def get_candles(
        self,
        symbol: str,
        interval: str,
        limit: int = 100,
        market: str = "crypto"
    ):

        pass
        
