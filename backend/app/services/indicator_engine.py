import math


class IndicatorEngine:

    # ==========================
    # EMA
    # ==========================
    def ema(self, prices, period=20):

        if not prices:
            return 0

        if len(prices) < period:
            return round(prices[-1], 2)

        multiplier = 2 / (period + 1)

        ema = sum(prices[:period]) / period

        for price in prices[period:]:

            ema = (price - ema) * multiplier + ema

        return round(ema, 2)

    # ==========================
    # SMA
    # ==========================
    def sma(self, prices, period=20):

        if not prices:
            return 0

        if len(prices) < period:
            return round(prices[-1], 2)

        return round(

            sum(prices[-period:]) / period,

            2

        )

    # ==========================
    # RSI
    # ==========================
    def rsi(self, prices, period=14):

        if len(prices) <= period:
            return 50

        gains = []
        losses = []

        for i in range(1, len(prices)):

            diff = prices[i] - prices[i - 1]

            if diff >= 0:

                gains.append(diff)

                losses.append(0)

            else:

                gains.append(0)

                losses.append(abs(diff))

        avg_gain = sum(gains[-period:]) / period

        avg_loss = sum(losses[-period:]) / period

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return round(rsi, 2)

    # ==========================
    # MACD
    # ==========================
    def macd(self, prices):

        ema12 = self.ema(prices, 12)

        ema26 = self.ema(prices, 26)

        macd = ema12 - ema26

        return round(macd, 2)

    # ==========================
    # Trend Strength
    # ==========================
    def trend_strength(self, prices):

        if len(prices) < 20:
            return 0

        first = prices[-20]

        last = prices[-1]

        if first == 0:
            return 0

        trend = ((last - first) / first) * 100

        return round(trend, 2)

    # ==========================
    # Volatility
    # ==========================
    def volatility(self, prices):

        if not prices:
            return 0

        avg = sum(prices) / len(prices)

        variance = sum(

            (x - avg) ** 2

            for x in prices

        ) / len(prices)

        return round(

            math.sqrt(variance),

            2

        )

    # ==========================
    # ATR
    # ==========================
    def atr(self, candles, period=14):

        if len(candles) < period + 1:
            return 0

        trs = []

        for i in range(1, len(candles)):

            high = candles[i]["high"]

            low = candles[i]["low"]

            prev_close = candles[i - 1]["close"]

            tr = max(

                high - low,

                abs(high - prev_close),

                abs(low - prev_close)

            )

            trs.append(tr)

        return round(

            sum(trs[-period:]) / period,

            4

        )

    # ==========================
    # Momentum
    # ==========================
    def momentum(self, prices, period=10):

        if len(prices) <= period:
            return 0

        return round(

            prices[-1] - prices[-period],

            4

        )
