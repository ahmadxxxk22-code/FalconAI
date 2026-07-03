import requests

from app.services.base_market_service import BaseMarketService


class OKXService(BaseMarketService):

    BASE_URL = "https://www.okx.com/api/v5"

    def get_price(self, symbol="BTC-USDT"):

        response = requests.get(
            f"{self.BASE_URL}/market/ticker",
            params={"instId": symbol},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()["data"][0]

        return {

            "symbol": data["instId"],

            "price": float(data["last"])

        }

    def get_24h(self, symbol="BTC-USDT"):

        response = requests.get(
            f"{self.BASE_URL}/market/ticker",
            params={"instId": symbol},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()["data"][0]

        return {

            "symbol": data["instId"],

            "price": float(data["last"]),

            "change": float(data["sodUtc0"]),

            "high": float(data["high24h"]),

            "low": float(data["low24h"]),

            "volume": float(data["vol24h"])

        }

    def get_candles(
        self,
        symbol="BTC-USDT",
        interval="1H",
        limit=200
    ):

        response = requests.get(
            f"{self.BASE_URL}/market/candles",
            params={
                "instId": symbol,
                "bar": interval,
                "limit": limit
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()["data"]

        candles = []

        for candle in reversed(data):

            candles.append({

                "open_time": int(candle[0]),

                "open": float(candle[1]),

                "high": float(candle[2]),

                "low": float(candle[3]),

                "close": float(candle[4]),

                "volume": float(candle[5]),

                "close_time": int(candle[0])

            })

        return candles
