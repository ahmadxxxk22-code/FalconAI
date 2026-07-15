from math import fabs


class CandlesAI:

    def __init__(self):
        pass

    def body(self, candle):
        return fabs(candle["close"] - candle["open"])

    def range(self, candle):
        return candle["high"] - candle["low"]

    def upper_shadow(self, candle):
        return candle["high"] - max(
            candle["open"],
            candle["close"]
        )

    def lower_shadow(self, candle):
        return min(
            candle["open"],
            candle["close"]
        ) - candle["low"]

    def bullish(self, candle):
        return candle["close"] > candle["open"]

    def bearish(self, candle):
        return candle["close"] < candle["open"]

    def analyze(self, candles):

        if len(candles) < 5:

            return {

                "pattern": "UNKNOWN",

                "confidence": 0,

                "bullish": False,

                "bearish": False,

                "patterns": []

            }

        patterns = []

        last = candles[-1]
        prev = candles[-2]

        b = self.body(last)

        u = self.upper_shadow(last)

        l = self.lower_shadow(last)

        # Hammer

        if l > b * 2 and u < b:

            patterns.append({

                "name": "HAMMER",

                "score": 25,

                "bullish": True

            })

        # Inverted Hammer

        if u > b * 2 and l < b:

            patterns.append({

                "name": "INVERTED_HAMMER",

                "score": 20,

                "bullish": True

            })

        # Hanging Man

        if (

            self.bullish(prev)

            and

            l > b * 2

        ):

            patterns.append({

                "name": "HANGING_MAN",

                "score": 25,

                "bearish": True

            })

        # Shooting Star

        if (

            self.bearish(last)

            and

            u > b * 2

        ):

            patterns.append({

                "name": "SHOOTING_STAR",

                "score": 25,

                "bearish": True

            })

        # Bullish Engulfing

        if (

            self.bearish(prev)

            and

            self.bullish(last)

            and

            last["close"] > prev["open"]

        ):

            patterns.append({

                "name": "BULLISH_ENGULFING",

                "score": 35,

                "bullish": True

            })

        # Bearish Engulfing

        if (

            self.bullish(prev)

            and

            self.bearish(last)

            and

            last["close"] < prev["open"]

        ):

            patterns.append({

                "name": "BEARISH_ENGULFING",

                "score": 35,

                "bearish": True

            })

        # Doji

        if b <= self.range(last) * 0.1:

            patterns.append({

                "name": "DOJI",

                "score": 15

            })

        bullish = any(
            p.get("bullish", False)
            for p in patterns
        )

        bearish = any(
            p.get("bearish", False)
            for p in patterns
        )

        confidence = 0

        if patterns:

            confidence = max(
                p["score"]
                for p in patterns
            )

        return {

            "pattern": (
                patterns[0]["name"]
                if patterns
                else "NONE"
            ),

            "patterns": patterns,

            "confidence": confidence,

            "bullish": bullish,

            "bearish": bearish

        }
