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


from app.notifications.alert_engine import AlertEngine

from app.notifications.notification_manager import NotificationManager



try:

    from app.ai.models.prediction_model import (
        prediction_to_json
    )

except Exception:

    prediction_to_json = None




# =====================================================
# OPTIONAL AI MODULES
# =====================================================


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

    Production Intelligence Layer

    Features:

    - Technical Analysis Fusion
    - Smart Money Intelligence
    - Liquidity Analysis
    - Order Blocks
    - Fibonacci
    - News Filtering
    - Economic Events
    - Early Trend Detection
    - Reversal Detection
    - Breakout Detection
    - Explainable AI
    - User Alerts
    """



    def __init__(self):


        self.market = MarketAnalyzer()


        self.trend = TrendEngine()


        self.opportunity = OpportunityEngine()



        self.alert_engine = AlertEngine()


        self.notification_manager = NotificationManager()




        # =================================================
        # Advanced Modules
        # =================================================



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





        # =================================================
        # AI Dynamic Weights
        # =================================================



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





        # =================================================
        # AI Settings
        # =================================================



        self.minimum_confidence = 60


        self.maximum_confidence = 100


        self.allow_counter_trend = False




        self.enable_news_filter = True


        self.enable_economic_filter = True


        self.enable_fibonacci_filter = True


        self.enable_smart_money_filter = True


        self.enable_volume_filter = True


        self.enable_liquidity_filter = True


        self.enable_orderblock_filter = True




        # =================================================
        # AI Memory
        # =================================================



        self.signal_statistics = {


            "buy": 0,


            "sell": 0,


            "wait": 0,


            "success": 0,


            "failed": 0

        }



        self.prediction_history = []



        self.version = (

            "FalconAI Prediction Engine V4.0"

        )



        logger.info(

            "FalconAI Prediction Engine Started"

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



        opportunity = (

            self.opportunity.analyze(

                symbol=symbol,

                candles=candles

            )

            if candles

            else

            {

                "signal": "WAIT",

                "confidence": 0

            }

        )





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





        early_move = self.detect_early_move(

            market_data

        )



        reversal = self.reversal_probability(

            market_data,

            trend_data

        )



        breakout = self.breakout_probability(

            candles

        )





        prediction["symbol"] = symbol


        prediction["market"] = market


        prediction["interval"] = interval



        prediction["early_move"] = early_move


        prediction["reversal"] = reversal


        prediction["breakout"] = breakout



        prediction["created_at"] = datetime.utcnow().isoformat()





        # =====================================================
        # ALERT GENERATION
        # =====================================================



        alert = self.alert_engine.analyze_prediction(

            {

                **prediction

            }

        )



        if alert:


            prediction["alert"] = alert.to_dict()



            self.notification_manager.add_notification(

                alert

            )


        else:


            prediction["alert"] = None






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



        except Exception as error:


            logger.warning(

                f"AI module failed: {error}"

            )



            return {


                "available": False,


                "error": str(error)

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



        macd = market_data.get(

            "macd",

            0

        )



        momentum = market_data.get(

            "momentum",

            0

        )



        volume_ratio = market_data.get(

            "volume_ratio",

            0

        )



        opportunity_signal = opportunity.get(

            "signal",

            "WAIT"

        )



        opportunity_confidence = opportunity.get(

            "confidence",

            0

        )





        # =====================================================
        # TREND ENGINE
        # =====================================================


        if trend_score > 0:


            bullish_score += (

                abs(trend_score)

                *

                self.weights["trend"]

            )


            reasons.append(

                "الاتجاه العام يدعم الصعود"

            )



        elif trend_score < 0:


            bearish_score += (

                abs(trend_score)

                *

                self.weights["trend"]

            )


            reasons.append(

                "الاتجاه العام يدعم الهبوط"

            )





        # =====================================================
        # RSI
        # =====================================================


        if rsi < 35:


            bullish_score += (

                15

                *

                self.weights["rsi"]

            )


            reasons.append(

                "RSI يظهر فرصة انعكاس صعودي"

            )



        elif rsi > 65:


            bearish_score += (

                15

                *

                self.weights["rsi"]

            )


            reasons.append(

                "RSI يظهر ضغط بيعي"

            )





        # =====================================================
        # MACD
        # =====================================================


        if macd > 0:


            bullish_score += (

                abs(macd)

                *

                10

                *

                self.weights["macd"]

            )


            reasons.append(

                "MACD إيجابي"

            )



        elif macd < 0:


            bearish_score += (

                abs(macd)

                *

                10

                *

                self.weights["macd"]

            )


            reasons.append(

                "MACD سلبي"

            )





        # =====================================================
        # MOMENTUM
        # =====================================================


        if momentum > 0:


            bullish_score += (

                abs(momentum)

                *

                8

                *

                self.weights["momentum"]

            )


            reasons.append(

                "الزخم يتحسن"

            )



        elif momentum < 0:


            bearish_score += (

                abs(momentum)

                *

                8

                *

                self.weights["momentum"]

            )


            reasons.append(

                "الزخم يضعف"

            )





        # =====================================================
        # VOLUME
        # =====================================================


        if volume_ratio > 1:


            bullish_score += (

                10

                *

                self.weights["volume"]

            )


            reasons.append(

                "حجم التداول يؤكد الحركة"

            )



        elif volume_ratio < 0.7:


            conflicts.append(

                "ضعف حجم التداول"

            )





        # =====================================================
        # OPPORTUNITY ENGINE
        # =====================================================


        if opportunity_signal == "BUY":


            bullish_score += (

                opportunity_confidence

                *

                self.weights["opportunity"]

            )


            reasons.append(

                "محرك الفرص يدعم الشراء"

            )



        elif opportunity_signal == "SELL":


            bearish_score += (

                opportunity_confidence

                *

                self.weights["opportunity"]

            )


            reasons.append(

                "محرك الفرص يدعم البيع"

            )





        # =====================================================
        # SMART MONEY
        # =====================================================


        smart_signal = smart_money.get(

            "signal",

            "WAIT"

        )



        if smart_signal == "BUY":


            bullish_score += 15


            reasons.append(

                "Smart Money يدعم الصعود"

            )



        elif smart_signal == "SELL":


            bearish_score += 15


            reasons.append(

                "Smart Money يدعم الهبوط"

            )





        # =====================================================
        # LIQUIDITY
        # =====================================================


        liquidity_signal = liquidity.get(

            "signal",

            "NONE"

        )



        if liquidity_signal == "BUY":


            bullish_score += 10


            reasons.append(

                "السيولة تدعم الشراء"

            )



        elif liquidity_signal == "SELL":


            bearish_score += 10


            reasons.append(

                "السيولة تدعم البيع"

            )





        # =====================================================
        # FINAL CALCULATION
        # =====================================================


        total_score = (

            bullish_score

            +

            bearish_score

        )



        if total_score == 0:


            bullish_probability = 50


            bearish_probability = 50



        else:


            bullish_probability = (

                bullish_score

                /

                total_score

            ) * 100



            bearish_probability = (

                bearish_score

                /

                total_score

            ) * 100





        if bullish_probability > bearish_probability:


            direction = "BULLISH"



        elif bearish_probability > bullish_probability:


            direction = "BEARISH"



        else:


            direction = "NEUTRAL"





        signal = "WAIT"



        if bullish_probability >= 65:


            signal = "BUY"



        elif bearish_probability >= 65:


            signal = "SELL"





        confidence = self.calculate_advanced_confidence(

            bullish_probability,

            bearish_probability,

            opportunity_confidence,

            conflicts

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


            "market_regime": self.detect_market_regime(

                market_data,

                trend_data

            ),


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
# EARLY MOVE DETECTOR
# =====================================================


    def detect_early_move(

        self,

        market_data: Dict[str, Any]

    ) -> Dict[str, Any]:



        score = 0


        reasons = []



        momentum = market_data.get(

            "momentum",

            0

        )


        volume = market_data.get(

            "volume_ratio",

            0

        )


        volatility = market_data.get(

            "volatility",

            0

        )





        if momentum > 0:


            score += 25


            reasons.append(

                "بداية زخم صعودي"

            )



        elif momentum < 0:


            score -= 25


            reasons.append(

                "بداية ضعف وهبوط"

            )





        if volume > 1.5:


            score += 30


            reasons.append(

                "دخول حجم تداول قوي"

            )





        if volatility > 2:


            score += 15


            reasons.append(

                "نشاط سوق مرتفع"

            )





        probability = min(

            abs(score),

            100

        )





        direction = "NONE"



        if score > 0:


            direction = "UP"



        elif score < 0:


            direction = "DOWN"





        return {


            "direction": direction,


            "probability": probability,


            "score": score,


            "reasons": reasons

        }







# =====================================================
# REVERSAL PROBABILITY
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



        momentum = market_data.get(

            "momentum",

            0

        )



        trend_score = trend_data.get(

            "score",

            0

        )





        if rsi < 30:


            score += 25


            reasons.append(

                "تشبع بيعي واحتمال انعكاس"

            )



        elif rsi > 70:


            score -= 25


            reasons.append(

                "تشبع شرائي واحتمال تصحيح"

            )





        if momentum > 0 and trend_score < 0:


            score += 20


            reasons.append(

                "تغير زخم ضد الاتجاه"

            )





        elif momentum < 0 and trend_score > 0:


            score -= 20


            reasons.append(

                "ضعف اتجاه صاعد"

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
# BREAKOUT PROBABILITY
# =====================================================


    def breakout_probability(

        self,

        candles: List[Dict[str, Any]]

    ):



        if len(candles) < 30:


            return {


                "probability": 0,


                "type": "NONE",


                "reasons": [

                    "بيانات غير كافية"

                ]

            }





        closes = [


            candle.get(

                "close",

                0

            )


            for candle in candles


        ]





        price = closes[-1]



        resistance = max(

            closes[-30:]

        )



        support = min(

            closes[-30:]

        )



        result = {


            "probability": 0,


            "type": "NONE",


            "reasons": []

        }





        if price >= resistance:


            result["probability"] = 70


            result["type"] = "BULLISH"


            result["reasons"].append(

                "اختراق مقاومة"

            )





        elif price <= support:


            result["probability"] = 70


            result["type"] = "BEARISH"


            result["reasons"].append(

                "كسر دعم"

            )





        return result







# =====================================================
# CONFIDENCE ENGINE
# =====================================================


    def calculate_advanced_confidence(

        self,

        bullish,

        bearish,

        opportunity,

        conflicts

    ):



        confidence = (

            abs(

                bullish - bearish

            )

            *

            0.6

        ) + (

            opportunity

            *

            0.4

        )



        confidence -= (

            len(conflicts)

            *

            8

        )



        return round(

            max(

                min(

                    confidence,

                    100

                ),

                0

            ),

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
# MARKET REGIME
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
# HEALTH CHECK
# =====================================================


    def health_check(self):


        return {


            "engine": self.version,


            "status": "running",


            "modules": {


                "market": True,


                "trend": True,


                "opportunity": True,


                "alerts": True,


                "notifications": True,


                "smart_money": self.smart_money is not None,


                "liquidity": self.liquidity is not None,


                "order_blocks": self.order_blocks is not None,


                "fibonacci": self.fibonacci is not None,


                "news": self.news is not None

            }

    }
