# =====================================================
# backend/app/ai/prediction.py
# FalconAI Advanced Prediction Engine
# Production Intelligence Layer
# =====================================================


from typing import (
    Dict,
    Any,
    List,
    Optional
)

from datetime import datetime
import logging



# =====================================================
# AI MODULES
# =====================================================


from app.ai.market_analyzer import MarketAnalyzer

from app.ai.trend_engine import TrendEngine

from app.ai.opportunity.opportunity_engine import OpportunityEngine


try:

    from app.ai.models.prediction_model import (
        prediction_to_json
    )

except Exception:

    prediction_to_json = None



# Optional Intelligence Modules

try:

    from app.ai.smart_money import SmartMoneyAnalyzer

except Exception:

    SmartMoneyAnalyzer = None



try:

    from app.ai.liquidity import LiquidityAnalyzer

except Exception:

    LiquidityAnalyzer = None



try:

    from app.ai.order_blocks import OrderBlockAnalyzer

except Exception:

    OrderBlockAnalyzer = None



try:

    from app.ai.fibonacci import FibonacciAnalyzer

except Exception:

    FibonacciAnalyzer = None



try:

    from app.ai.news_analyzer import NewsAnalyzer

except Exception:

    NewsAnalyzer = None



try:

    from app.ai.economic_calendar import EconomicCalendar

except Exception:

    EconomicCalendar = None



logger = logging.getLogger(
    "FalconAI.Prediction"
)




# =====================================================
# PREDICTION ENGINE
# =====================================================


class PredictionEngine:


    """
    FalconAI Advanced Prediction Engine


    المسؤوليات:

    - تحليل السوق

    - دمج الذكاء الاصطناعي

    - كشف الاتجاه

    - كشف الانعكاس

    - كشف الاختراق

    - تقييم الثقة

    - تجهيز مخرجات API والموبايل

    """



    def __init__(self):



        self.market = MarketAnalyzer()


        self.trend = TrendEngine()


        self.opportunity = OpportunityEngine()



        # -------------------------------------
        # Advanced Modules
        # -------------------------------------


        self.smart_money = (

            SmartMoneyAnalyzer()

            if SmartMoneyAnalyzer

            else None

        )


        self.liquidity = (

            LiquidityAnalyzer()

            if LiquidityAnalyzer

            else None

        )


        self.order_blocks = (

            OrderBlockAnalyzer()

            if OrderBlockAnalyzer

            else None

        )


        self.fibonacci = (

            FibonacciAnalyzer()

            if FibonacciAnalyzer

            else None

        )


        self.news = (

            NewsAnalyzer()

            if NewsAnalyzer

            else None

        )



        self.economic = (

            EconomicCalendar()

            if EconomicCalendar

            else None

        )



        # -------------------------------------
        # Intelligence Weights
        # -------------------------------------


        self.weights = {


            "trend": 0.25,


            "momentum": 0.15,


            "volume": 0.10,


            "rsi": 0.10,


            "macd": 0.10,


            "opportunity": 0.15,


            "smart_money": 0.10,


            "liquidity": 0.05


        }



        # -------------------------------------
        # Decision Settings
        # -------------------------------------


        self.minimum_confidence = 60


        self.minimum_signal_score = 6


        self.maximum_confidence = 100


        self.allow_counter_trend = False



        # -------------------------------------
        # AI Filters
        # -------------------------------------


        self.enable_news_filter = True


        self.enable_economic_filter = True


        self.enable_fibonacci_filter = True


        self.enable_smart_money_filter = True


        self.enable_volume_filter = True


        self.enable_liquidity_filter = True


        self.enable_orderblock_filter = True



        # -------------------------------------
        # Performance Memory
        # -------------------------------------


        self.signal_statistics = {


            "buy": 0,


            "sell": 0,


            "wait": 0,


            "success": 0,


            "failed": 0


        }



        self.prediction_history = []



        self.version = (

            "FalconAI Prediction Engine V3.0"

        )


        logger.info(

            "Prediction Engine initialized"

        )



