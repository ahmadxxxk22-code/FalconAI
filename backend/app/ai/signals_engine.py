from datetime import datetime
from typing import Dict, Any, Optional

from app.ai.market_analyzer import MarketAnalyzer
from app.ai.trend_engine import TrendEngine
from app.ai.patterns import PatternAnalyzer
from app.ai.smart_money import SmartMoneyAnalyzer
from app.ai.prediction import PredictionEngine
from app.ai.risk_manager import RiskManager
from app.ai.news_ai import NewsAnalyzer
from app.ai.fibonacci import FibonacciAnalyzer

from app.ai.opportunity.opportunity_engine import OpportunityEngine
from app.ai.multi_timeframe_engine import MultiTimeframeEngine

from app.ai.opportunity.volume_engine import VolumeEngine
from app.ai.opportunity.liquidity_engine import LiquidityEngine
from app.ai.opportunity.order_blocks import OrderBlocksEngine
from app.ai.opportunity.candles_ai import CandlesAI
from app.ai.opportunity.historical_learning import HistoricalLearning

try:
    from app.ai.economic_calendar import EconomicCalendar
except Exception:
    EconomicCalendar = None


# =====================================================
# FALCONAI SIGNAL ENGINE V3 PRODUCTION
# =====================================================

class SignalEngine:

    """
    FalconAI Institutional Grade AI
    """

    def __init__(self):

        # =================================================
        # CORE ENGINES
        # =================================================

        self.market = MarketAnalyzer()
        self.trend = TrendEngine()
        self.patterns = PatternAnalyzer()
        self.smart_money = SmartMoneyAnalyzer()
        self.prediction = PredictionEngine()
        self.risk = RiskManager()
        self.news = NewsAnalyzer()
        self.fibonacci = FibonacciAnalyzer()

        # =================================================
        # OPPORTUNITY
        # =================================================

        self.opportunity = OpportunityEngine()
        self.multi_timeframe = MultiTimeframeEngine()
        self.volume = VolumeEngine()
        self.liquidity = LiquidityEngine()
        self.order_blocks = OrderBlocksEngine()
        self.candles_ai = CandlesAI()
        self.history = HistoricalLearning()

        # =================================================
        # ECONOMIC
        # =================================================

        self.enable_economic_filter = True

        if EconomicCalendar:
            self.economic = EconomicCalendar()
        else:
            self.economic = None

        # =================================================
        # FALCONAI PRODUCTION FILTERS
        # =================================================



        # =================================================
        # MULTI TIMEFRAME CONFIGURATION
        # =================================================

        self.timeframes = [

            "1m",

            "3m",

            "5m",

            "15m",

            "30m",

            "45m",

            "1h",

            "2h",

            "4h",

            "6h",

            "8h",

            "12h",

            "1d",

            "3d",

            "1w",

            "1M"

        ]

        self.minimum_confidence = 60

        self.minimum_confirmations = 4

        self.maximum_confidence = 100

        self.minimum_score = 45

        self.maximum_score = 100

        self.reject_conflicting_signals = True

        
        # =================================================
        # ENGINE STATE
        # =================================================

        self.version = "V3_PRODUCTION"

        self.active = True

        self.last_signal = None

        self.analysis_count = 0

        self.error_count = 0


# ==========================================================
# SIGNAL QUALITY VALIDATION ENGINE
# Part 1
# ==========================================================

    def validate_signal_quality(
        self,
        signal: str,
        confidence: float,
        confirmations: int,
        market_regime: str,
        smart_money: dict,
        volume: dict,
        trend: dict
    ):

        result = {
            "accepted": True,
            "quality": "LOW",
            "score": 0,
            "reasons": []
        }

        score = 0

        # ==========================================
        # Confidence
        # ==========================================

        if confidence >= 90:
            score += 30

        elif confidence >= 80:
            score += 25

        elif confidence >= 70:
            score += 20

        elif confidence >= 60:
            score += 10

        else:
            result["accepted"] = False
            result["reasons"].append("Low confidence")

        # ==========================================
        # Confirmations
        # ==========================================

        if confirmations >= 8:
            score += 20

        elif confirmations >= 6:
            score += 15

        elif confirmations >= 4:
            score += 10

        else:
            result["accepted"] = False
            result["reasons"].append("Weak confirmations")

        # ==========================================
        # Market Regime
        # ==========================================

        if market_regime == "TRENDING":
            score += 10

        elif market_regime == "VOLATILE":
            score += 6

        elif market_regime == "RANGING":
            score -= 8

        # ==========================================
        # Smart Money
        # ==========================================

        if smart_money.get("bos"):
            score += 5

        if smart_money.get("choch"):
            score += 5

        if smart_money.get("order_block"):
            score += 5

        if smart_money.get("liquidity_sweep"):
            score += 5

        # ==========================================
        # Volume
        # ==========================================

        if volume.get("score", 0) > 0:
            score += 5

        # ==========================================
        # Trend
        # ==========================================

        if trend.get("signal") == signal:
            score += 10

        result["score"] = score

        if score >= 85:
            result["quality"] = "A+"

        elif score >= 75:
            result["quality"] = "A"

        elif score >= 65:
            result["quality"] = "B"

        elif score >= 50:
            result["quality"] = "C"

        else:
            result["quality"] = "D"

        if result["quality"] == "D":
            result["accepted"] = False
            result["reasons"].append("Quality too low")

        return result



