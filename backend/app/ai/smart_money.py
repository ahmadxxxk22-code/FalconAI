from typing import List, Dict, Any
from statistics import mean

from app.services.market_data import MarketData


class SmartMoneyAnalyzer:

    def __init__(self):

        self.market = MarketData()

        # شموع اكتشاف Swing
        self.swing_window = 7

        # هامش اعتبار القمم/القيعان متساوية
        self.equal_tolerance = 0.0015

        # قوة شمعة displacement
        self.displacement_multiplier = 1.8

        # متوسط جسم الشموع
        self.average_body_period = 50


    # =====================================================
    # MAIN ANALYSIS
    # =====================================================

    def analyze(

        self,

        symbol="BTCUSDT",

        interval="1h",

        market="crypto"

    ):


        candles = self.market.get_candles(

            symbol=symbol,

            interval=interval,

            limit=400,

            market=market

        )


        if not candles or len(candles) < 100:

            return self.empty_result()



        highs = [
            c["high"]
            for c in candles
        ]


        lows = [
            c["low"]
            for c in candles
        ]


        closes = [
            c["close"]
            for c in candles
        ]


        current_price = closes[-1]


        bullish = False

        bearish = False


        score = 0

        reasons = []



        # =================================================
        # Swing Structure
        # =================================================


        swing_highs = self.detect_swing_highs(

            highs

        )


        swing_lows = self.detect_swing_lows(

            lows

        )



        last_swing_high = (

            swing_highs[-1]

            if swing_highs

            else None

        )


        last_swing_low = (

            swing_lows[-1]

            if swing_lows

            else None

        )



        # =================================================
        # Liquidity Sweep
        # =================================================


        liquidity_sweep = False

        liquidity_side = "NONE"



        if last_swing_high:


            if (

                highs[-1] >

                last_swing_high["price"]

                and

                closes[-1] <

                last_swing_high["price"]

            ):


                liquidity_sweep = True

                liquidity_side = "BUY_SIDE"


                bearish = True


                score += 15


                reasons.append(

                    "سحب سيولة من القمم ثم رفض السعر"

                )



        if last_swing_low:


            if (

                lows[-1] <

                last_swing_low["price"]

                and

                closes[-1] >

                last_swing_low["price"]

            ):


                liquidity_sweep = True

                liquidity_side = "SELL_SIDE"


                bullish = True


                score += 15


                reasons.append(

                    "سحب سيولة من القيعان ثم انعكاس"

                )



        # =================================================
        # Equal Highs / Equal Lows
        # =================================================


        equal_highs = []

        equal_lows = []


        for i in range(1, len(swing_highs)):

            previous = swing_highs[i - 1]["price"]

            current = swing_highs[i]["price"]


            difference = abs(
                current - previous
            ) / previous


            if difference <= self.equal_tolerance:

                equal_highs.append(
                    swing_highs[i]
                )



        for i in range(1, len(swing_lows)):

            previous = swing_lows[i - 1]["price"]

            current = swing_lows[i]["price"]


            difference = abs(
                current - previous
            ) / previous


            if difference <= self.equal_tolerance:

                equal_lows.append(
                    swing_lows[i]
                )



        if equal_highs:

            score += 5

            reasons.append(
                "تم اكتشاف Equal Highs (سيولة فوق القمم)"
            )



        if equal_lows:

            score += 5

            reasons.append(
                "تم اكتشاف Equal Lows (سيولة تحت القيعان)"
            )



        # =================================================
        # Displacement Detection
        # =================================================


        displacement = False


        bodies = [

            abs(
                c["close"] -
                c["open"]
            )

            for c in candles[
                -self.average_body_period:
            ]

        ]


        average_body = mean(
            bodies
        )


        current_body = abs(

            candles[-1]["close"]

            -

            candles[-1]["open"]

        )



        if (

            current_body >=

            average_body *

            self.displacement_multiplier

        ):


            displacement = True


            score += 15


            reasons.append(

                "شمعة Displacement قوية"

            )



            if candles[-1]["close"] > candles[-1]["open"]:

                bullish = True


            else:

                bearish = True




        # =================================================
        # Break Of Structure (BOS)
        # =================================================


        bos = False

        bos_direction = "NONE"



        if last_swing_high:


            if current_price > last_swing_high["price"]:


                bos = True

                bos_direction = "BULLISH"


                bullish = True


                score += 20


                reasons.append(

                    "كسر هيكل صاعد BOS"

                )




        if last_swing_low:


            if current_price < last_swing_low["price"]:


                bos = True

                bos_direction = "BEARISH"


                bearish = True


                score += 20


                reasons.append(

                    "كسر هيكل هابط BOS"

                )



        # =================================================
        # Change Of Character (CHOCH)
        # =================================================


        choch = False

        choch_direction = "NONE"



        if (

            len(swing_highs) >= 2

            and

            len(swing_lows) >= 2

        ):


            last_high = swing_highs[-1]["price"]

            previous_high = swing_highs[-2]["price"]


            last_low = swing_lows[-1]["price"]

            previous_low = swing_lows[-2]["price"]



            # انعكاس صاعد

            if (

                last_low > previous_low

                and

                current_price > last_high

            ):


                choch = True

                choch_direction = "BULLISH"


                bullish = True


                score += 20


                reasons.append(

                    "CHoCH صاعد - تغير الاتجاه"

                )



            # انعكاس هابط

            elif (

                last_high < previous_high

                and

                current_price < last_low

            ):


                choch = True

                choch_direction = "BEARISH"


                bearish = True


                score += 20


                reasons.append(

                    "CHoCH هابط - تغير الاتجاه"

        )



        # =================================================
        # Internal BOS
        # =================================================

        internal_bos = False


        if len(closes) >= 10:


            recent_high = max(
                closes[-10:-1]
            )


            recent_low = min(
                closes[-10:-1]
            )


            if current_price > recent_high:


                internal_bos = True

                bullish = True

                score += 8


                reasons.append(
                    "Internal Bullish BOS"
                )



            elif current_price < recent_low:


                internal_bos = True

                bearish = True

                score += 8


                reasons.append(
                    "Internal Bearish BOS"
                )



        # =================================================
        # Premium / Discount
        # =================================================


        premium_discount = "NEUTRAL"


        if last_swing_high and last_swing_low:


            high = last_swing_high["price"]

            low = last_swing_low["price"]


            midpoint = (

                high + low

            ) / 2



            if current_price > midpoint:


                premium_discount = "PREMIUM"


                reasons.append(
                    "السعر داخل Premium Zone"
                )



            else:


                premium_discount = "DISCOUNT"


                reasons.append(
                    "السعر داخل Discount Zone"
                )



        # =================================================
        # Fair Value Gap
        # =================================================


        fair_value_gap = None



        if len(candles) >= 3:


            c1 = candles[-3]

            c3 = candles[-1]



            # Bullish FVG

            if c3["low"] > c1["high"]:


                fair_value_gap = {


                    "type": "BULLISH",


                    "top": c3["low"],


                    "bottom": c1["high"]

                }



                score += 10


                reasons.append(
                    "Bullish Fair Value Gap"
                )




            # Bearish FVG

            elif c3["high"] < c1["low"]:


                fair_value_gap = {


                    "type": "BEARISH",


                    "top": c1["low"],


                    "bottom": c3["high"]

                }



                score += 10


                reasons.append(
                    "Bearish Fair Value Gap"
                )



        # =================================================
        # Order Block
        # =================================================


        order_block = None



        if bullish:


            for candle in reversed(candles[-20:-1]):


                if candle["close"] < candle["open"]:


                    order_block = {


                        "type": "BULLISH",


                        "high": candle["high"],


                        "low": candle["low"]

                    }


                    break




        elif bearish:


            for candle in reversed(candles[-20:-1]):


                if candle["close"] > candle["open"]:


                    order_block = {


                        "type": "BEARISH",


                        "high": candle["high"],


                        "low": candle["low"]

                    }


                    break



        # =================================================
        # Mitigation Block
        # =================================================


        mitigation_block = None


        if order_block:


            mitigation_block = {


                "active": True,


                "zone": order_block

            }




        # =================================================
        # Breaker Block
        # =================================================


        breaker_block = None



        if bos and liquidity_sweep:


            breaker_block = {


                "active": True,


                "direction": bos_direction,


                "reason": "BOS + Liquidity Sweep"

            }



            score += 10



        # =================================================
        # Final Score
        # =================================================


        score = min(
            score,
            100
        )


        confidence = score



        signal = "WAIT"



        if bullish and score >= 60:


            signal = "BUY"



        elif bearish and score >= 60:


            signal = "SELL"




        return {


            "signal": signal,


            "confidence": confidence,


            "smart_money_score": score,


            "bullish": bullish,


            "bearish": bearish,


            "bos": bos,


            "bos_direction": bos_direction,


            "choch": choch,


            "choch_direction": choch_direction,


            "internal_bos": internal_bos,


            "liquidity_sweep": liquidity_sweep,


            "liquidity_side": liquidity_side,


            "equal_highs": equal_highs,


            "equal_lows": equal_lows,


            "displacement": displacement,


            "premium_discount": premium_discount,


            "fair_value_gap": fair_value_gap,


            "order_block": order_block,


            "mitigation_block": mitigation_block,


            "breaker_block": breaker_block,


            "reasons": reasons

        }



    # =====================================================
    # EMPTY RESULT
    # =====================================================


    def empty_result(self):


        return {


            "signal": "WAIT",


            "confidence": 0,


            "smart_money_score": 0,


            "bullish": False,


            "bearish": False,


            "bos": False,


            "bos_direction": "NONE",


            "choch": False,


            "choch_direction": "NONE",


            "internal_bos": False,


            "liquidity_sweep": False,


            "liquidity_side": "NONE",


            "equal_highs": [],


            "equal_lows": [],


            "displacement": False,


            "premium_discount": "NEUTRAL",


            "fair_value_gap": None,


            "order_block": None,


            "mitigation_block": None,


            "breaker_block": None,


            "reasons": []

                }
