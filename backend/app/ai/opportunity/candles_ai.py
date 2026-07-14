class CandlesAI:

    def analyze(self, candles):

        if len(candles) < 3:

            return {

                "pattern": "UNKNOWN",

                "bullish": False,

                "bearish": False,

                "confidence": 0,

                "score": 0

            }

        last = candles[-1]

        previous = candles[-2]

        body = abs(
            last["close"] - last["open"]
        )

        candle_range = (
            last["high"] - last["low"]
        )

        upper_shadow = (
            last["high"] -
            max(last["open"], last["close"])
        )

        lower_shadow = (
            min(last["open"], last["close"]) -
            last["low"]
        )

        pattern = "NONE"

        bullish = False
        bearish = False
        score = 0

        # Hammer
        if (
            lower_shadow > body * 2
            and upper_shadow < body
        ):

            pattern = "HAMMER"

            bullish = True

            score = 25

        # Shooting Star
        elif (
            upper_shadow > body * 2
            and lower_shadow < body
        ):

            pattern = "SHOOTING_STAR"

            bearish = True

            score = 25

        # Bullish Engulfing
        elif (

            previous["close"] < previous["open"]

            and

            last["close"] > last["open"]

            and

            last["close"] > previous["open"]

        ):

            pattern = "BULLISH_ENGULFING"

            bullish = True

            score = 35

        # Bearish Engulfing
        elif (

            previous["close"] > previous["open"]

            and

            last["close"] < last["open"]

            and

            last["close"] < previous["open"]

        ):

            pattern = "BEARISH_ENGULFING"

            bearish = True

            score = 35

        return {

            "pattern": pattern,

            "bullish": bullish,

            "bearish": bearish,

            "confidence": score,

            "score": score

        }