# ==========================================================
# RISK SAFETY GATE
# Part 2
# ==========================================================

    def risk_safety_check(

        self,

        confidence,

        risk,

        market_regime

    ):

        if confidence < 60:
            return False

        if risk.get("risk_level") == "HIGH":
            return False

        if market_regime == "RANGING":
            return False

        return True


# ==========================================================
# MARKET DATA QUALITY VALIDATOR
# Part 2
# ==========================================================

    def validate_market_data_quality(

        self,

        market_data,

        providers_data=None

    ):

        quality_score = 100

        warnings = []

        candles = market_data.get("candles", [])

        price = market_data.get("price", 0)

        volume = market_data.get("volume", 0)

        # ==========================================
        # Candle Validation
        # ==========================================

        candle_count = len(candles)

        if candle_count < 50:

            quality_score -= 30

            warnings.append("Missing candles")

        elif candle_count < 100:

            quality_score -= 15

        # ==========================================
        # Price Validation
        # ==========================================

        if price is None or price <= 0:

            quality_score -= 40

            warnings.append("Invalid price")

        # ==========================================
        # Volume Validation
        # ==========================================

        if volume is None or volume <= 0:

            quality_score -= 20

            warnings.append("Invalid volume")

        # ==========================================
        # Multi Provider Validation
        # ==========================================

        if providers_data:

            prices = []

            for provider in providers_data:

                provider_price = provider.get("price", 0)

                if provider_price > 0:

                    prices.append(provider_price)

            if len(prices) >= 2:

                highest = max(prices)

                lowest = min(prices)

                difference = ((highest - lowest) / lowest) * 100

                if difference > 1:

                    quality_score -= 20

                    warnings.append(
                        "Provider price mismatch"
                    )

        # ==========================================
        # Final Quality
        # ==========================================

        quality_score = max(
            0,
            min(
                quality_score,
                100
            )
        )

        if quality_score >= 90:

            quality = "EXCELLENT"

        elif quality_score >= 75:

            quality = "HIGH"

        elif quality_score >= 60:

            quality = "MEDIUM"

        elif quality_score >= 40:

            quality = "LOW"

        else:

            quality = "VERY_LOW"

        return {

            "quality": quality,

            "score": quality_score,

            "warnings": warnings

        }



# ==========================================================
# MULTI TIMEFRAME ANALYSIS ENGINE
# Part 3
# ==========================================================

    def analyze_all_timeframes(

        self,

        symbol,

        market="crypto"

    ):

        results = {}

        bullish = 0

        bearish = 0

        total_confidence = 0

        completed = 0

        for timeframe in self.timeframes:

            try:

                analysis = self.analyze_market(

                    symbol=symbol,

                    timeframe=timeframe,

                    market=market

                )

                results[timeframe] = analysis

                if analysis.get("signal") == "BUY":
                    bullish += 1

                elif analysis.get("signal") == "SELL":
                    bearish += 1

                total_confidence += analysis.get(
                    "confidence",
                    0
                )

                completed += 1

            except Exception as e:

                results[timeframe] = {

                    "signal": "WAIT",

                    "confidence": 0,

                    "error": str(e)

                }

        average_confidence = (

            total_confidence / completed

            if completed

            else 0
        )



        # ==========================================
        # FINAL DIRECTION
        # ==========================================

        final_signal = "WAIT"

        if bullish > bearish:

            final_signal = "BUY"

        elif bearish > bullish:

            final_signal = "SELL"

        # ==========================================
        # TIMEFRAME AGREEMENT
        # ==========================================

        agreement = 0

        if completed > 0:

            agreement = int(

                max(

                    bullish,

                    bearish

                )

                /

                completed

                * 100

            )

        return {

            "signal": final_signal,

            "agreement": agreement,

            "average_confidence": round(

                average_confidence,

                2

            ),

            "bullish_timeframes": bullish,

            "bearish_timeframes": bearish,

            "completed": completed,

            "results": results

        }


