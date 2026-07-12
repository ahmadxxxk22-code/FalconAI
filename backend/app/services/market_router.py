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

    # ==========================================
    # Provider Selection
    # ==========================================

    def get_providers(self, market="crypto"):

        if market == "crypto":
            return self.crypto

        if market == "stocks":
            return self.stocks

        if market == "forex":
            return self.forex

        return self.crypto

    # ==========================================
    # Symbol Mapping
    # ==========================================

    def map_symbol(self, provider, symbol):

        name = provider.provider_name

        if name == "OKX":
            return symbol.replace("USDT", "-USDT")

        if name == "Coinbase":
            return symbol.replace("USDT", "-USD")

        if name == "Kraken":
            if symbol == "BTCUSDT":
                return "XBTUSDT"

        return symbol

    # ==========================================
    # Price
    # ==========================================

    def get_price(
        self,
        symbol,
        market="crypto"
    ):

        last_error = None

        for provider in self.get_providers(market):

            try:

                provider_symbol = self.map_symbol(
                    provider,
                    symbol
                )

                return provider.get_price(
                    provider_symbol,
                    market
                )

            except Exception as e:

                last_error = e

        raise Exception(
            f"No Provider Available: {last_error}"
        )

    # ==========================================
    # 24H
    # ==========================================

    def get_24h(
        self,
        symbol,
        market="crypto"
    ):

        last_error = None

        for provider in self.get_providers(market):

            try:

                provider_symbol = self.map_symbol(
                    provider,
                    symbol
                )

                return provider.get_24h(
                    provider_symbol,
                    market
                )

            except Exception as e:

                last_error = e

        raise Exception(
            f"No Provider Available: {last_error}"
        )

    # ==========================================
    # Candles
    # ==========================================

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

                provider_symbol = self.map_symbol(
                    provider,
                    symbol
                )

                return provider.get_candles(
                    provider_symbol,
                    interval,
                    limit,
                    market
                )

            except Exception as e:

                last_error = e

        raise Exception(
            f"No Provider Available: {last_error}"
            )