# =====================================================
# MAIN PREDICTION PIPELINE
# =====================================================


    def predict(

        self,

        symbol: str = "BTCUSDT",

        interval: str = "1h",

        market: str = "crypto",

        economic_event: Optional[Dict[str, Any]] = None

    ) -> Dict[str, Any]:



        market_data = self.market.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )



        trend_data = self.trend.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )



        candles = market_data.get(

            "candles",

            []

        )



        opportunity = self.opportunity.analyze(

            symbol=symbol,

            candles=candles

        ) if candles else {


            "signal": "WAIT",

            "confidence": 0

        }



        smart_money = self.safe_module_call(

            self.smart_money,

            symbol,

            interval

        )



        liquidity = self.safe_module_call(

            self.liquidity,

            candles

        )



        order_blocks = self.safe_module_call(

            self.order_blocks,

            candles

        )



        fibonacci = self.safe_module_call(

            self.fibonacci,

            symbol,

            interval

        )



        news = self.safe_module_call(

            self.news,

            symbol

        )



        prediction = self.fusion_prediction(

            market_data,

            trend_data,

            opportunity,

            smart_money,

            liquidity,

            order_blocks,

            fibonacci,

            news

        )



        prediction["symbol"] = symbol


        prediction["market"] = market


        prediction["interval"] = interval



        prediction["created_at"] = datetime.utcnow().isoformat()



        if prediction_to_json:


            return prediction_to_json(

                prediction

            )



        return prediction





# =====================================================
# SAFE MODULE CALL
# =====================================================


    def safe_module_call(

        self,

        module,

        *args

    ):


        if module is None:

            return {


                "available": False

            }



        try:

            return module.analyze(

                *args

            )


        except Exception as e:


            logger.warning(

                f"Module error: {e}"

            )


            return {


                "available": False,

                "error": str(e)

            }





# =====================================================
# AI FUSION PREDICTION
# =====================================================


    def fusion_prediction(

        self,

        market_data: Dict[str, Any],

        trend_data: Dict[str, Any],

        opportunity: Dict[str, Any],

        smart_money: Dict[str, Any],

        liquidity: Dict[str, Any],

        order_blocks: Dict[str, Any],

        fibonacci: Dict[str, Any],

        news: Dict[str, Any]

    ) -> Dict[str, Any]:



        bullish_score = 0


        bearish_score = 0



        reasons = []


        conflicts = []



        trend_score = trend_data.get(

            "score",

            0

        )



        rsi = market_data.get(

            "rsi",

            50

        )



        momentum = market_data.get(

            "momentum",

            0

        )



        volume = market_data.get(

            "volume_ratio",

            1

        )



        opportunity_signal = opportunity.get(

            "signal",

            "WAIT"

        )



        opportunity_confidence = opportunity.get(

            "confidence",

            0

        )



        # -----------------------------
        # Trend Intelligence
        # -----------------------------


        if trend_score > 0:


            bullish_score += trend_score * self.weights["trend"]


            reasons.append(

                "الاتجاه العام صاعد"

            )


        elif trend_score < 0:


            bearish_score += abs(trend_score) * self.weights["trend"]


            reasons.append(

                "الاتجاه العام هابط"

            )



        # -----------------------------
        # Momentum
        # -----------------------------


        if momentum > 0:


            bullish_score += abs(momentum) * self.weights["momentum"]


            reasons.append(

                "الزخم إيجابي"

            )


        elif momentum < 0:


            bearish_score += abs(momentum) * self.weights["momentum"]


            reasons.append(

                "الزخم سلبي"

            )



        # -----------------------------
        # RSI
        # -----------------------------


        if rsi < 35:


            bullish_score += 10


            reasons.append(

                "تشبع بيع"

            )


        elif rsi > 65:


            bearish_score += 10


            reasons.append(

                "تشبع شراء"

            )



        # -----------------------------
        # Volume
        # -----------------------------


        if volume > 1.5:


            bullish_score += 10


            reasons.append(

                "حجم تداول قوي"

            )


        elif volume < 0.7:


            conflicts.append(

                "ضعف الحجم"

            )



        # -----------------------------
        # Opportunity
        # -----------------------------


        if opportunity_signal == "BUY":


            bullish_score += opportunity_confidence * 0.25


        elif opportunity_signal == "SELL":


            bearish_score += opportunity_confidence * 0.25