# ==========================================================
# MARKET REGIME DETECTOR
# Part 4
# ==========================================================

    def detect_market_regime(

        self,

        market_data

    ):

        trend = market_data.get(

            "trend",

            {}

        )

        volume = market_data.get(

            "volume",

            {}

        )

        volatility = market_data.get(

            "volatility",

            0

        )

        if (

            trend.get("strength", 0) >= 70

            and

            volatility >= 60

        ):

            return "TRENDING"

        if (

            volatility >= 80

        ):

            return "VOLATILE"

        return "RANGING"



# ==========================================================
# SIGNAL EXPLANATION ENGINE
# Part 5
# ==========================================================

    def explain_signal(

        self,

        signal,

        confidence,

        agreement,

        regime,

        reasons=None

    ):

        explanation = []


        if signal == "BUY":

            explanation.append(
                "Bullish market conditions detected"
            )

        elif signal == "SELL":

            explanation.append(
                "Bearish market conditions detected"
            )

        else:

            explanation.append(
                "No clear market direction"
            )


        explanation.append(

            f"Confidence level: {confidence}%"

        )


        explanation.append(

            f"Timeframe agreement: {agreement}%"

        )


        explanation.append(

            f"Market regime: {regime}"

        )


        if reasons:

            explanation.extend(reasons)


        return {

            "signal": signal,

            "explanation": explanation

        }



# ==========================================================
# RISK GATE SYSTEM
# Part 6
# ==========================================================

    def external_risk_gate(

        self,

        confidence,

        risk_data,

        market_regime

    ):

        risk_level = risk_data.get(

            "risk_level",

            "UNKNOWN"

        )


        if confidence < 70:

            return {

                "allowed": False,

                "reason": "LOW_CONFIDENCE"

            }


        if risk_level == "HIGH":

            return {

                "allowed": False,

                "reason": "HIGH_RISK"

            }


        if market_regime == "RANGING":

            return {

                "allowed": False,

                "reason": "BAD_MARKET_CONDITION"

            }


        return {

            "allowed": True,

            "reason": "PASSED"

        }



# ==========================================================
# HEALTH CHECK
# Part 7
# ==========================================================

    def health_check(

        self

    ):

        components = {

            "market":

                self.market is not None,

            "trend":

                self.trend is not None,

            "patterns":

                self.patterns is not None,

            "risk":

                self.risk is not None,

            "prediction":

                self.prediction is not None,

            "opportunity":

                self.opportunity is not None

        }


        status = all(

            components.values()

        )


        return {

            "status":

                "healthy" if status else "degraded",

            "components":

                components

        }



