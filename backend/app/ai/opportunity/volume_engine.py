class VolumeEngine:


    def analyze(
        self,
        candles
    ):

        if len(candles) < 30:

            return {

                "volume_state": "UNKNOWN",

                "score": 0,

                "confidence": 0,

                "high_volume": False,

                "low_volume": False,

                "volume_spike": False,

                "accumulation": False,

                "distribution": False,

                "reasons": []

            }


        volumes = [

            candle["volume"]

            for candle in candles

        ]


        closes = [

            candle["close"]

            for candle in candles

        ]


        current_volume = volumes[-1]


        avg_20 = sum(
            volumes[-21:-1]
        ) / 20


        avg_50 = sum(
            volumes[-51:-1]
        ) / 50



        ratio_20 = (

            current_volume / avg_20

            if avg_20 > 0

            else 0

        )


        ratio_50 = (

            current_volume / avg_50

            if avg_50 > 0

            else 0

        )


        score = 0

        reasons = []


        volume_spike = False

        accumulation = False

        distribution = False



        # حجم قوي مفاجئ

        if ratio_20 >= 2:

            score += 30

            volume_spike = True

            reasons.append(
                "ارتفاع قوي مفاجئ في حجم التداول"
            )


        elif ratio_20 >= 1.5:

            score += 20

            reasons.append(
                "حجم التداول أعلى من الطبيعي"
            )


        # ضعف الحجم

        elif ratio_20 <= 0.7:

            score -= 10

            reasons.append(
                "ضعف في حجم التداول"
            )



        # كشف تراكم

        if current_volume > avg_20:

            if closes[-1] >= closes[-5]:

                score += 15

                accumulation = True

                reasons.append(
                    "احتمال دخول سيولة وتجميع"
                )



        # كشف تصريف

        if current_volume > avg_20:

            if closes[-1] < closes[-5]:

                score -= 15

                distribution = True

                reasons.append(
                    "احتمال تصريف"
                )



        if score >= 30:

            state = "VERY_HIGH"


        elif score >= 15:

            state = "HIGH"


        elif score < 0:

            state = "LOW"


        else:

            state = "NORMAL"



        confidence = min(
            abs(score) * 2,
            100
        )



        return {

            "volume_state": state,

            "score": score,

            "confidence": confidence,

            "high_volume": ratio_20 >= 1.5,

            "low_volume": ratio_20 <= 0.7,

            "volume_spike": volume_spike,

            "accumulation": accumulation,

            "distribution": distribution,

            "average_volume_20": round(
                avg_20,
                2
            ),

            "average_volume_50": round(
                avg_50,
                2
            ),

            "current_volume": round(
                current_volume,
                2
            ),

            "ratio_20": round(
                ratio_20,
                2
            ),

            "ratio_50": round(
                ratio_50,
                2
            ),

            "reasons": reasons

        }
