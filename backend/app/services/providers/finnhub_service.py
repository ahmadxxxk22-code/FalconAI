import time
import requests

from app.services.base_market_service import BaseMarketService


class FinnhubService(BaseMarketService):

    BASE_URL = "https://finnhub.io/api/v1"

    def __init__(self, api_key="YOUR_FINNHUB_API_KEY"):

        self.api_key = api_key

    def request(self, endpoint, params=None):

        if params is None:
            params = {}

        params["token"] = self.api_key

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

                f"Finnhub API Error: {e}"

            )

    def get_price(self, symbol="AAPL"):

        data = self.request(

            "quote",

            {

                "symbol": symbol

            }

        )

        return {

            "symbol": symbol,

            "price": float(data["c"])

        }

    def get_24h(self, symbol="AAPL"):

        data = self.request(

            "quote",

            {

                "symbol": symbol

            }

        )

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

        limit=200

    ):

        end = int(time.time())

        start = end - (limit * 3600)

        data = self.request(

            "stock/candle",

            {

                "symbol": symbol,

                "resolution": interval,

                "from": start,

                "to": end

            }

        )

        candles = []

        if data.get("s") != "ok":

            return candles

        for i in range(len(data["t"])):

            candles.append({

                "open_time": data["t"][i],

                "open": float(data["o"][i]),

                "high": float(data["h"][i]),

                "low": float(data["l"][i]),

                "close": float(data["c"][i]),

                "volume": float(data["v"][i]),

                "close_time": data["t"][i]

            })

        return candles
