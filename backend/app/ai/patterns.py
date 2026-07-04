from app.services.market_data import MarketData


class PatternAnalyzer:

    def __init__(self):

        self.market = MarketData()

    def analyze(
        self,
        symbol="BTCUSDT",
        interval="1h"
    ):

        candles = self.market.get_candles(
            symbol=symbol,
            interval=interval,
            limit=100
        )

        bullish = False
        bearish = False

        pattern = "NONE"

        strength = 0

        if self.bullish_engulfing(candles):

            bullish = True

            pattern = "Bullish Engulfing"

            strength = 80

        elif self.bearish_engulfing(candles):

            bearish = True

            pattern = "Bearish Engulfing"

            strength = 80

        elif self.doji(candles[-1]):

            pattern = "Doji"

            strength = 40

        return {

            "pattern": pattern,

            "bullish": bullish,

            "bearish": bearish,

            "strength": strength

        }

    def bullish_engulfing(self, candles):

        if len(candles) < 2:
            return False

        prev = candles[-2]

        curr = candles[-1]

        return (

            prev["close"] < prev["open"]

            and

            curr["close"] > curr["open"]

            and

            curr["close"] > prev["open"]

        )

    def bearish_engulfing(self, candles):

        if len(candles) < 2:
            return False

        prev = candles[-2]

        curr = candles[-1]

        return (

            prev["close"] > prev["open"]

            and

            curr["close"] < curr["open"]

            and

            curr["close"] < prev["open"]

        )

    def doji(self, candle):

        body = abs(

            candle["close"]

            -

            candle["open"]

        )

        return body < (

            candle["high"]

            -

            candle["low"]

        ) * 0.10
