from typing import Dict, Any


from app.ai.opportunity.trend_engine import TrendEngine
from app.ai.opportunity.volume_engine import VolumeEngine
from app.ai.opportunity.liquidity_engine import LiquidityEngine
from app.ai.opportunity.order_blocks import OrderBlocksEngine
from app.ai.opportunity.support_resistance import SupportResistanceEngine
from app.ai.opportunity.candles_ai import CandlesAI
from app.ai.opportunity.historical_learning import HistoricalLearning



class OpportunityEngine:


    def __init__(self):

        self.trend = TrendEngine()

        self.volume = VolumeEngine()

        self.liquidity = LiquidityEngine()

        self.order_blocks = OrderBlocksEngine()

        self.support = SupportResistanceEngine()

        self.candles = CandlesAI()

        self.history = HistoricalLearning()



        self.weights = {

            "trend": 25,

            "volume": 15,

            "liquidity": 15,

            "order_blocks": 15,

            "candles": 10,

            "history": 15,

            "support_resistance": 5

        }



        self.minimum_score = 40
        self.maximum_score = 100



    # ==================================================
    # MAIN OPPORTUNITY ANALYSIS
    # ==================================================


    def analyze(

        self,

        symbol: str,

        candles: list

    ) -> Dict[str, Any]:


        if not candles or len(candles) < 20:

            return {

                "signal": "WAIT",

                "confidence": 0,

                "score": 0,

                "reasons": [

                    "بيانات غير كافية للتحليل"

                ]

            }



        trend = self.trend.analyze(

            symbol

        )


        volume = self.volume.analyze(

            candles

        )


        liquidity = self.liquidity.analyze(

            candles

        )


        order_blocks = self.order_blocks.analyze(

            candles

        )


        candle_patterns = self.candles.analyze(

            candles

        )


        history = self.history.analyze(

            candles

        )


        highs = [

            candle["high"]

            for candle in candles

        ]


        lows = [

            candle["low"]

            for candle in candles

        ]


        closes = [

            candle["close"]

            for candle in candles

        ]



        support = self.support.analyze(

            highs,

            lows,

            closes

        )



        bullish_score = 0

        bearish_score = 0


        reasons = []



        # ==================================================
        # TREND ANALYSIS
        # ==================================================

        trend_signal = trend.get(

            "signal",

            "WAIT"

        )


        if trend_signal == "BUY":

            bullish_score += self.weights["trend"]

            reasons.append(

                "الاتجاه Opportunity يدعم الشراء"

            )


        elif trend_signal == "SELL":

            bearish_score += self.weights["trend"]

            reasons.append(

                "الاتجاه Opportunity يدعم البيع"

            )



        # ==================================================
        # VOLUME ANALYSIS
        # ==================================================

        volume_score = volume.get(

            "score",

            0

        )


        if volume_score > 0:

            bullish_score += min(

                volume_score,

                self.weights["volume"]

            )

            reasons.append(

                "الحجم يدعم الصعود"

            )


        elif volume_score < 0:

            bearish_score += min(

                abs(volume_score),

                self.weights["volume"]

            )

            reasons.append(

                "الحجم يدعم الهبوط"

            )



        # ==================================================
        # LIQUIDITY ANALYSIS
        # ==================================================

        liquidity_score = liquidity.get(

            "score",

            0

        )


        if liquidity_score > 0:

            bullish_score += min(

                liquidity_score,

                self.weights["liquidity"]

            )

            reasons.append(

                "السيولة تشير لصالح المشترين"

            )


        elif liquidity_score < 0:

            bearish_score += min(

                abs(liquidity_score),

                self.weights["liquidity"]

            )

            reasons.append(

                "السيولة تشير لصالح البائعين"

            )



        # ==================================================
        # ORDER BLOCKS
        # ==================================================

        if order_blocks.get(

            "bullish_blocks",

            False

        ):

            bullish_score += self.weights["order_blocks"]

            reasons.append(

                "وجود Bullish Order Block"

            )


        if order_blocks.get(

            "bearish_blocks",

            False

        ):

            bearish_score += self.weights["order_blocks"]

            reasons.append(

                "وجود Bearish Order Block"

            )



        # ==================================================
        # CANDLE AI
        # ==================================================

        candle_confidence = candle_patterns.get(

            "confidence",

            0

        )


        if candle_patterns.get(

            "bullish",

            False

        ):

            bullish_score += min(

                candle_confidence,

                self.weights["candles"]

            )

            reasons.append(

                "الشموع تدعم الصعود"

            )


        if candle_patterns.get(

            "bearish",

            False

        ):

            bearish_score += min(

                candle_confidence,

                self.weights["candles"]

            )

            reasons.append(

                "الشموع تدعم الهبوط"

            )



        # ==================================================
        # HISTORICAL LEARNING
        # ==================================================

        if history.get(

            "bullish",

            False

        ):

            bullish_score += self.weights["history"]

            reasons.append(

                "النماذج التاريخية تدعم الصعود"

            )


        if history.get(

            "bearish",

            False

        ):

            bearish_score += self.weights["history"]

            reasons.append(

                "النماذج التاريخية تدعم الهبوط"

            )



        # ==================================================
        # SUPPORT / RESISTANCE
        # ==================================================

        if support.get(

            "near_support",

            False

        ):

            bullish_score += self.weights["support_resistance"]

            reasons.append(

                "السعر قريب من دعم قوي"

            )


        if support.get(

            "near_resistance",

            False

        ):

            bearish_score += self.weights["support_resistance"]

            reasons.append(

                "السعر قريب من مقاومة قوية"

            )



        # ==================================================
        # FINAL SCORE
        # ==================================================

        final_score = (

            bullish_score

            -

            bearish_score

        )



id="opp_part3"
        # ==================================================
        # SIGNAL DECISION
        # ==================================================

        if (

            bullish_score >= self.minimum_score

            and

            bullish_score > bearish_score

        ):

            signal = "BUY"


        elif (

            bearish_score >= self.minimum_score

            and

            bearish_score > bullish_score

        ):

            signal = "SELL"


        else:

            signal = "WAIT"



        # ==================================================
        # CONFIDENCE CALCULATION
        # ==================================================

        total_score = (

            bullish_score

            +

            bearish_score

        )


        if total_score > 0:

            confidence = int(

                (

                    max(

                        bullish_score,

                        bearish_score

                    )

                    /

                    total_score

                )

                *

                100

            )

        else:

            confidence = 0



        confidence = min(

            confidence,

            self.maximum_score

        )



        # ==================================================
        # FINAL RETURN
        # ==================================================

        return {


            "signal": signal,


            "confidence": confidence,


            "score": final_score,


            "bullish_score": bullish_score,


            "bearish_score": bearish_score,


            "reasons": reasons,


            "trend": trend,


            "volume": volume,


            "liquidity": liquidity,


            "order_blocks": order_blocks,


            "candles": candle_patterns,


            "history": history,


            "support": support,


            "engine": "OpportunityEngine",


            "status": "completed"

            }
