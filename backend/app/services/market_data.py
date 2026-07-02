import requests


class MarketData:

    BINANCE_URL = "https://api.binance.com/api/v3/klines"

    def get_candles(
        self,
        symbol="BTCUSDT",
        interval="1m",
        limit=100
    ):

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        response = requests.get(
            self.BINANCE_URL,
            params=params,
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


    def get_close_prices(
        self,
        symbol="BTCUSDT",
        interval="1m",
        limit=100
    ):

        candles = self.get_candles(
            symbol,
            interval,
            limit
        )

        return [
            c["close"]
            for c in candles
        ]


    def get_volumes(
        self,
        symbol="BTCUSDT",
        interval="1m",
        limit=100
    ):

        candles = self.get_candles(
            symbol,
            interval,
            limit
        )

        return [
            c["volume"]
            for c in candles
        ]
