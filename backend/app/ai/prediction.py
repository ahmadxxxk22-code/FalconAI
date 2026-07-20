# backend/app/ai/prediction.py


from typing import (
    Dict,
    Any,
    List,
    Optional
)

from datetime import datetime


from app.ai.market_analyzer import MarketAnalyzer
from app.ai.trend_engine import TrendEngine
from app.ai.opportunity.opportunity_engine import OpportunityEngine


try:

    from app.ai.smart_money import SmartMoneyAnalyzer
    from app.ai.liquidity import LiquidityEngine
    from app.ai.opportunity.order_blocks import OrderBlocksEngine
    from app.ai.fibonacci import FibonacciAnalyzer
    from app.ai.news_ai import NewsAnalyzer

except Exception:

    SmartMoneyAnalyzer = None
    LiquidityEngine = None
    OrderBlocksEngine = None
    FibonacciAnalyzer = None
    NewsAnalyzer = None



class PredictionEngine:
    """
    FalconAI Prediction Engine V2

    Advanced AI Fusion Layer

    مسؤول عن:

    - دمج جميع محركات التحليل
    - حساب احتمالية الاتجاه
    - كشف الانعكاس
    - كشف الاختراقات
    - تقييم جودة الإشارة
    - بناء قرار قابل للشرح
    - التكيف مع حالة السوق
    """



    def __init__(self):


        # =========================================
        # Core Engines
        # =========================================


        self.market = MarketAnalyzer()

        self.trend = TrendEngine()

        self.opportunity = OpportunityEngine()



        # =========================================
        # Intelligence Modules
        # =========================================


        self.smart_money = (

            SmartMoneyAnalyzer()

            if SmartMoneyAnalyzer

            else None

        )


        self.liquidity = (

            LiquidityEngine()

            if LiquidityEngine

            else None

        )


        self.order_blocks = (

            OrderBlocksEngine()

            if OrderBlocksEngine

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



        # =========================================
        # Dynamic Configuration
        # =========================================


        self.base_confidence = 50


        self.minimum_signal_confidence = 60


        self.maximum_confidence = 100



        self.allow_counter_trend = False



        # =========================================
        # Adaptive Weights
        # =========================================


        self.weights = {


            "trend": 0.20,


            "opportunity": 0.15,


            "smart_money": 0.15,


            "momentum": 0.10,


            "volume": 0.10,


            "liquidity": 0.10,


            "order_blocks": 0.05,


            "fibonacci": 0.05,


            "news": 0.05,


            "market_state": 0.05

        }



        # =========================================
        # Performance Memory
        # =========================================


        self.performance = {


            "signals": 0,


            "correct": 0,


            "failed": 0,


            "accuracy": 0

        }



        self.version = (

            "FalconAI Prediction Engine V2"

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


        return self.fusion_prediction(

            symbol=symbol,

            market=market,

            interval=interval,

            market_data=market_data,

            trend_data=trend_data,

            opportunity=opportunity,

            economic_event=economic_event

        )



    # =====================================================
    # AI FUSION PREDICTION
    # =====================================================


    def fusion_prediction(

        self,

        symbol,

        market,

        interval,

        market_data,

        trend_data,

        opportunity,

        economic_event=None

    ):


        bullish_score = 0

        bearish_score = 0


        reasons = []

        conflicts = []



        # =========================================
        # Dynamic Market Values
        # =========================================


        trend_score = trend_data.get(

            "score",

            0

        )


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



        rsi = market_data.get(

            "rsi",

            50

        )



        opportunity_signal = opportunity.get(

            "signal",

            "WAIT"

        )


        opportunity_confidence = opportunity.get(

            "confidence",

            0

        )



        # =========================================
        # TREND INTELLIGENCE
        # =========================================


        trend_power = min(

            abs(trend_score),

            100

        )



        if trend_score > 0:


            bullish_score += (

                trend_power *

                self.weights["trend"]

            )


            reasons.append(

                "Trend Engine يدعم الاتجاه الصاعد"

            )



        elif trend_score < 0:


            bearish_score += (

                trend_power *

                self.weights["trend"]

            )


            reasons.append(

                "Trend Engine يدعم الاتجاه الهابط"

            )



        # =========================================
        # OPPORTUNITY INTELLIGENCE
        # =========================================


        if opportunity_signal == "BUY":


            bullish_score += (

                opportunity_confidence *

                self.weights["opportunity"]

            )


            reasons.append(

                "Opportunity Engine إيجابي"

            )



        elif opportunity_signal == "SELL":


            bearish_score += (

                opportunity_confidence *

                self.weights["opportunity"]

            )


            reasons.append(

                "Opportunity Engine سلبي"

            )



        # =========================================
        # MOMENTUM
        # =========================================


        momentum_power = min(

            abs(momentum),

            100

        )



        if momentum > 0:


            bullish_score += (

                momentum_power *

                self.weights["momentum"]

            )


            reasons.append(

                "الزخم يدعم الصعود"

            )



        elif momentum < 0:


            bearish_score += (

                momentum_power *

                self.weights["momentum"]

            )


            reasons.append(

                "الزخم يدعم الهبوط"

            )



        # =========================================
        # VOLUME INTELLIGENCE
        # =========================================


        if volume > 1:


            bullish_score += (

                min(volume * 20, 100)

                *

                self.weights["volume"]

            )


            reasons.append(

                "حجم التداول فوق الطبيعي"

            )



        elif volume < 0.8:


            conflicts.append(

                "ضعف حجم التداول"

            )



        # =========================================
        # RSI ADAPTIVE ANALYSIS
        # =========================================


        dynamic_rsi_low = 35

        dynamic_rsi_high = 65



        if volatility > 3:

            dynamic_rsi_low = 30

            dynamic_rsi_high = 70



        if rsi <= dynamic_rsi_low:


            bullish_score += 8


            reasons.append(

                "RSI يعطي احتمال انعكاس صعودي"

            )



        elif rsi >= dynamic_rsi_high:


            bearish_score += 8


            reasons.append(

                "RSI يعطي ضغط بيعي"

            )



        # =========================================
        # MARKET REGIME
        # =========================================


        market_regime = self.detect_market_regime(

            market_data,

            trend_data

        )



        return self.build_prediction_result(

            symbol,

            market,

            interval,

            bullish_score,

            bearish_score,

            reasons,

            conflicts,

            market_regime

        )



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
    # BUILD FINAL PREDICTION RESULT
    # =====================================================


    def build_prediction_result(

        self,

        symbol,

        market,

        interval,

        bullish_score,

        bearish_score,

        reasons,

        conflicts,

        market_regime

    ):


        total_score = (

            bullish_score +

            bearish_score

        )



        if total_score <= 0:


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




        if bullish_probability > bearish_probability:


            direction = "BULLISH"


        elif bearish_probability > bullish_probability:


            direction = "BEARISH"


        else:


            direction = "NEUTRAL"



        signal = "WAIT"



        if bullish_probability >= self.minimum_signal_confidence:


            signal = "BUY"



        elif bearish_probability >= self.minimum_signal_confidence:


            signal = "SELL"




        confidence = self.calculate_confidence(

            bullish_probability,

            bearish_probability,

            conflicts

        )



        quality = self.signal_quality(

            confidence,

            len(conflicts)

        )



        return {


            "symbol": symbol,


            "market": market,


            "interval": interval,


            "signal": signal,


            "direction": direction,


            "confidence": confidence,


            "probability": {


                "bullish":

                    round(

                        bullish_probability,

                        2

                    ),


                "bearish":

                    round(

                        bearish_probability,

                        2

                    )

            },


            "quality": quality,


            "market_regime": market_regime,


            "reasons": reasons,


            "conflicts": conflicts,


            "scores": {


                "bullish":

                    round(

                        bullish_score,

                        2

                    ),


                "bearish":

                    round(

                        bearish_score,

                        2

                    )

            },


            "created_at":

                datetime.utcnow().isoformat()

        }



    # =====================================================
    # ADVANCED CONFIDENCE CALIBRATION
    # =====================================================


    def calculate_confidence(

        self,

        bullish_probability,

        bearish_probability,

        conflicts

    ):


        difference = abs(

            bullish_probability -

            bearish_probability

        )



        confidence = difference



        conflict_penalty = (

            len(conflicts) *

            7

        )



        confidence -= conflict_penalty



        if confidence > self.maximum_confidence:


            confidence = self.maximum_confidence



        if confidence < 0:


            confidence = 0



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
    # SMART MONEY INTELLIGENCE
    # =====================================================


    def analyze_smart_money(

        self,

        symbol,

        interval

    ):


        if not self.smart_money:


            return {


                "available": False

            }



        try:


            return self.smart_money.analyze(

                symbol,

                interval

            )


        except Exception:


            return {


                "available": False,

                "error": "Smart Money unavailable"

            }



    # =====================================================
    # LIQUIDITY INTELLIGENCE
    # =====================================================


    def analyze_liquidity(

        self,

        candles

    ):


        if not self.liquidity:


            return {


                "available": False

            }



        try:


            return self.liquidity.analyze(

                candles

            )


        except Exception:


            return {


                "available": False

            }



    # =====================================================
    # ORDER BLOCK INTELLIGENCE
    # =====================================================


    def analyze_order_blocks(

        self,

        candles

    ):


        if not self.order_blocks:


            return {


                "available": False

            }



        try:


            return self.order_blocks.analyze(

                candles

            )


        except Exception:


            return {


                "available": False

        }



    # =====================================================
    # FIBONACCI INTELLIGENCE
    # =====================================================


    def analyze_fibonacci(

        self,

        symbol,

        interval

    ):


        if not self.fibonacci:


            return {


                "available": False

            }



        try:


            return self.fibonacci.analyze(

                symbol,

                interval

            )


        except Exception:


            return {


                "available": False

            }



    # =====================================================
    # NEWS INTELLIGENCE
    # =====================================================


    def analyze_news(

        self,

        symbol

    ):


        if not self.news:


            return {


                "available": False

            }



        try:


            return self.news.analyze(

                symbol

            )


        except Exception:


            return {


                "available": False

            }



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


            score += 20


            reasons.append(

                "بداية زخم صاعد"

            )


        elif momentum < 0:


            score -= 20


            reasons.append(

                "بداية ضعف زخم"

            )



        if volume > 1.5:


            score += 25


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



        return {


            "direction":

                "UP"

                if score > 0

                else

                "DOWN"

                if score < 0

                else

                "NONE",


            "score": score,


            "probability": probability,


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

                "تحول زخم ضد الاتجاه"

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
    # BREAKOUT INTELLIGENCE
    # =====================================================


    def breakout_probability(

        self,

        candles: List[Dict[str, Any]]

    ):


        if len(candles) < 30:


            return {


                "probability": 0,


                "type": "NONE"

            }



        closes = [

            c.get(

                "close",

                0

            )

            for c in candles

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


                "probability": 70,


                "type": "BULLISH",


                "reason":

                    "اختراق مقاومة"

            }



        if price <= support:


            return {


                "probability": 70,


                "type": "BEARISH",


                "reason":

                    "كسر دعم"

            }



        return {


            "probability": 0,


            "type": "NONE"

        }



    # =====================================================
    # ADAPTIVE LEARNING UPDATE
    # =====================================================


    def update_weights(

        self,

        result: Dict[str, Any]

    ):


        success = result.get(

            "success",

            False

        )


        adjustment = 0.01


        for key in self.weights:


            if success:


                self.weights[key] += adjustment


            else:


                self.weights[key] -= adjustment



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


    def health_check(self):


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


                "order_blocks":

                    self.order_blocks is not None,


                "fibonacci":

                    self.fibonacci is not None,


                "news":

                    self.news is not None,


                "adaptive_learning":

                    True

            }

            }
