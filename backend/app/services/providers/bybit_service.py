import requests

from app.services.base_market_service import BaseMarketService


class BybitService(BaseMarketService):

    BASE_URL = "https://api.bybit.com/v5"

    def get_price(self, symbol="BTCUSDT"):

        response = requests.get(
            f"{self.BASE_URL}/market/tickers",
            params={
                "category": "linear",
                "symbol": symbol
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()["result"]["list"][0]

        return {

            "symbol": data["symbol"],

            "price": float(data["lastPrice"])

        }

    def get_24h(self, symbol="BTCUSDT"):

        response = requests.get(
            f"{self.BASE_URL}/market/tickers",
            params={
                "category": "linear",
                "symbol": symbol
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()["result"]["list"][0]

        return {

            "symbol": data["symbol"],

            "price": float(data["lastPrice"]),

            "change": float(data["price24hPcnt"]) * 100,

            "high": float(data["highPrice24h"]),

            "low": float(data["lowPrice24h"]),

            "volume": float(data["volume24h"])

        }

    def get_candles(

        self,

        symbol="BTCUSDT",

        interval="60",

        limit=200

    ):

        response = requests.get(

            f"{self.BASE_URL}/market/kline",

            params={

                "category": "linear",

                "symbol": symbol,

                "interval": interval,

                "limit": limit

            },

            timeout=10

        )

        response.raise_for_status()

        data = response.json()["result"]["list"]

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
