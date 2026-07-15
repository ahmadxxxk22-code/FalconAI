class LiquidityEngine:


    def analyze(
        self,
        candles
    ):


        if len(candles) < 30:

            return {

                "liquidity": "UNKNOWN",

                "score": 0,

                "confidence": 0,

                "buy_liquidity": False,

                "sell_liquidity": False,

                "liquidity_sweep": False,

                "fake_breakout": False,

                "reasons": []

            }



        recent = candles[-30:]


        highs = [

            c["high"]

            for c in recent[:-1]

        ]


        lows = [

            c["low"]

            for c in recent[:-1]

        ]



        highest = max(highs)

        lowest = min(lows)



        current = candles[-1]

        previous = candles[-2]



        score = 0

        reasons = []



        buy_liquidity = False

        sell_liquidity = False

        liquidity_sweep = False

        fake_breakout = False



        # =================================
        # سحب سيولة فوق القمم
        # =================================

        if current["high"] > highest:


            buy_liquidity = True

            score += 20

            reasons.append(
                "تم أخذ سيولة فوق القمم السابقة"
            )



            # رجوع السعر تحت القمة = فخ شراء

            if current["close"] < highest:


                liquidity_sweep = True

                fake_breakout = True

                score += 15

                reasons.append(
                    "احتمال انعكاس بعد سحب سيولة شرائية"
                )



        # =================================
        # سحب سيولة تحت القيعان
        # =================================

        if current["low"] < lowest:


            sell_liquidity = True

            score += 20

            reasons.append(
                "تم أخذ سيولة تحت القيعان السابقة"
            )



            if current["close"] > lowest:


                liquidity_sweep = True

                fake_breakout = True

                score += 15

                reasons.append(
                    "احتمال انعكاس بعد سحب سيولة بيعية"
                )



        # =================================
        # تحديد الحالة
        # =================================


        if liquidity_sweep:

            state = "SWEEP"


        elif buy_liquidity:

            state = "BUY_SIDE"


        elif sell_liquidity:

            state = "SELL_SIDE"


        else:

            state = "NORMAL"



        confidence = min(
            abs(score) * 3,
            100
        )



        return {


            "liquidity": state,


            "score": score,


            "confidence": confidence,


            "buy_liquidity": buy_liquidity,


            "sell_liquidity": sell_liquidity,


            "liquidity_sweep": liquidity_sweep,


            "fake_breakout": fake_breakout,


            "highest_liquidity_level": highest,


            "lowest_liquidity_level": lowest,


            "reasons": reasons

                }
