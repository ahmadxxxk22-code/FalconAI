from app.services.binance_service import BinanceService
from app.services.bybit_service import BybitService


class MarketRouter:

    def __init__(self):

        self.providers = [

            BinanceService(),

            BybitService(),

        ]

    def get_price(self, symbol="BTCUSDT"):

        last_error = None

        for provider in self.providers:

            try:

                return provider.get_price(symbol)

            except Exception as e:

                last_error = e

                continue

        raise Exception(

            f"No Market Provider Available: {last_error}"

        )

    def get_24h(self, symbol="BTCUSDT"):

        last_error = None

        for provider in self.providers:

            try:

                return provider.get_24h(symbol)

            except Exception as e:

                last_error = e

                continue

        raise Exception(

            f"No Market Provider Available: {last_error}"

        )

    def get_candles(

        self,

        symbol="BTCUSDT",

        interval="1h",

        limit=200

    ):

        last_error = None

        for provider in self.providers:

            try:

                return provider.get_candles(

                    symbol,

                    interval,

                    limit

                )

            except Exception as e:

                last_error = e

                continue

        raise Exception(

            f"No Market Provider Available: {last_error}"

        )
