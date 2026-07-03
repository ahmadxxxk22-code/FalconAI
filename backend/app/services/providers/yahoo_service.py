import requests


class YahooService:

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

    def get_candles(
        self,
        symbol="AAPL",
        interval="1d"
    ):

        url = f"{self.BASE_URL}/{symbol}"

        params = {
            "interval": self.INTERVALS.get(interval, "1d"),
            "range": self.RANGES.get(interval, "1y")
        }

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        result = data["chart"]["result"][0]

        quote = result["indicators"]["quote"][0]

        timestamps = result["timestamp"]

        candles = []

        for i in range(len(timestamps)):

            if quote["close"][i] is None:
                continue

            candles.append({

                "time": timestamps[i],

                "open": quote["open"][i],

                "high": quote["high"][i],

                "low": quote["low"][i],

                "close": quote["close"][i],

                "volume": quote["volume"][i]

            })

        return candles

    def get_close_prices(
        self,
        symbol="AAPL",
        interval="1d"
    ):

        return [

            candle["close"]

            for candle in self.get_candles(
                symbol,
                interval
            )

        ]

    def get_volumes(
        self,
        symbol="AAPL",
        interval="1d"
    ):

        return [

            candle["volume"]

            for candle in self.get_candles(
                symbol,
                interval
            )

        ]
