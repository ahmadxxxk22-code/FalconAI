import numpy as np


class IndicatorEngine:

    def rsi(self, prices, period: int = 14):
        if len(prices) < period + 1:
            return 50

        gains = []
        losses = []

        for i in range(1, len(prices)):
            change = prices[i] - prices[i - 1]

            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return round(rsi, 2)


    def ema(self, prices, period: int = 14):
        if len(prices) < period:
            return sum(prices) / len(prices)

        alpha = 2 / (period + 1)
        ema = prices[0]

        for price in prices[1:]:
            ema = (price * alpha) + (ema * (1 - alpha))

        return round(ema, 2)


    def trend_strength(self, prices):
        if len(prices) < 2:
            return 50

        changes = np.diff(prices)
        strength = np.mean(np.abs(changes))

        return round(min(strength * 10, 100), 2)
