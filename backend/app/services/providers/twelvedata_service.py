import requests

from app.services.base_market_service import BaseMarketService


class TwelveDataService(BaseMarketService):

    BASE_URL = "https://api.twelvedata.com"

    def __init__(self, api_key="YOUR_TWELVEDATA_API_KEY"):
        self.api_key = api_key

    def get_price(self, symbol="EUR/USD"):

        response = requests.get(
            f"{self.BASE_URL}/price",
            params={
                "symbol": symbol,
                "apikey": self.api_key
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        return {

            "symbol": symbol,

            "price": float(data["price"])

        }

    def get_24h(self, symbol="EUR/USD"):

        response = requests.get(
            f"{self.BASE_URL}/quote",
            params={
                "symbol": symbol,
                "apikey": self.api_key
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        return {

            "symbol": symbol,

            "price": float(data["close"]),

            "high": float(data["high"]),

            "low": float(data["low"]),

            "open": float(data["open"]),

            "change": float(data["percent_change"])

        }

    def get_candles(

        self,

        symbol="EUR/USD",

        interval="1h",

        limit=200

    ):

        response = requests.get(

            f"{self.BASE_URL}/time_series",

            params={

                "symbol": symbol,

                "interval": interval,

                "outputsize": limit,

                "apikey": self.api_key

            },

            timeout=15

        )

        response.raise_for_status()

        data = response.json()["values"]

        candles = []

        for candle in reversed(data):

            candles.append({

                "time": candle["datetime"],

                "open": float(candle["open"]),

                "high": float(candle["high"]),

                "low": float(candle["low"]),

                "close": float(candle["close"]),

                "volume": float(candle.get("volume", 0))

            })

        return candles
