from app.services.market_data import MarketData


class PatternAnalyzer:

    def __init__(self):

        self.market = MarketData()


    # ==================================================
    # MAIN ANALYSIS
    # ==================================================

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


        if not candles or len(candles) < 5:

            return {

                "pattern": "NONE",
                "bullish": False,
                "bearish": False,
                "strength": 0,
                "confidence": 0,
                "reasons": [
                    "Not enough candles"
                ]

            }


        bullish = False
        bearish = False

        pattern = "NONE"

        strength = 0

        reasons = []


        # ==========================
        # Bullish Patterns
        # ==========================


        if self.bullish_engulfing(candles):

            bullish = True

            pattern = "Bullish Engulfing"

            strength = 85

            reasons.append(
                "ابتلاع شرائي قوي"
            )


        elif self.hammer(candles[-1]):

            bullish = True

            pattern = "Hammer"

            strength = 75

            reasons.append(
                "شمعة انعكاس صاعدة"
            )


        elif self.morning_star(candles):

            bullish = True

            pattern = "Morning Star"

            strength = 90

            reasons.append(
                "نموذج انعكاس صاعد قوي"
            )



        # ==========================
        # Bearish Patterns
        # ==========================

        elif self.bearish_engulfing(candles):

            bearish = True

            pattern = "Bearish Engulfing"

            strength = 85

            reasons.append(
                "ابتلاع بيعي قوي"
            )


        elif self.shooting_star(candles[-1]):

            bearish = True

            pattern = "Shooting Star"

            strength = 75

            reasons.append(
                "شمعة رفض صاعدة وانعكاس هابط"
            )


        elif self.evening_star(candles):

            bearish = True

            pattern = "Evening Star"

            strength = 90

            reasons.append(
                "نموذج انعكاس هابط قوي"
            )


        # ==========================
        # Neutral Patterns
        # ==========================

        elif self.inside_bar(candles):

            pattern = "Inside Bar"

            strength = 50

            reasons.append(
                "ضغط سعري قبل الحركة"
            )


        elif self.doji(candles[-1]):

            pattern = "Doji"

            strength = 40

            reasons.append(
                "تردد بالسوق"
            )


        confidence = min(
            strength,
            100
        )


        return {

            "pattern": pattern,

            "bullish": bullish,

            "bearish": bearish,

            "strength": strength,

            "confidence": confidence,

            "reasons": reasons

        }


    # ==================================================
    # Bullish Engulfing
    # ==================================================

    def bullish_engulfing(
        self,
        candles
    ):

        prev = candles[-2]

        curr = candles[-1]


        return (

            prev["close"] < prev["open"]

            and

            curr["close"] > curr["open"]

            and

            curr["open"] <= prev["close"]

            and

            curr["close"] >= prev["open"]

        )


    # ==================================================
    # Bearish Engulfing
    # ==================================================

    def bearish_engulfing(
        self,
        candles
    ):

        prev = candles[-2]

        curr = candles[-1]


        return (

            prev["close"] > prev["open"]

            and

            curr["close"] < curr["open"]

            and

            curr["open"] >= prev["close"]

            and

            curr["close"] <= prev["open"]

        )



    # ==================================================
    # Hammer
    # ==================================================

    def hammer(
        self,
        candle
    ):

        body = abs(
            candle["close"] -
            candle["open"]
        )

        lower_wick = min(
            candle["open"],
            candle["close"]
        ) - candle["low"]


        upper_wick = (
            candle["high"]
            -
            max(
                candle["open"],
                candle["close"]
            )
        )


        return (

            lower_wick > body * 2

            and

            upper_wick < body

        )


    # ==================================================
    # Shooting Star
    # ==================================================

    def shooting_star(
        self,
        candle
    ):

        body = abs(
            candle["close"]
            -
            candle["open"]
        )


        upper_wick = (
            candle["high"]
            -
            max(
                candle["open"],
                candle["close"]
            )
        )


        lower_wick = min(
            candle["open"],
            candle["close"]
        ) - candle["low"]


        return (

            upper_wick > body * 2

            and

            lower_wick < body

        )


    # ==================================================
    # Morning Star
    # ==================================================

    def morning_star(
        self,
        candles
    ):

        if len(candles) < 3:

            return False


        first = candles[-3]

        second = candles[-2]

        third = candles[-1]


        return (

            first["close"] < first["open"]

            and

            abs(
                second["close"]
                -
                second["open"]
            )

            <
            abs(
                first["close"]
                -
                first["open"]
            )
            *

            0.5

            and

            third["close"] > third["open"]

            and

            third["close"] >
            (
                first["open"]
                +
                first["close"]
            )
            /
            2

        )


    # ==================================================
    # Evening Star
    # ==================================================

    def evening_star(
        self,
        candles
    ):

        if len(candles) < 3:

            return False


        first = candles[-3]

        second = candles[-2]

        third = candles[-1]


        return (

            first["close"] > first["open"]

            and

            abs(
                second["close"]
                -
                second["open"]
            )

            <
            abs(
                first["close"]
                -
                first["open"]
            )
            *

            0.5

            and

            third["close"] < third["open"]

            and

            third["close"] <
            (
                first["open"]
                +
                first["close"]
            )
            /
            2

        )



# ==================================================
# Inside Bar
# ==================================================

    def inside_bar(
        self,
        candles
    ):

        if len(candles) < 2:

            return False


        prev = candles[-2]

        curr = candles[-1]


        return (

            curr["high"] < prev["high"]

            and

            curr["low"] > prev["low"]

        )


# ==================================================
# Doji
# ==================================================

    def doji(
        self,
        candle
    ):

        body = abs(
            candle["close"]
            -
            candle["open"]
        )


        range_size = (

            candle["high"]
            -
            candle["low"]

        )


        if range_size == 0:

            return False


        return (

            body / range_size

        ) < 0.10