# ==========================================================
# MAIN SIGNAL ANALYSIS ENGINE
# Part 8
# ==========================================================

    def analyze(

        self,

        symbol,

        market="crypto",

        timeframe="15m"

    ):

        try:


            # ==========================================
            # MARKET ANALYSIS
            # ==========================================

            market_data = self.market.analyze(

                symbol,

                timeframe

            )



            if not market_data:


                return {

                    "signal": "WAIT",

                    "confidence": 0,

                    "reason":

                        "NO_MARKET_DATA"

                }



            # ==========================================
            # MARKET REGIME
            # ==========================================

            market_regime = self.detect_market_regime(

                market_data

            )



            # ==========================================
            # TREND ANALYSIS
            # ==========================================

            trend_result = self.trend.analyze(

                market_data

            )



            # ==========================================
            # PATTERN ANALYSIS
            # ==========================================

            pattern_result = self.patterns.analyze(

                market_data

            )



            # ==========================================
            # SMART MONEY ANALYSIS
            # ==========================================

            smart_money_result = self.smart_money.analyze(

                market_data

            )



            # ==========================================
            # OPPORTUNITY ENGINE
            # ==========================================

            opportunity_result = self.opportunity.analyze(

                symbol,

                market,

                timeframe

            )



            # ==========================================
            # MULTI TIMEFRAME
            # ==========================================

            timeframe_result = self.analyze_all_timeframes(

                symbol,

                market

            )



            # ==========================================
            # PREDICTION ENGINE
            # ==========================================

            prediction_result = self.prediction.predict(

                market_data

            )



            # ==========================================
            # SIGNAL COLLECTION
            # ==========================================


            buy_score = 0

            sell_score = 0


            reasons = []



            # Trend

            if trend_result.get(

                "direction"

            ) == "UP":


                buy_score += 20

                reasons.append(

                    "UPTREND"

                )


            elif trend_result.get(

                "direction"

            ) == "DOWN":


                sell_score += 20

                reasons.append(

                    "DOWNTREND"

                )



            # Smart Money

            if smart_money_result.get(

                "bullish"

            ):


                buy_score += 20

                reasons.append(

                    "SMART_MONEY_BUY"

                )



            if smart_money_result.get(

                "bearish"

            ):


                sell_score += 20

                reasons.append(

                    "SMART_MONEY_SELL"

                )



            # Opportunity

            if opportunity_result.get(

                "signal"

            ) == "BUY":


                buy_score += 20


            elif opportunity_result.get(

                "signal"

            ) == "SELL":


                sell_score += 20



            # Prediction

            if prediction_result.get(

                "signal"

            ) == "BUY":


                buy_score += 15


            elif prediction_result.get(

                "signal"

            ) == "SELL":


                sell_score += 15



            # ==========================================
            # FINAL SIGNAL
            # ==========================================


            final_signal = "WAIT"



            if buy_score > sell_score:


                final_signal = "BUY"



            elif sell_score > buy_score:


                final_signal = "SELL"



            total_score = max(

                buy_score,

                sell_score

            )



            confidence = min(

                total_score,

                100

            )



            # ==========================================
            # RISK CHECK
            # ==========================================


            risk_result = self.risk.analyze(

                market_data

            )



            risk_gate = self.external_risk_gate(

                confidence,

                risk_result,

                market_regime

            )



            if not risk_gate["allowed"]:


                final_signal = "WAIT"



                reasons.append(

                    risk_gate["reason"]

                )



            # ==========================================
            # EXPLANATION
            # ==========================================


            explanation = self.explain_signal(

                final_signal,

                confidence,

                timeframe_result.get(

                    "agreement",

                    0

                ),

                market_regime,

                reasons

            )



            return {


                "symbol":

                    symbol,


                "timeframe":

                    timeframe,


                "signal":

                    final_signal,


                "confidence":

                    confidence,


                "market_regime":

                    market_regime,


                "buy_score":

                    buy_score,


                "sell_score":

                    sell_score,


                "risk":

                    risk_result,


                "timeframes":

                    timeframe_result,


                "smart_money":

                    smart_money_result,


                "opportunity":

                    opportunity_result,


                "prediction":

                    prediction_result,


                "explanation":

                    explanation


            }



        except Exception as e:


            return {


                "signal":

                    "WAIT",


                "confidence":

                    0,


                "error":

                    str(e)

            }



# ==========================================================
# CONFIDENCE CALCULATION ENGINE
# Part 9
# ==========================================================

    def calculate_confidence(

        self,

        buy_score,

        sell_score,

        confirmations=0

    ):

        total = max(

            buy_score,

            sell_score

        )


        confidence = total


        if confirmations >= 8:

            confidence += 10


        elif confirmations >= 5:

            confidence += 5



        return min(

            max(

                confidence,

                0

            ),

            100

        )



# ==========================================================
# FINAL DECISION ENGINE
# Part 10
# ==========================================================

    def make_decision(

        self,

        buy_score,

        sell_score,

        confidence

    ):


        signal = "WAIT"



        if confidence < self.minimum_confidence:

            return {

                "signal": "WAIT",

                "confidence": confidence,

                "reason": "LOW_CONFIDENCE"

            }



        if buy_score > sell_score:

            signal = "BUY"



        elif sell_score > buy_score:

            signal = "SELL"



        return {

            "signal": signal,

            "confidence": confidence,

            "buy_score": buy_score,

            "sell_score": sell_score

        }
