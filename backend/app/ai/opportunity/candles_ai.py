from math import fabs



class CandlesAI:


    def body(self, candle):

        return fabs(
            candle["close"] -
            candle["open"]
        )



    def candle_range(self, candle):

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



    def analyze(
        self,
        candles
    ):


        if len(candles) < 5:

            return {

                "pattern":"UNKNOWN",

                "patterns":[],

                "confidence":0,

                "bullish":False,

                "bearish":False,

                "reasons":[]

            }



        patterns = []

        reasons = []



        last = candles[-1]

        prev = candles[-2]

        before = candles[-3]



        body = self.body(last)

        rng = self.candle_range(last)

        upper = self.upper_shadow(last)

        lower = self.lower_shadow(last)



        if rng == 0:

            return {

                "pattern":"NONE",

                "patterns":[],

                "confidence":0,

                "bullish":False,

                "bearish":False,

                "reasons":[]

            }



        # ======================
        # Hammer
        # ======================

        if (

            lower > body * 2

            and

            upper < body

        ):


            patterns.append({

                "name":"HAMMER",

                "score":30,

                "bullish":True

            })


            reasons.append(
                "شمعة Hammer تشير لاحتمال انعكاس صاعد"
            )



        # ======================
        # Shooting Star
        # ======================

        if (

            upper > body * 2

            and

            lower < body

        ):


            patterns.append({

                "name":"SHOOTING_STAR",

                "score":30,

                "bearish":True

            })


            reasons.append(
                "شمعة Shooting Star تشير لاحتمال هبوط"
            )



        # ======================
        # Bullish Engulfing
        # ======================

        if (

            self.bearish(prev)

            and

            self.bullish(last)

            and

            last["close"] > prev["open"]

        ):


            patterns.append({

                "name":"BULLISH_ENGULFING",

                "score":40,

                "bullish":True

            })


            reasons.append(
                "ابتلاع شرائي قوي"
            )



        # ======================
        # Bearish Engulfing
        # ======================


        if (

            self.bullish(prev)

            and

            self.bearish(last)

            and

            last["close"] < prev["open"]

        ):


            patterns.append({

                "name":"BEARISH_ENGULFING",

                "score":40,

                "bearish":True

            })


            reasons.append(
                "ابتلاع بيعي قوي"
            )



        # ======================
        # Morning Star
        # ======================


        if (

            self.bearish(before)

            and

            abs(
                self.body(prev)
            )
            <
            self.body(before)*0.5

            and

            self.bullish(last)

            and

            last["close"] >
            (
                before["open"]
                +
                before["close"]
            )/2

        ):


            patterns.append({

                "name":"MORNING_STAR",

                "score":50,

                "bullish":True

            })


            reasons.append(
                "نموذج Morning Star انعكاسي صاعد"
            )



        # ======================
        # Evening Star
        # ======================


        if (

            self.bullish(before)

            and

            self.body(prev)
            <
            self.body(before)*0.5

            and

            self.bearish(last)

            and

            last["close"]
            <
            (
                before["open"]
                +
                before["close"]
            )/2

        ):


            patterns.append({

                "name":"EVENING_STAR",

                "score":50,

                "bearish":True

            })


            reasons.append(
                "نموذج Evening Star انعكاسي هابط"
            )



        # ======================
        # Doji
        # ======================


        if body <= rng*0.1:


            patterns.append({

                "name":"DOJI",

                "score":15

            })


            reasons.append(
                "شمعة حيرة في السوق"
            )



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



        confidence = 0


        if patterns:

            confidence = max(

                p["score"]

                for p in patterns

            )



        return {


            "pattern":

            patterns[0]["name"]

            if patterns

            else "NONE",


            "patterns":

            patterns,


            "confidence":

            confidence,


            "bullish":

            bullish,


            "bearish":

            bearish,


            "reasons":

            reasons

            }
