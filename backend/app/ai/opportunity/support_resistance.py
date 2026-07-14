import numpy as np


class SupportResistanceEngine:

    def __init__(self, window=5):
        self.window = window

    def analyze(self, highs, lows, closes):

        if len(highs) < self.window * 2:
            return {
                "supports": [],
                "resistances": [],
                "nearest_support": None,
                "nearest_resistance": None
            }

        supports = []
        resistances = []

        for i in range(self.window, len(lows) - self.window):

            current_low = lows[i]

            if current_low == min(
                lows[i - self.window:i + self.window + 1]
            ):
                supports.append(float(current_low))

        for i in range(self.window, len(highs) - self.window):

            current_high = highs[i]

            if current_high == max(
                highs[i - self.window:i + self.window + 1]
            ):
                resistances.append(float(current_high))

        supports = sorted(list(set(supports)))
        resistances = sorted(list(set(resistances)))

        current_price = float(closes[-1])

        nearest_support = None
        nearest_resistance = None

        lower = [s for s in supports if s <= current_price]
        upper = [r for r in resistances if r >= current_price]

        if lower:
            nearest_support = max(lower)

        if upper:
            nearest_resistance = min(upper)

        return {

            "supports": supports,

            "resistances": resistances,

            "nearest_support": nearest_support,

            "nearest_resistance": nearest_resistance

        }
