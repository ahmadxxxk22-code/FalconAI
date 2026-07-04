import requests

from app.services.base_market_service import BaseMarketService


class TwelveDataService(BaseMarketService):

    BASE_URL = "https://api.twelvedata.com"

    def __init__(self, api_key="YOUR_TWELVEDATA_API_KEY"):

        self.api_key = api_key

    def request(self, endpoint, params=None):

        if params is None:
            params = {}

        params["apikey"] = self.api_key

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

                f"TwelveData API Error: {e}"

            )

    def get_price(self, symbol="EUR/USD"):

        data = self.request(

            "price",

            {

                "symbol": symbol

            }

        )

        return {

            "symbol": symbol,

            "price": float(data["price"])

        }

    def get_24h(self, symbol="EUR/USD"):

        data = self.request(

            "quote",

            {

                "symbol": symbol

            }

        )

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

        data = self.request(

            "time_series",

            {

                "symbol": symbol,

                "interval": interval,

                "outputsize": limit

            }

        )

        candles = []

        values = data.get("values", [])

        for candle in reversed(values):

            candles.append({

                "open_time": candle["datetime"],

                "open": float(candle["open"]),

                "high": float(candle["high"]),

                "low": float(candle["low"]),

                "close": float(candle["close"]),

                "volume": float(candle.get("volume", 0)),

                "close_time": candle["datetime"]

            })

        return candles
