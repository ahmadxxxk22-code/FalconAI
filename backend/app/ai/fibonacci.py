from app.services.market_data import MarketData


class FibonacciAnalyzer:

    def __init__(self):
        self.market = MarketData()

    def analyze(self, symbol="BTCUSDT", interval="1h"):

        candles = self.market.get_candles(
            symbol=symbol,
            interval=interval,
            limit=200
        )

        high = max(c["high"] for c in candles)
        low = min(c["low"] for c in candles)
        current_price = candles[-1]["close"]

        diff = high - low

        levels = {
            "0.236": high - diff * 0.236,
            "0.382": high - diff * 0.382,
            "0.500": high - diff * 0.500,
            "0.618": high - diff * 0.618,
            "0.786": high - diff * 0.786,
        }

        nearest = min(
            levels,
            key=lambda x: abs(levels[x] - current_price)
        )

        bullish = current_price <= levels["0.618"]
        bearish = current_price >= levels["0.236"]

        signal = "WAIT"

        if bullish:
            signal = "BUY"

        elif bearish:
            signal = "SELL"

        return {
            "signal": signal,
            "bullish": bullish,
            "bearish": bearish,
            "levels": levels,
            "nearest_level": nearest,
            "price": current_price
        }
