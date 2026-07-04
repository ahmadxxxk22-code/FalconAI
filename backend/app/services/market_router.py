from app.services.providers.binance_service import BinanceService
from app.services.providers.bybit_service import BybitService
from app.services.providers.okx_service import OKXService
from app.services.providers.coinbase_service import CoinbaseService
from app.services.providers.kraken_service import KrakenService
from app.services.providers.yahoo_service import YahooService
from app.services.providers.finnhub_service import FinnhubService
from app.services.providers.twelvedata_service import TwelveDataService


class MarketRouter:

    def __init__(self):

        self.crypto = [

            BinanceService(),

            BybitService(),

            OKXService(),

            CoinbaseService(),

            KrakenService()

        ]

        self.stocks = [

            YahooService(),

            FinnhubService()

        ]

        self.forex = [

            TwelveDataService()

        ]

    def get_providers(self, market="crypto"):

        if market == "crypto":
            return self.crypto

        if market == "stocks":
            return self.stocks

        if market == "forex":
            return self.forex

        return self.crypto

    def get_price(
        self,
        symbol,
        market="crypto"
    ):

        last_error = None

        for provider in self.get_providers(market):

            try:

                return provider.get_price(symbol)

            except Exception as e:

                last_error = e

        raise Exception(f"No Provider Available: {last_error}")

    def get_24h(
        self,
        symbol,
        market="crypto"
    ):

        last_error = None

        for provider in self.get_providers(market):

            try:

                return provider.get_24h(symbol)

            except Exception as e:

                last_error = e

        raise Exception(f"No Provider Available: {last_error}")

    def get_candles(
        self,
        symbol,
        interval="1h",
        limit=200,
        market="crypto"
    ):

        last_error = None

        for provider in self.get_providers(market):

            try:

                return provider.get_candles(
                    symbol,
                    interval,
                    limit
                )

            except Exception as e:

                last_error = e

        raise Exception(f"No Provider Available: {last_error}")
