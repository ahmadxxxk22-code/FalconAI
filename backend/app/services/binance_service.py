import requests

from app.services.base_market_service import BaseMarketService


class BinanceService(BaseMarketService):

    BASE_URL = "https://api.binance.com/api/v3"

    def get_price(self, symbol="BTCUSDT"):

        response = requests.get(
            f"{self.BASE_URL}/ticker/price",
            params={"symbol": symbol},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {
            "symbol": data["symbol"],
            "price": float(data["price"])
        }

    def get_24h(self, symbol="BTCUSDT"):

        response = requests.get(
            f"{self.BASE_URL}/ticker/24hr",
            params={"symbol": symbol},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {

            "symbol": data["symbol"],

            "price": float(data["lastPrice"]),

            "change": float(data["priceChangePercent"]),

            "high": float(data["highPrice"]),

            "low": float(data["lowPrice"]),

            "volume": float(data["volume"])

        }

    def get_candles(
        self,
        symbol="BTCUSDT",
        interval="1h",
        limit=200
    ):

        response = requests.get(
            f"{self.BASE_URL}/klines",
            params={
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        candles = []

        for candle in data:

            candles.append({

                "open_time": candle[0],

                "open": float(candle[1]),

                "high": float(candle[2]),

                "low": float(candle[3]),

                "close": float(candle[4]),

                "volume": float(candle[5]),

                "close_time": candle[6]

            })

        return candles
