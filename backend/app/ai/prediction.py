from typing import Dict, Any, List
from datetime import datetime


from app.ai.market_analyzer import MarketAnalyzer
from app.ai.trend_engine import TrendEngine
from app.ai.opportunity.opportunity_engine import OpportunityEngine


class PredictionEngine:
    """
    FalconAI Advanced Prediction Engine

    مسؤول عن:
    - دمج التحليل الفني
    - تقييم الاتجاه
    - دمج الفرص
    - حساب احتمالية الحركة
    - كشف التضارب
    - إنتاج قرار قابل للشرح
    """

    def __init__(self):

        self.market = MarketAnalyzer()

        self.trend = TrendEngine()

        self.opportunity = OpportunityEngine()


        # أوزان ديناميكية قابلة للتطوير
        self.weights = {

            "trend": 0.25,

            "momentum": 0.15,

            "volume": 0.10,

            "rsi": 0.10,

            "macd": 0.15,

            "opportunity": 0.20,

            "market_state": 0.05

        }


    # ==================================================
    # MAIN PREDICTION PIPELINE
    # ==================================================

    def predict(
        self,
        symbol="BTCUSDT",
        interval="1h",
        market="crypto"
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

        )


        fusion = self.advanced_prediction(

            market_data,

            trend_data,

            opportunity

        )


        return {


            "symbol": symbol,


            "market": market,


            "interval": interval,


            "signal": fusion["signal"],


            "direction": fusion["direction"],


            "confidence": fusion["confidence"],


            "probability": fusion["probability"],


            "quality": fusion["quality"],


            "market_regime": fusion["market_regime"],


            "conflicts": fusion["conflicts"],


            "reasons": fusion["reasons"],


            "price": market_data.get(

                "price",

                0

            ),


            "analysis": {


                "market": market_data,


                "trend": trend_data,


                "opportunity": opportunity

            },


            "created_at": datetime.utcnow().isoformat()

        }


    # ==================================================
    # ADVANCED FUSION
    # ==================================================

    def advanced_prediction(
        self,
        market_data: Dict[str, Any],
        trend_data: Dict[str, Any],
        opportunity: Dict[str, Any]
    ) -> Dict[str, Any]:


        bullish = 0

        bearish = 0


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


        volume = market_data.get(

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



        # ------------------------------
        # Trend
        # ------------------------------

        if trend_score > 0:

            bullish += abs(trend_score) * self.weights["trend"]

            reasons.append(

                "الاتجاه يدعم الصعود"

            )


        elif trend_score < 0:

            bearish += abs(trend_score) * self.weights["trend"]

            reasons.append(

                "الاتجاه يدعم الهبوط"

            )



        # ------------------------------
        # RSI
        # ------------------------------

        if rsi < 35:

            bullish += 10

            reasons.append(

                "RSI منطقة انعكاس صعودي"

            )


        elif rsi > 65:

            bearish += 10

            reasons.append(

                "RSI منطقة ضغط بيعي"

            )



        # ------------------------------
        # MACD
        # ------------------------------

        if macd > 0:

            bullish += abs(macd) * 10

            reasons.append(

                "MACD إيجابي"

            )


        elif macd < 0:

            bearish += abs(macd) * 10

            reasons.append(

                "MACD سلبي"

            )



        # ------------------------------
        # Momentum
        # ------------------------------

        if momentum > 0:

            bullish += abs(momentum) * 8

            reasons.append(

                "الزخم يتحسن"

            )


        elif momentum < 0:

            bearish += abs(momentum) * 8

            reasons.append(

                "الزخم يضعف"

            )



        # ------------------------------
        # Volume
        # ------------------------------

        if volume > 1:

            bullish += 10

            reasons.append(

                "حجم التداول يدعم الحركة"

            )


        elif volume < 0.7:

            bearish += 5

            conflicts.append(

                "ضعف حجم التداول"

            )



        # ------------------------------
        # Opportunity Engine
        # ------------------------------

        if opportunity_signal == "BUY":

            bullish += opportunity_confidence * 0.25

            reasons.append(

                "محرك الفرص يدعم الشراء"

            )


        elif opportunity_signal == "SELL":

            bearish += opportunity_confidence * 0.25

            reasons.append(

                "محرك الفرص يدعم البيع"

            )



        # ------------------------------
        # Conflict Detection
        # ------------------------------

        if rsi < 35 and trend_score < -50:

            conflicts.append(

                "RSI شراء لكن الاتجاه هابط"

            )


        if rsi > 65 and trend_score > 50:

            conflicts.append(

                "RSI ضغط لكن الاتجاه قوي"

            )



        # ------------------------------
        # Market Regime
        # ------------------------------

        market_regime = self.detect_market_regime(

            market_data,

            trend_data

        )



        # ------------------------------
        # Final Scores
        # ------------------------------

        total = bullish + bearish


        if total == 0:

            bullish_probability = 50

            bearish_probability = 50


        else:

            bullish_probability = (

                bullish / total

            ) * 100


            bearish_probability = (

                bearish / total

            ) * 100



        if bullish_probability > bearish_probability:


            direction = "BULLISH"


        elif bearish_probability > bullish_probability:


            direction = "BEARISH"


        else:


            direction = "NEUTRAL"



        # ------------------------------
        # Signal
        # ------------------------------

        signal = "WAIT"



        if bullish_probability >= 65:

            signal = "BUY"



        elif bearish_probability >= 65:

            signal = "SELL"



        # ------------------------------
        # Confidence
        # ------------------------------

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


            "quality": quality,


            "market_regime": market_regime,


            "conflicts": conflicts,


            "reasons": reasons,


            "scores": {


                "bullish": round(

                    bullish,

                    2

                ),


                "bearish": round(

                    bearish,

                    2

                )

            }

        }



        # ==================================================
        # MARKET REGIME DETECTOR
        # ==================================================

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



    # ==================================================
    # ADVANCED CONFIDENCE
    # ==================================================

    def calculate_advanced_confidence(
        self,
        bullish_probability,
        bearish_probability,
        opportunity_confidence,
        conflicts
    ):


        difference = abs(

            bullish_probability -

            bearish_probability

        )


        confidence = (

            difference * 0.6

            +

            opportunity_confidence * 0.4

        )


        # خصم بسبب التعارض

        conflict_penalty = len(conflicts) * 8


        confidence -= conflict_penalty



        if confidence > 100:

            confidence = 100



        if confidence < 0:

            confidence = 0



        return round(

            confidence,

            2

        )



    # ==================================================
    # SIGNAL QUALITY
    # ==================================================

    def signal_quality(
        self,
        confidence,
        conflicts_count
    ):


        if confidence >= 85 and conflicts_count == 0:

            return "VERY_STRONG"



        if confidence >= 70:

            return "STRONG"



        if confidence >= 50:

            return "MEDIUM"



        return "WEAK"



    # ==================================================
    # EXPLAINABLE AI SCORE
    # ==================================================

    def explain_score(
        self,
        prediction
    ):


        explanation = []


        probability = prediction.get(

            "probability",

            {}

        )


        bullish = probability.get(

            "bullish",

            0

        )


        bearish = probability.get(

            "bearish",

            0

        )



        if bullish > bearish:

            explanation.append(

                "معظم المحركات تميل للاتجاه الصاعد"

            )


        elif bearish > bullish:

            explanation.append(

                "معظم المحركات تميل للاتجاه الهابط"

            )


        else:

            explanation.append(

                "السوق غير واضح حالياً"

            )



        conflicts = prediction.get(

            "conflicts",

            []

        )


        if conflicts:

            explanation.extend(

                conflicts

            )



        return explanation



    # ==================================================
    # EARLY MOVE DETECTOR
    # ==================================================

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

            0

        )


        volatility = market_data.get(

            "volatility",

            0

        )



        if momentum > 0:

            score += 20

            reasons.append(

                "Momentum بداية حركة"

            )


        elif momentum < 0:

            score -= 20

            reasons.append(

                "Momentum ضعف الحركة"

            )



        if volume > 1.5:

            score += 25

            reasons.append(

                "دخول حجم تداول قوي"

            )



        if volatility > 2:

            score += 15

            reasons.append(

                "ارتفاع نشاط السوق"

            )



        probability = min(

            abs(score),

            100

        )



        if score > 0:

            direction = "UP"



        elif score < 0:

            direction = "DOWN"



        else:

            direction = "NONE"



        return {


            "direction": direction,


            "probability": probability,


            "score": score,


            "reasons": reasons

        }



    # ==================================================
    # REVERSAL PROBABILITY ENGINE
    # ==================================================

    def reversal_probability(
        self,
        market_data,
        trend_data
    ):


        reversal_score = 0

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


        volume = market_data.get(

            "volume_ratio",

            0

        )



        # Oversold reversal

        if rsi < 30:

            reversal_score += 25

            reasons.append(

                "تشبع بيعي قوي احتمال انعكاس"

            )



        # Overbought reversal

        elif rsi > 70:

            reversal_score -= 25

            reasons.append(

                "تشبع شرائي احتمال تصحيح"

            )



        # Momentum change

        if momentum > 0 and trend_score < 0:

            reversal_score += 20

            reasons.append(

                "تحول زخم ضد الاتجاه"

            )



        elif momentum < 0 and trend_score > 0:

            reversal_score -= 20

            reasons.append(

                "ضعف زخم الاتجاه"

            )



        # Volume confirmation

        if volume > 1.5:

            reversal_score += 15

            reasons.append(

                "حجم قوي يدعم الحركة"

            )



        probability = min(

            abs(reversal_score),

            100

        )



        return {


            "score": reversal_score,


            "probability": probability,


            "reasons": reasons

        }



    # ==================================================
    # BREAKOUT INTELLIGENCE
    # ==================================================

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



        current_price = closes[-1]



        resistance = max(

            closes[-30:]

        )


        support = min(

            closes[-30:]

        )



        probability = 0

        breakout_type = "NONE"

        reasons = []



        if current_price >= resistance:

            probability += 60

            breakout_type = "BULLISH"

            reasons.append(

                "اختبار مقاومة قوية"

            )



        elif current_price <= support:

            probability += 60

            breakout_type = "BEARISH"

            reasons.append(

                "اختبار دعم قوي"

            )



        return {


            "probability": probability,


            "type": breakout_type,


            "reasons": reasons

        }



    # ==================================================
    # ADAPTIVE WEIGHT UPDATE
    # ==================================================

    def update_weights(
        self,
        historical_result: Dict[str, Any]
    ):


        """
        تحديث أوزان المحرك مع نتائج التوقعات السابقة.
        يستخدم لاحقاً مع LearningEngine.
        """

        success = historical_result.get(

            "success",

            False

        )


        if success:

            for key in self.weights:

                self.weights[key] += 0.01



        else:

            for key in self.weights:

                self.weights[key] -= 0.01



        # حماية الأوزان

        for key in self.weights:


            if self.weights[key] > 1:

                self.weights[key] = 1



            if self.weights[key] < 0:

                self.weights[key] = 0



        return self.weights



    # ==================================================
    # FULL AI REPORT
    # ==================================================

    def generate_report(
        self,
        prediction: Dict[str, Any]
    ):


        probability = prediction.get(

            "probability",

            {}

        )


        return {


            "summary": {


                "signal": prediction.get(

                    "signal"

                ),


                "direction": prediction.get(

                    "direction"

                ),


                "confidence": prediction.get(

                    "confidence"

                )

            },


            "probability": probability,


            "quality": prediction.get(

                "quality"

            ),


            "market_regime": prediction.get(

                "market_regime"

            ),


            "explanation": self.explain_score(

                prediction

            ),


            "risk_flags": prediction.get(

                "conflicts",

                []

            )

        }



    # ==================================================
    # HEALTH CHECK
    # ==================================================

    def health_check(self):

        return {


            "engine": "PredictionEngine",


            "status": "running",


            "modules": {


                "market_analyzer": True,


                "trend_engine": True,


                "opportunity_engine": True,


                "adaptive_weights": True,


                "explainable_ai": True,


                "probability_model": True

            }

                }



    # ==================================================
    # FINAL AI DECISION WRAPPER
    # ==================================================

    def final_prediction(
        self,
        symbol="BTCUSDT",
        interval="1h",
        market="crypto",
        smart_money=None,
        liquidity=None,
        order_blocks=None
    ):


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

        )


        prediction = self.advanced_prediction(

            market_data,

            trend_data,

            opportunity

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


        # دمج الحركة المبكرة والانعكاس

        if early_move["probability"] > 70:

            prediction["reasons"].extend(

                early_move["reasons"]

            )


        if reversal["probability"] > 60:

            prediction["reasons"].extend(

                reversal["reasons"]

            )


        prediction["early_move"] = early_move

        prediction["reversal"] = reversal

        prediction["breakout"] = breakout



        return {


            "symbol": symbol,


            "market": market,


            "interval": interval,


            "signal": prediction["signal"],


            "direction": prediction["direction"],


            "confidence": prediction["confidence"],


            "probability": prediction["probability"],


            "quality": prediction["quality"],


            "market_regime": prediction["market_regime"],


            "reasons": prediction["reasons"],


            "conflicts": prediction["conflicts"],


            "early_move": early_move,


            "reversal": reversal,


            "breakout": breakout,


            "market_analysis": market_data,


            "trend_analysis": trend_data,


            "opportunity": opportunity,


            "created_at": datetime.utcnow().isoformat()

                }
