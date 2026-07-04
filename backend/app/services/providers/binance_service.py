import requests

from app.services.base_market_service import BaseMarketService


class BinanceService(BaseMarketService):

    BASE_URL = "https://api.binance.com/api/v3"

    def request(self, endpoint, params=None):

        try:

            response = requests.get(

                f"{self.BASE_URL}/{endpoint}",

                params=params,

                timeout=10

            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:

            raise Exception(

                f"Binance API Error: {e}"

            )

    def get_price(self, symbol="BTCUSDT"):

        data = self.request(

            "ticker/price",

            {"symbol": symbol}

        )

        return {

            "symbol": data["symbol"],

            "price": float(data["price"])

        }

    def get_24h(self, symbol="BTCUSDT"):

        data = self.request(

            "ticker/24hr",

            {"symbol": symbol}

        )

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

        data = self.request(

            "klines",

            {

                "symbol": symbol,

                "interval": interval,

                "limit": limit

            }

        )

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
