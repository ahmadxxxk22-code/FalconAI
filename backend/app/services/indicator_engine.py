import math


class IndicatorEngine:

    # ==========================
    # EMA
    # ==========================
    def ema(self, prices, period=20):

        if len(prices) < period:
            return prices[-1]

        multiplier = 2 / (period + 1)

        ema = sum(prices[:period]) / period

        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema

        return round(ema, 2)

    # ==========================
    # SMA
    # ==========================
    def sma(self, prices, period=20):

        if len(prices) < period:
            return prices[-1]

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

            if diff > 0:
                gains.append(diff)
            else:
                losses.append(abs(diff))

        avg_gain = (
            sum(gains[-period:]) / period
            if gains else 0.0001
        )

        avg_loss = (
            sum(losses[-period:]) / period
            if losses else 0.0001
        )

        rs = avg_gain / avg_loss

        return round(
            100 - (100 / (1 + rs)),
            2
        )

    # ==========================
    # MACD
    # ==========================
    def macd(self, prices):

        ema12 = self.ema(prices, 12)
        ema26 = self.ema(prices, 26)

        return round(
            ema12 - ema26,
            2
        )

    # ==========================
    # Trend Strength
    # ==========================
    def trend_strength(self, prices):

        if len(prices) < 20:
            return 0

        first = prices[-20]

        last = prices[-1]

        return round(
            ((last - first) / first) * 100,
            2
        )

    # ==========================
    # Volatility
    # ==========================
    def volatility(self, prices):

        avg = sum(prices) / len(prices)

        variance = sum(
            (x - avg) ** 2
            for x in prices
        ) / len(prices)

        return round(
            math.sqrt(variance),
            2
        )
