import requests


class KrakenService:

    BASE_URL = "https://api.kraken.com/0/public/OHLC"

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

    def get_candles(
        self,
        symbol="BTCUSDT",
        interval="1h"
    ):

        pair = self.SYMBOLS.get(symbol, symbol)

        params = {
            "pair": pair,
            "interval": self.INTERVALS.get(interval, 60)
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data["error"]:
            raise Exception(str(data["error"]))

        result = list(data["result"].values())[0]

        candles = []

        for row in result:

            candles.append({
                "time": int(row[0]),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[6])
            })

        return candles


    def get_close_prices(
        self,
        symbol="BTCUSDT",
        interval="1h"
    ):

        return [
            c["close"]
            for c in self.get_candles(symbol, interval)
        ]


    def get_volumes(
        self,
        symbol="BTCUSDT",
        interval="1h"
    ):

        return [
            c["volume"]
            for c in self.get_candles(symbol, interval)
        ]
