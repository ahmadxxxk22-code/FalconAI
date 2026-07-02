import requests


class MarketData:

    def get_binance_candles(self, symbol="BTCUSDT", interval="1m", limit=50):

        url = "https://api.binance.com/api/v3/klines"

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        response = requests.get(url, params=params)
        data = response.json()

        prices = []

        for candle in data:
            close_price = float(candle[4])  # سعر الإغلاق
            prices.append(close_price)

        return prices