# =====================================================
# ADVANCED INTELLIGENCE FUSION
# =====================================================


        # -----------------------------
        # Smart Money Intelligence
        # -----------------------------


        if smart_money.get("available"):


            smart_direction = smart_money.get(

                "direction",

                "NONE"

            )


            smart_strength = smart_money.get(

                "strength",

                0

            )



            if smart_direction == "BUY":


                bullish_score += (

                    smart_strength *

                    self.weights["smart_money"]

                )


                reasons.append(

                    "الأموال الذكية تدعم الشراء"

                )



            elif smart_direction == "SELL":


                bearish_score += (

                    smart_strength *

                    self.weights["smart_money"]

                )


                reasons.append(

                    "الأموال الذكية تدعم البيع"

                )





        # -----------------------------
        # Liquidity Intelligence
        # -----------------------------


        if liquidity.get("available"):


            liquidity_strength = liquidity.get(

                "strength",

                0

            )


            bullish_score += (

                liquidity_strength *

                self.weights["liquidity"]

            )


            reasons.append(

                "السيولة تؤكد النشاط"

            )





        # -----------------------------
        # Order Blocks
        # -----------------------------


        if order_blocks.get("available"):


            bullish_blocks = order_blocks.get(

                "bullish_blocks",

                []

            )


            bearish_blocks = order_blocks.get(

                "bearish_blocks",

                []

            )


            if bullish_blocks:


                bullish_score += 10


                reasons.append(

                    "منطقة طلب قوية"

                )



            if bearish_blocks:


                bearish_score += 10


                reasons.append(

                    "منطقة عرض قوية"

                )





        # -----------------------------
        # Fibonacci Filter
        # -----------------------------


        if self.enable_fibonacci_filter:


            if fibonacci.get("available"):


                reasons.append(

                    "Fibonacci فعال في التحليل"

                )





        # -----------------------------
        # News Risk
        # -----------------------------


        if self.enable_news_filter:


            if news.get("impact") == "HIGH":


                conflicts.append(

                    "خبر عالي التأثير"

                )





        # -----------------------------
        # Market Regime
        # -----------------------------


        market_regime = self.detect_market_regime(

            market_data,

            trend_data

        )





        # -----------------------------
        # Probability Calculation
        # -----------------------------


        total_score = (

            bullish_score +

            bearish_score

        )



        if total_score == 0:


            bullish_probability = 50


            bearish_probability = 50



        else:


            bullish_probability = (

                bullish_score /

                total_score

            ) * 100



            bearish_probability = (

                bearish_score /

                total_score

            ) * 100





        # -----------------------------
        # Direction
        # -----------------------------


        if bullish_probability > bearish_probability:


            direction = "BULLISH"



        elif bearish_probability > bullish_probability:


            direction = "BEARISH"



        else:


            direction = "NEUTRAL"





        # -----------------------------
        # Final Signal
        # -----------------------------


        signal = "WAIT"



        if bullish_probability >= 65:


            signal = "BUY"



        elif bearish_probability >= 65:


            signal = "SELL"





        confidence = self.calculate_confidence(

            bullish_probability,

            bearish_probability,

            len(conflicts)

        )



        quality = self.signal_quality(

            confidence,

            len(conflicts)

        )



        return {


            "signal": signal,


            "direction": direction,


            "confidence": confidence,


            "quality": quality,


            "probability": {


                "bullish": round(

                    bullish_probability,

                    2

                ),


                "bearish": round(

                    bearish_probability,

                    2

                )

            },


            "market_regime": market_regime,


            "reasons": reasons,


            "conflicts": conflicts,


            "scores": {


                "bullish": round(

                    bullish_score,

                    2

                ),


                "bearish": round(

                    bearish_score,

                    2

                )

            }

        }



# =====================================================
# MARKET REGIME DETECTOR
# =====================================================


    def detect_market_regime(

        self,

        market_data,

        trend_data

    ):


        trend = trend_data.get(

            "trend",

            "SIDEWAYS"

        )



        volatility = market_data.get(

            "volatility",

            0

        )



        if trend in [

            "STRONG_BULL",

            "STRONG_BEAR"

        ]:


            return "TRENDING"



        if volatility > 3:


            return "HIGH_VOLATILITY"



        return "RANGE"



# =====================================================
# CONFIDENCE ENGINE
# =====================================================


    def calculate_confidence(

        self,

        bullish_probability,

        bearish_probability,

        conflicts_count

    ):


        difference = abs(

            bullish_probability -

            bearish_probability

        )



        confidence = difference



        penalty = (

            conflicts_count *

            8

        )



        confidence -= penalty



        if confidence < 0:

            confidence = 0



        if confidence > 100:

            confidence = 100



        return round(

            confidence,

            2

        )





