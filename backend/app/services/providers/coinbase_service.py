import requests

from app.services.base_market_service import BaseMarketService


class CoinbaseService(BaseMarketService):

    BASE_URL = "https://api.exchange.coinbase.com"

    def get_price(self, symbol="BTC-USD"):

        response = requests.get(
            f"{self.BASE_URL}/products/{symbol}/ticker",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {

            "symbol": symbol,

            "price": float(data["price"])

        }

    def get_24h(self, symbol="BTC-USD"):

        response = requests.get(
            f"{self.BASE_URL}/products/{symbol}/stats",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {

            "symbol": symbol,

            "price": float(data["last"]),

            "high": float(data["high"]),

            "low": float(data["low"]),

            "volume": float(data["volume"])

        }

    def get_candles(
        self,
        symbol="BTC-USD",
        interval=3600,
        limit=200
    ):

        response = requests.get(
            f"{self.BASE_URL}/products/{symbol}/candles",
            params={"granularity": interval},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        candles = []

        for candle in reversed(data[:limit]):

            candles.append({

                "open_time": candle[0],

                "low": float(candle[1]),

                "high": float(candle[2]),

                "open": float(candle[3]),

                "close": float(candle[4]),

                "volume": float(candle[5]),

                "close_time": candle[0]

            })

        return candles
