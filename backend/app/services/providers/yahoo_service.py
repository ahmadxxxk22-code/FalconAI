import requests

from app.services.base_market_service import BaseMarketService


class YahooService(BaseMarketService):

    BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart"

    INTERVALS = {
        "1m": "1m",
        "2m": "2m",
        "5m": "5m",
        "15m": "15m",
        "30m": "30m",
        "1h": "60m",
        "1d": "1d"
    }

    RANGES = {
        "1m": "7d",
        "2m": "30d",
        "5m": "60d",
        "15m": "60d",
        "30m": "60d",
        "1h": "730d",
        "1d": "10y"
    }

    def request(self, symbol, interval="1d"):

        response = requests.get(

            f"{self.BASE_URL}/{symbol}",

            params={

                "interval": self.INTERVALS.get(interval, "1d"),

                "range": self.RANGES.get(interval, "1y")

            },

            timeout=10

        )

        response.raise_for_status()

        return response.json()

    def get_price(self, symbol="AAPL"):

        data = self.request(symbol)

        result = data["chart"]["result"][0]

        quote = result["indicators"]["quote"][0]

        price = quote["close"][-1]

        return {

            "symbol": symbol,

            "price": float(price)

        }

    def get_24h(self, symbol="AAPL"):

        data = self.request(symbol)

        result = data["chart"]["result"][0]

        quote = result["indicators"]["quote"][0]

        return {

            "symbol": symbol,

            "price": float(quote["close"][-1]),

            "high": float(max(quote["high"])),

            "low": float(min(quote["low"])),

            "volume": float(quote["volume"][-1])

        }

    def get_candles(

        self,

        symbol="AAPL",

        interval="1d",

        limit=200

    ):

        data = self.request(symbol, interval)

        result = data["chart"]["result"][0]

        quote = result["indicators"]["quote"][0]

        timestamps = result["timestamp"]

        candles = []

        for i in range(len(timestamps)):

            if quote["close"][i] is None:
                continue

            candles.append({

                "open_time": timestamps[i],

                "open": float(quote["open"][i]),

                "high": float(quote["high"][i]),

                "low": float(quote["low"][i]),

                "close": float(quote["close"][i]),

                "volume": float(quote["volume"][i]),

                "close_time": timestamps[i]

            })

        return candles[-limit:]
