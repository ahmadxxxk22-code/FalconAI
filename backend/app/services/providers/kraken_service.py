import requests

from app.services.base_market_service import BaseMarketService


class KrakenService(BaseMarketService):

    BASE_URL = "https://api.kraken.com/0/public"

    INTERVALS = {
        "1m": 1,
        "5m": 5,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "4h": 240,
        "1d": 1440
    }

    SYMBOLS = {
        "BTCUSDT": "XBTUSDT",
        "ETHUSDT": "ETHUSDT"
    }

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

            raise Exception(f"Kraken API Error: {e}")

    def get_price(self, symbol="BTCUSDT"):

        pair = self.SYMBOLS.get(symbol, symbol)

        data = self.request(

            "Ticker",

            {"pair": pair}

        )

        if data["error"]:
            raise Exception(str(data["error"]))

        ticker = list(data["result"].values())[0]

        return {

            "symbol": pair,

            "price": float(ticker["c"][0])

        }

    def get_24h(self, symbol="BTCUSDT"):

        pair = self.SYMBOLS.get(symbol, symbol)

        data = self.request(

            "Ticker",

            {"pair": pair}

        )

        if data["error"]:
            raise Exception(str(data["error"]))

        ticker = list(data["result"].values())[0]

        return {

            "symbol": pair,

            "price": float(ticker["c"][0]),

            "high": float(ticker["h"][1]),

            "low": float(ticker["l"][1]),

            "volume": float(ticker["v"][1])

        }

    def get_candles(

        self,

        symbol="BTCUSDT",

        interval="1h",

        limit=200

    ):

        pair = self.SYMBOLS.get(symbol, symbol)

        data = self.request(

            "OHLC",

            {

                "pair": pair,

                "interval": self.INTERVALS.get(interval, 60)

            }

        )

        if data["error"]:
            raise Exception(str(data["error"]))

        result = list(data["result"].values())[0]

        candles = []

        for row in result[-limit:]:

            candles.append({

                "open_time": int(row[0]),

                "open": float(row[1]),

                "high": float(row[2]),

                "low": float(row[3]),

                "close": float(row[4]),

                "volume": float(row[6]),

                "close_time": int(row[0])

            })

        return candles
