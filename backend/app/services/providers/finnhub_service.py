import requests

from app.services.base_market_service import BaseMarketService


class FinnhubService(BaseMarketService):

    BASE_URL = "https://finnhub.io/api/v1"

    def __init__(self, api_key="YOUR_FINNHUB_API_KEY"):
        self.api_key = api_key

    def get_price(self, symbol="AAPL"):

        response = requests.get(
            f"{self.BASE_URL}/quote",
            params={
                "symbol": symbol,
                "token": self.api_key
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        return {

            "symbol": symbol,

            "price": float(data["c"])

        }

    def get_24h(self, symbol="AAPL"):

        response = requests.get(
            f"{self.BASE_URL}/quote",
            params={
                "symbol": symbol,
                "token": self.api_key
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        return {

            "symbol": symbol,

            "price": float(data["c"]),

            "high": float(data["h"]),

            "low": float(data["l"]),

            "open": float(data["o"]),

            "previous_close": float(data["pc"])

        }

    def get_candles(
        self,
        symbol="AAPL",
        interval="60",
        start=0,
        end=0
    ):

        response = requests.get(
            f"{self.BASE_URL}/stock/candle",
            params={
                "symbol": symbol,
                "resolution": interval,
                "from": start,
                "to": end,
                "token": self.api_key
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        candles = []

        for i in range(len(data["t"])):

            candles.append({

                "time": data["t"][i],

                "open": data["o"][i],

                "high": data["h"][i],

                "low": data["l"][i],

                "close": data["c"][i],

                "volume": data["v"][i]

            })

        return candles
