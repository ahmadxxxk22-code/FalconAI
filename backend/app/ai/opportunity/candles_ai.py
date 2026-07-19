from math import fabs



class CandlesAI:


    def __init__(self):

        self.minimum_candles = 5

        self.volume_weight = 10



    # ==================================================
    # Candle Helpers
    # ==================================================


    def body(self, candle):

        return fabs(
            candle["close"] -
            candle["open"]
        )



    def candle_range(self, candle):

        return (

            candle["high"]
            -
            candle["low"]

        )



    def upper_shadow(self, candle):

        return (

            candle["high"]
            -
            max(
                candle["open"],
                candle["close"]
            )

        )



    def lower_shadow(self, candle):

        return (

            min(
                candle["open"],
                candle["close"]
            )

            -

            candle["low"]

        )



    def bullish(self, candle):

        return (

            candle["close"]
            >
            candle["open"]

        )



    def bearish(self, candle):

        return (

            candle["close"]
            <
            candle["open"]

        )



    def volume_strength(
        self,
        candles
    ):


        volumes = [

            c.get(
                "volume",
                0
            )

            for c in candles

        ]


        if not volumes:

            return 0



        average = sum(
            volumes[:-1]
        ) / max(
            len(volumes)-1,
            1
        )


        current = volumes[-1]


        if average == 0:

            return 0



        ratio = current / average


        if ratio >= 2:

            return self.volume_weight


        if ratio >= 1.5:

            return 5


        return 0



    # ==================================================
    # Pattern Detectors
    # ==================================================


    def detect_hammer(
        self,
        candle
    ):


        body = self.body(candle)

        upper = self.upper_shadow(candle)

        lower = self.lower_shadow(candle)


        return (

            lower > body * 2

            and

            upper < body

        )



    def detect_shooting_star(
        self,
        candle
    ):


        body = self.body(candle)

        upper = self.upper_shadow(candle)

        lower = self.lower_shadow(candle)


        return (

            upper > body * 2

            and

            lower < body

        )



    def detect_inside_bar(
        self,
        previous,
        current
    ):


        return (

            current["high"]
            <
            previous["high"]

            and

            current["low"]
            >
            previous["low"]

        )



    def detect_bullish_engulfing(
        self,
        previous,
        current
    ):


        return (

            self.bearish(previous)

            and

            self.bullish(current)

            and

            current["close"]
            >
            previous["open"]

            and

            current["open"]
            <
            previous["close"]

        )



    def detect_bearish_engulfing(
        self,
        previous,
        current
    ):


        return (

            self.bullish(previous)

            and

            self.bearish(current)

            and

            current["close"]
            <
            previous["open"]

            and

            current["open"]
            >
            previous["close"]

        )



    def detect_morning_star(
        self,
        first,
        second,
        third
    ):


        return (

            self.bearish(first)

            and

            self.body(second)
            <
            self.body(first) * 0.5

            and

            self.bullish(third)

            and

            third["close"]
            >
            (
                first["open"]
                +
                first["close"]
            ) / 2

        )



    def detect_evening_star(
        self,
        first,
        second,
        third
    ):


        return (

            self.bullish(first)

            and

            self.body(second)
            <
            self.body(first) * 0.5

            and

            self.bearish(third)

            and

            third["close"]
            <
            (
                first["open"]
                +
                first["close"]
            ) / 2

        )



    def detect_three_white_soldiers(
        self,
        candles
    ):


        if len(candles) < 3:

            return False


        a = candles[-3]

        b = candles[-2]

        c = candles[-1]


        return (

            self.bullish(a)

            and

            self.bullish(b)

            and

            self.bullish(c)

            and

            b["close"] > a["close"]

            and

            c["close"] > b["close"]

            and

            b["open"] > a["open"]

            and

            c["open"] > b["open"]

        )



    def detect_three_black_crows(
        self,
        candles
    ):


        if len(candles) < 3:

            return False


        a = candles[-3]

        b = candles[-2]

        c = candles[-1]


        return (

            self.bearish(a)

            and

            self.bearish(b)

            and

            self.bearish(c)

            and

            b["close"] < a["close"]

            and

            c["close"] < b["close"]

            and

            b["open"] < a["open"]

            and

            c["open"] < b["open"]

        )



    def calculate_pattern_strength(
        self,
        patterns,
        candles
    ):


        if not patterns:

            return 0



        scores = [

            p.get(
                "score",
                0
            )

            for p in patterns

        ]


        strength = max(scores)


        strength += self.volume_strength(
            candles
        )


        return min(

            strength,

            100

        )



    # ==================================================
    # MAIN ANALYSIS
    # ==================================================


    def analyze(
        self,
        candles
    ):


        if not candles or len(candles) < self.minimum_candles:

            return {

                "pattern": "UNKNOWN",

                "patterns": [],

                "confidence": 0,

                "strength_score": 0,

                "bullish": False,

                "bearish": False,

                "reasons": []

            }



        patterns = []

        reasons = []


        last = candles[-1]

        prev = candles[-2]



        # ======================
        # Basic Patterns
        # ======================


        if self.detect_hammer(last):

            patterns.append({

                "name": "HAMMER",

                "score": 30,

                "bullish": True

            })

            reasons.append(
                "Hammer تشير لاحتمال انعكاس صاعد"
            )



        if self.detect_shooting_star(last):

            patterns.append({

                "name": "SHOOTING_STAR",

                "score": 30,

                "bearish": True

            })

            reasons.append(
                "Shooting Star تشير لاحتمال هبوط"
            )



        if self.detect_bullish_engulfing(
            prev,
            last
        ):

            patterns.append({

                "name": "BULLISH_ENGULFING",

                "score": 40,

                "bullish": True

            })

            reasons.append(
                "ابتلاع شرائي قوي"
            )



        if self.detect_bearish_engulfing(
            prev,
            last
        ):

            patterns.append({

                "name": "BEARISH_ENGULFING",

                "score": 40,

                "bearish": True

            })

            reasons.append(
                "ابتلاع بيعي قوي"
            )



        if self.detect_inside_bar(
            prev,
            last
        ):

            patterns.append({

                "name": "INSIDE_BAR",

                "score": 20

            })

            reasons.append(
                "Inside Bar تدل على ضغط قبل الحركة"
            )



        # ======================
        # Multi Candle Patterns
        # ======================


        if self.detect_morning_star(
            candles[-3],
            candles[-2],
            candles[-1]
        ):

            patterns.append({

                "name": "MORNING_STAR",

                "score": 50,

                "bullish": True

            })

            reasons.append(
                "Morning Star انعكاس صاعد"
            )



        if self.detect_evening_star(
            candles[-3],
            candles[-2],
            candles[-1]
        ):

            patterns.append({

                "name": "EVENING_STAR",

                "score": 50,

                "bearish": True

            })

            reasons.append(
                "Evening Star انعكاس هابط"
            )



        if self.detect_three_white_soldiers(
            candles
        ):

            patterns.append({

                "name": "THREE_WHITE_SOLDIERS",

                "score": 60,

                "bullish": True

            })

            reasons.append(
                "ثلاث شموع صاعدة قوية"
            )



        if self.detect_three_black_crows(
            candles
        ):

            patterns.append({

                "name": "THREE_BLACK_CROWS",

                "score": 60,

                "bearish": True

            })

            reasons.append(
                "ثلاث شموع هابطة قوية"
            )



        # ======================
        # Direction
        # ======================


        bullish = any(

            p.get(
                "bullish",
                False
            )

            for p in patterns

        )


        bearish = any(

            p.get(
                "bearish",
                False
            )

            for p in patterns

        )



        strength = self.calculate_pattern_strength(
            patterns,
            candles
        )



        return {

            "pattern":

            patterns[0]["name"]

            if patterns

            else "NONE",


            "patterns":

            patterns,


            "confidence":

            strength,


            "strength_score":

            strength,


            "bullish":

            bullish,


            "bearish":

            bearish,


            "reasons":

            reasons

            }