# =====================================================
# SIGNAL QUALITY
# =====================================================


    def signal_quality(

        self,

        confidence,

        conflicts

    ):


        if confidence >= 85 and conflicts == 0:

            return "VERY_STRONG"



        if confidence >= 70:

            return "STRONG"



        if confidence >= 50:

            return "MEDIUM"



        return "WEAK"





# =====================================================
# EARLY MOVE DETECTOR
# =====================================================


    def detect_early_move(

        self,

        market_data

    ):


        score = 0


        reasons = []



        momentum = market_data.get(

            "momentum",

            0

        )


        volume = market_data.get(

            "volume_ratio",

            1

        )


        volatility = market_data.get(

            "volatility",

            0

        )



        if momentum > 0:


            score += 25


            reasons.append(

                "بداية زخم صاعد"

            )


        elif momentum < 0:


            score -= 25


            reasons.append(

                "بداية ضعف"

            )



        if volume > 1.5:


            score += 30


            reasons.append(

                "دخول سيولة قوية"

            )



        if volatility > 2:


            score += 15


            reasons.append(

                "نشاط سوق مرتفع"

            )



        return {


            "score": score,


            "probability": min(

                abs(score),

                100

            ),


            "direction":

                "UP"

                if score > 0

                else

                "DOWN"

                if score < 0

                else

                "NONE",


            "reasons": reasons

        }





# =====================================================
# REVERSAL ENGINE
# =====================================================


    def reversal_probability(

        self,

        market_data,

        trend_data

    ):


        score = 0


        reasons = []



        rsi = market_data.get(

            "rsi",

            50

        )


        trend = trend_data.get(

            "score",

            0

        )



        if rsi < 30:


            score += 30


            reasons.append(

                "تشبع بيعي واحتمال انعكاس"

            )



        if rsi > 70:


            score -= 30


            reasons.append(

                "تشبع شرائي واحتمال تصحيح"

            )



        if trend < 0 and rsi < 35:


            score += 20


            reasons.append(

                "انعكاس ضد الاتجاه"

            )



        return {


            "score": score,


            "probability": min(

                abs(score),

                100

            ),


            "reasons": reasons

        }





# =====================================================
# BREAKOUT INTELLIGENCE
# =====================================================


    def breakout_probability(

        self,

        candles

    ):


        if len(candles) < 30:


            return {


                "probability": 0,


                "type": "NONE"

            }



        closes = [

            x.get(

                "close",

                0

            )

            for x in candles

        ]



        price = closes[-1]



        resistance = max(

            closes[-30:]

        )


        support = min(

            closes[-30:]

        )



        if price >= resistance:


            return {


                "probability": 80,


                "type": "BULLISH"

            }



        if price <= support:


            return {


                "probability": 80,


                "type": "BEARISH"

            }



        return {


            "probability": 0,


            "type": "NONE"

        }





# =====================================================
# ADAPTIVE WEIGHT UPDATE
# =====================================================


    def update_weights(

        self,

        success: bool

    ):


        adjustment = (

            0.01

            if success

            else

            -0.01

        )



        for key in self.weights:


            self.weights[key] += adjustment



            self.weights[key] = max(

                0,

                min(

                    self.weights[key],

                    1

                )

            )



        return self.weights





# =====================================================
# HEALTH CHECK
# =====================================================


    def health_check(

        self

    ):


        return {


            "engine":

                self.version,


            "status":

                "running",


            "modules": {


                "market":

                    True,


                "trend":

                    True,


                "opportunity":

                    True,


                "smart_money":

                    self.smart_money is not None,


                "liquidity":

                    self.liquidity is not None,


                "fibonacci":

                    self.fibonacci is not None


            }

        }





# =====================================================
# FINAL REPORT
# =====================================================


    def generate_report(

        self,

        prediction

    ):


        return {


            "summary": {


                "signal":

                    prediction.get(

                        "signal"

                    ),


                "confidence":

                    prediction.get(

                        "confidence"

                    ),


                "quality":

                    prediction.get(

                        "quality"

                    )

            },


            "probability":

                prediction.get(

                    "probability",

                    {}

                ),


            "reasons":

                prediction.get(

                    "reasons",

                    []

                ),


            "conflicts":

                prediction.get(

                    "conflicts",

                    []

                )

        }
