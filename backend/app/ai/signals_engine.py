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

        self.minimum_confidence = 80

        self.minimum_alert_confidence = 85

        self.minimum_trend_confidence = 92

        self.minimum_strong_trend = 95

        self.maximum_confidence = 100

        self.minimum_signal_score = 10

        self.allow_counter_trend = False

        self.minimum_trend_strength = 75

        self.minimum_mtf_confidence = 85

        self.minimum_prediction_confidence = 80

        self.minimum_volume_confidence = 75

        self.minimum_liquidity_confidence = 75

        self.minimum_smart_money_confidence = 80

        self.minimum_history_confidence = 75

        self.minimum_orderblock_confidence = 75

        self.minimum_fibonacci_confidence = 75

        self.minimum_news_confidence = 70

        self.minimum_macro_confidence = 70

        self.minimum_data_quality = "GOOD"

        # =================================================
        # QUALITY PROTECTION
        # =================================================

        self.enable_quality_gate = True
        self.enable_duplicate_protection = True
        self.enable_confidence_gate = True
        self.enable_signal_validation = True

        self.enable_news_filter = True
        self.enable_economic_filter = True
        self.enable_fibonacci_filter = True
        self.enable_smart_money_filter = True
        self.enable_volume_filter = True
        self.enable_liquidity_filter = True
        self.enable_orderblock_filter = True
        self.enable_candle_filter = True
        self.enable_history_filter = True
        self.enable_mtf_filter = True

        self.enable_counter_trend_block = True
        self.enable_false_trend_filter = True
        self.enable_fake_breakout_filter = True
        self.enable_confirmation_filter = True

        # =================================================
        # AI WEIGHTS
        # =================================================

        self.weights = {

            "trend": 15,
            "multi_timeframe": 15,
            "prediction": 12,
            "smart_money": 12,
            "market": 8,
            "economic": 8,
            "news": 7,
            "fibonacci": 6,
            "volume": 5,
            "liquidity": 4,
            "order_blocks": 4,
            "candles": 2,
            "history": 2

        }

        # =================================================
        # STATISTICS
        # =================================================

        self.signal_statistics = {

            "buy": 0,
            "sell": 0,
            "wait": 0,
            "trend": 0,
            "success": 0,
            "failed": 0

        }

        self.version = "FalconAI Production V3"



# =====================================================
# MAIN AI SIGNAL ANALYSIS
# =====================================================

    def analyze(
        self,
        symbol: str = "BTCUSDT",
        interval: str = "1h",
        market: str = "crypto",
        economic_event: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        signal_id = (
            f"{symbol}_"
            f"{interval}_"
            f"{datetime.utcnow().timestamp()}"
        )

        # =================================================
        # MARKET DATA
        # =================================================

        market_data = self.market.analyze(
            symbol=symbol,
            interval=interval,
            market=market
        )

        candles = market_data.get(
            "candles",
            []
        )

        data_quality = self.evaluate_data_quality(
            candles
        )

        # =================================================
        # QUALITY GATE
        # =================================================

        if self.enable_quality_gate:

            if data_quality.get("quality") in [
                "LOW",
                "WEAK"
            ]:

                return {
                    "signal": "WAIT",
                    "confidence": 0,
                    "reason": "LOW_DATA_QUALITY",
                    "quality": data_quality,
                    "created_at":
                        datetime.utcnow().isoformat()
                }

        # =================================================
        # OPPORTUNITY MODULES
        # =================================================

        volume_analysis = self.volume.analyze(candles)

        liquidity_analysis = self.liquidity.analyze(candles)

        order_blocks_analysis = self.order_blocks.analyze(candles)

        candle_analysis = self.candles_ai.analyze(candles)

        historical_analysis = self.history.analyze(candles)

        # =================================================
        # CORE AI
        # =================================================

        trend = self.trend.analyze(
            symbol=symbol,
            interval=interval,
            market=market
        )

        multi_timeframe = self.multi_timeframe.analyze(
            symbol=symbol,
            market=market
        )

        opportunity = self.opportunity.analyze(
            symbol=symbol,
            candles=candles
        )

        smart_money = self.smart_money.analyze(
            symbol,
            interval
        )

        prediction = self.prediction.predict(
            symbol=symbol,
            interval=interval,
            market=market
        )

        patterns = self.patterns.analyze(
            symbol,
            interval
        )

        fibonacci = self.fibonacci.analyze(
            symbol,
            interval
        )

        news = self.news.analyze(
            symbol
               )



        # =================================================
        # ECONOMIC INTELLIGENCE
        # =================================================

        economic = {
            "available": False,
            "risk": "UNKNOWN",
            "confidence": 0
        }

        if (
            self.enable_economic_filter
            and
            self.economic
        ):
            economic = self.economic.analyze(
                economic_event
            )

        # =================================================
        # MARKET REGIME
        # =================================================

        market_regime = self.detect_market_regime(
            market_data,
            trend,
            multi_timeframe
        )

        # =================================================
        # EARLY TREND DETECTION
        # =================================================

        early_trend = self.detect_early_trend(
            market_data,
            opportunity,
            smart_money,
            multi_timeframe,
            volume_analysis,
            liquidity_analysis,
            order_blocks_analysis,
            candle_analysis,
            historical_analysis
        )

        # =================================================
        # CONFIDENCE FUSION
        # =================================================

        confidence, confidence_details = self.calculate_confidence(

            trend,

            multi_timeframe,

            opportunity,

            smart_money,

            prediction,

            market_data,

            fibonacci,

            news,

            patterns,

            volume_analysis,

            liquidity_analysis,

            order_blocks_analysis,

            candle_analysis,

            historical_analysis,

            economic

        )

        # =================================================
        # TREND PROTECTION
        # =================================================

        trend_allowed = (

            confidence >= self.minimum_trend_confidence

            and

            trend.get(
                "strength",
                0
            ) >= self.minimum_trend_strength

            and

            multi_timeframe.get(
                "confidence",
                0
            ) >= self.minimum_mtf_confidence

            and

            smart_money.get(
                "confidence",
                0
            ) >= self.minimum_smart_money_confidence

            and

            volume_analysis.get(
                "confidence",
                0
            ) >= self.minimum_volume_confidence

            and

            liquidity_analysis.get(
                "confidence",
                0
            ) >= self.minimum_liquidity_confidence

            and

            order_blocks_analysis.get(
                "confidence",
                0
            ) >= self.minimum_orderblock_confidence

            and

            fibonacci.get(
                "confidence",
                0
            ) >= self.minimum_fibonacci_confidence

            and

            historical_analysis.get(
                "confidence",
                0
            ) >= self.minimum_history_confidence

            and

            economic.get(
                "risk",
                "LOW"
            ) not in [

                "HIGH",

                "EXTREME"

            ]

        )



        # =================================================
        # FINAL AI DECISION
        # =================================================

        decision = self.make_decision(

            trend,

            multi_timeframe,

            opportunity,

            smart_money,

            prediction,

            market_data,

            fibonacci,

            news,

            early_trend,

            volume_analysis,

            liquidity_analysis,

            order_blocks_analysis,

            candle_analysis,

            historical_analysis,

            economic,

            market_regime

        )

        direction = decision.get(
            "signal",
            "WAIT"
        )

        # =================================================
        # TREND CERTIFICATION
        # =================================================

        trend_status = "NONE"

        if trend_allowed:

            if confidence >= self.minimum_strong_trend:

                trend_status = "CONFIRMED"

            else:

                trend_status = "POTENTIAL"

        else:

            trend_status = "REJECTED"

            if direction in [
                "BUY",
                "SELL"
            ]:

                direction = "WAIT"

                decision["signal"] = "WAIT"

                decision["warnings"] = decision.get(
                    "warnings",
                    []
                ) + [
                    "Trend confirmation failed"
                ]

        # =================================================
        # RISK MANAGEMENT
        # =================================================

        risk = self.risk.calculate(

            direction=direction,

            price=market_data.get(
                "price",
                0
            ),

            confidence=confidence,

            atr=market_data.get(
                "atr",
                0
            ),

            volatility=market_data.get(
                "volatility",
                0
            ),

            trend_strength=trend.get(
                "strength",
                0
            ),

            market_state=market_regime,

            smart_money=smart_money,

            fibonacci=fibonacci,

            market=market

        )




        # =================================================
        # ECONOMIC INTELLIGENCE
        # =================================================

        economic = {
            "available": False,
            "risk": "UNKNOWN",
            "confidence": 0
        }

        if (
            self.enable_economic_filter
            and
            self.economic
        ):
            economic = self.economic.analyze(
                economic_event
            )

        # =================================================
        # MARKET REGIME
        # =================================================

        market_regime = self.detect_market_regime(
            market_data,
            trend,
            multi_timeframe
        )

        # =================================================
        # EARLY TREND DETECTION
        # =================================================

        early_trend = self.detect_early_trend(
            market_data,
            opportunity,
            smart_money,
            multi_timeframe,
            volume_analysis,
            liquidity_analysis,
            order_blocks_analysis,
            candle_analysis,
            historical_analysis
        )

        # =================================================
        # CONFIDENCE FUSION
        # =================================================

        confidence, confidence_details = self.calculate_confidence(

            trend,

            multi_timeframe,

            opportunity,

            smart_money,

            prediction,

            market_data,

            fibonacci,

            news,

            patterns,

            volume_analysis,

            liquidity_analysis,

            order_blocks_analysis,

            candle_analysis,

            historical_analysis,

            economic

        )

        # =================================================
        # TREND PROTECTION
        # =================================================

        trend_allowed = (

            confidence >= self.minimum_trend_confidence

            and

            trend.get(
                "strength",
                0
            ) >= self.minimum_trend_strength

            and

            multi_timeframe.get(
                "confidence",
                0
            ) >= self.minimum_mtf_confidence

            and

            smart_money.get(
                "confidence",
                0
            ) >= self.minimum_smart_money_confidence

            and

            volume_analysis.get(
                "confidence",
                0
            ) >= self.minimum_volume_confidence

            and

            liquidity_analysis.get(
                "confidence",
                0
            ) >= self.minimum_liquidity_confidence

            and

            order_blocks_analysis.get(
                "confidence",
                0
            ) >= self.minimum_orderblock_confidence

            and

            fibonacci.get(
                "confidence",
                0
            ) >= self.minimum_fibonacci_confidence

            and

            historical_analysis.get(
                "confidence",
                0
            ) >= self.minimum_history_confidence

            and

            economic.get(
                "risk",
                "LOW"
            ) not in [

                "HIGH",

                "EXTREME"

            ]

        )



        # =================================================
        # FINAL REPORT
        # =================================================

        report = {

            "signal_id":
                signal_id,

            "engine":
                self.version,

            "symbol":
                symbol,

            "interval":
                interval,

            "market":
                market,

            "signal":
                direction,

            "trend_status":
                trend_status,

            "market_regime":
                market_regime,

            "confidence":
                confidence,

            "confidence_details":
                confidence_details,

            "decision":
                decision,

            "risk":
                risk,

            "quality":
                data_quality,

            "economic":
                economic,

            "modules": {

                "market":
                    market_data,

                "trend":
                    trend,

                "multi_timeframe":
                    multi_timeframe,

                "opportunity":
                    opportunity,

                "smart_money":
                    smart_money,

                "prediction":
                    prediction,

                "patterns":
                    patterns,

                "fibonacci":
                    fibonacci,

                "news":
                    news,

                "volume":
                    volume_analysis,

                "liquidity":
                    liquidity_analysis,

                "order_blocks":
                    order_blocks_analysis,

                "candles":
                    candle_analysis,

                "history":
                    historical_analysis

            },

            "created_at":
                datetime.utcnow().isoformat()

        }

        # =================================================
        # SIGNAL STATISTICS
        # =================================================

        if direction == "BUY":

            self.signal_statistics["buy"] += 1

        elif direction == "SELL":

            self.signal_statistics["sell"] += 1

        else:

            self.signal_statistics["wait"] += 1

        if trend_status == "CONFIRMED":

            self.signal_statistics["trend"] += 1

        # =================================================
        # ALERT FILTER
        # =================================================

        report["allow_notification"] = (

            trend_status == "CONFIRMED"

            and

            confidence >= self.minimum_trend_confidence

        )

        report["allow_mobile_push"] = (

            trend_status == "CONFIRMED"

            and

            confidence >= self.minimum_strong_trend

        )

        report["allow_subscription_signal"] = (

            confidence >= self.minimum_alert_confidence

        )

        return report


# =====================================================
# DATA QUALITY ENGINE
# =====================================================

    def evaluate_data_quality(
        self,
        candles
    ) -> Dict[str, Any]:

        count = len(candles)

        quality = "LOW"

        score = 0

        if count >= 300:

            quality = "EXCELLENT"

            score = 100

        elif count >= 200:

            quality = "VERY_GOOD"

            score = 90

        elif count >= 100:

            quality = "GOOD"

            score = 80

        elif count >= 60:

            quality = "ACCEPTABLE"

            score = 65

        elif count >= 30:

            quality = "WEAK"

            score = 45

        return {

            "quality": quality,

            "score": score,

            "candles": count

            }



# =====================================================
# MARKET REGIME DETECTION
# =====================================================

    def detect_market_regime(
        self,
        market,
        trend,
        multi_timeframe
    ) -> str:

        trend_strength = trend.get(
            "strength",
            trend.get("score", 0)
        )

        mtf = multi_timeframe.get(
            "confidence",
            0
        )

        volatility = market.get(
            "volatility",
            0
        )

        volume = market.get(
            "volume_ratio",
            1
        )

        if (
            trend_strength >= 90
            and
            mtf >= 90
            and
            volume >= 1.3
        ):
            return "STRONG_TREND"

        if (
            trend_strength >= 75
            and
            mtf >= 80
        ):
            return "TRENDING"

        if volatility >= 7:
            return "HIGH_VOLATILITY"

        return "RANGING"


# =====================================================
# EARLY TREND DETECTOR
# =====================================================

    def detect_early_trend(

        self,

        market,

        opportunity,

        smart_money,

        multi_timeframe,

        volume,

        liquidity,

        order_blocks,

        candles,

        history

    ):

        score = 0

        if smart_money.get("signal") == "BUY":
            score += 20

        if smart_money.get("signal") == "SELL":
            score -= 20

        if volume.get("confidence", 0) >= 80:
            score += 10

        if liquidity.get("confidence", 0) >= 80:
            score += 10

        if order_blocks.get("confidence", 0) >= 80:
            score += 10

        if candles.get("confidence", 0) >= 75:
            score += 10

        if history.get("confidence", 0) >= 80:
            score += 15

        if multi_timeframe.get("confidence", 0) >= 85:
            score += 15

        if opportunity.get("confidence", 0) >= 80:
            score += 10

        if score >= 80:
            return "EARLY_BULLISH"

        if score <= -80:
            return "EARLY_BEARISH"

        return "NONE"


# =====================================================
# SIGNAL VALIDATION GATE
# =====================================================

    def validate_signal(

        self,

        confidence,

        trend_status,

        economic,

        news,

        market_regime

    ):

        if confidence < self.minimum_confidence:
            return False

        if trend_status == "REJECTED":
            return False

        if economic.get("risk") in [
            "HIGH",
            "EXTREME"
        ]:
            return False

        if news.get("risk") == "HIGH":
            return False

        if market_regime == "RANGING":
            return False

        return True



# =====================================================
# AI CONFIDENCE FUSION
# =====================================================

    def calculate_confidence(

        self,

        trend,

        multi_timeframe,

        opportunity,

        smart_money,

        prediction,

        market,

        fibonacci,

        news,

        patterns,

        volume,

        liquidity,

        order_blocks,

        candles,

        history,

        economic

    ):

        confidence = 0.0

        details = []

        engines = {

            "trend": trend,

            "multi_timeframe": multi_timeframe,

            "prediction": prediction,

            "smart_money": smart_money,

            "market": market,

            "economic": economic,

            "news": news,

            "fibonacci": fibonacci,

            "volume": volume,

            "liquidity": liquidity,

            "order_blocks": order_blocks,

            "candles": candles,

            "history": history

        }

        for name, engine in engines.items():

            if not engine:
                continue

            weight = self.weights.get(
                name,
                0
            )

            engine_confidence = engine.get(
                "confidence",
                0
            )

            confidence += (
                engine_confidence
                * weight
                / 100
            )

            if engine_confidence >= 80:

                details.append(
                    f"{name}:PASS"
                )

            else:

                details.append(
                    f"{name}:LOW"
                )

        # =============================================
        # HARD FILTERS
        # =============================================

        if trend.get(
            "strength",
            0
        ) < self.minimum_trend_strength:

            confidence -= 20

            details.append(
                "Weak trend"
            )

        if multi_timeframe.get(
            "confidence",
            0
        ) < self.minimum_mtf_confidence:

            confidence -= 15

            details.append(
                "Weak MTF"
            )

        if smart_money.get(
            "confidence",
            0
        ) < self.minimum_smart_money_confidence:

            confidence -= 15

            details.append(
                "Weak SmartMoney"
            )

        if liquidity.get(
            "confidence",
            0
        ) < self.minimum_liquidity_confidence:

            confidence -= 10

        if volume.get(
            "confidence",
            0
        ) < self.minimum_volume_confidence:

            confidence -= 10

        if order_blocks.get(
            "confidence",
            0
        ) < self.minimum_orderblock_confidence:

            confidence -= 10

        if history.get(
            "confidence",
            0
        ) < self.minimum_history_confidence:

            confidence -= 10

        if fibonacci.get(
            "confidence",
            0
        ) < self.minimum_fibonacci_confidence:

            confidence -= 5

        if economic.get(
            "risk",
            ""
        ) in [

            "HIGH",

            "EXTREME"

        ]:

            confidence -= 20

            details.append(
                "Economic Risk"
            )

        confidence = max(
            0,
            min(
                round(confidence),
                100
            )
        )

        return confidence, details



# =====================================================
# FINAL AI DECISION ENGINE
# =====================================================

    def make_decision(

        self,

        trend,

        multi_timeframe,

        opportunity,

        smart_money,

        prediction,

        market,

        fibonacci,

        news,

        early_trend,

        volume,

        liquidity,

        order_blocks,

        candles,

        history,

        economic,

        market_regime

    ):

        buy_score = 0
        sell_score = 0

        reasons = []
        warnings = []

        # ============================================
        # TREND
        # ============================================

        if trend.get("signal") == "BUY":
            buy_score += 15
            reasons.append("Trend Bullish")

        elif trend.get("signal") == "SELL":
            sell_score += 15
            reasons.append("Trend Bearish")

        # ============================================
        # MULTI TIMEFRAME
        # ============================================

        if multi_timeframe.get("signal") == "BUY":
            buy_score += 15

        elif multi_timeframe.get("signal") == "SELL":
            sell_score += 15

        # ============================================
        # SMART MONEY
        # ============================================

        if smart_money.get("signal") == "BUY":
            buy_score += 12
            reasons.append("Smart Money Buy")

        elif smart_money.get("signal") == "SELL":
            sell_score += 12
            reasons.append("Smart Money Sell")

        # ============================================
        # PREDICTION
        # ============================================

        if prediction.get("signal") == "BUY":
            buy_score += 10

        elif prediction.get("signal") == "SELL":
            sell_score += 10

        # ============================================
        # OPPORTUNITY
        # ============================================

        if opportunity.get("signal") == "BUY":
            buy_score += 10

        elif opportunity.get("signal") == "SELL":
            sell_score += 10

        # ============================================
        # FIBONACCI
        # ============================================

        if fibonacci.get("signal") == "BUY":
            buy_score += 6

        elif fibonacci.get("signal") == "SELL":
            sell_score += 6

        # ============================================
        # ORDER BLOCKS
        # ============================================

        if order_blocks.get("signal") == "BUY":
            buy_score += 5

        elif order_blocks.get("signal") == "SELL":
            sell_score += 5

        # ============================================
        # LIQUIDITY
        # ============================================

        if liquidity.get("signal") == "BUY":
            buy_score += 5

        elif liquidity.get("signal") == "SELL":
            sell_score += 5

        # ============================================
        # VOLUME
        # ============================================

        if volume.get("signal") == "BUY":
            buy_score += 5

        elif volume.get("signal") == "SELL":
            sell_score += 5

        # ============================================
        # CANDLE AI
        # ============================================

        if candles.get("signal") == "BUY":
            buy_score += 3

        elif candles.get("signal") == "SELL":
            sell_score += 3

        # ============================================
        # HISTORY
        # ============================================

        if history.get("signal") == "BUY":
            buy_score += 3

        elif history.get("signal") == "SELL":
            sell_score += 3

        # ============================================
        # EARLY TREND
        # ============================================

        if early_trend == "EARLY_BULLISH":
            buy_score += 15

        elif early_trend == "EARLY_BEARISH":
            sell_score += 15

        # ============================================
        # NEWS
        # ============================================

        if news.get("risk") == "HIGH":
            warnings.append("High News Risk")

            buy_score -= 10
            sell_score -= 10

        # ============================================
        # ECONOMIC
        # ============================================

        if economic.get("risk") in [
            "HIGH",
            "EXTREME"
        ]:

            warnings.append("Economic Event")

            buy_score -= 15
            sell_score -= 15

        # ============================================
        # FINAL RESULT
        # ============================================

        signal = "WAIT"

        if buy_score >= self.minimum_signal_score and buy_score > sell_score:
            signal = "BUY"

        elif sell_score >= self.minimum_signal_score and sell_score > buy_score:
            signal = "SELL"

        return {

            "signal": signal,

            "buy_score": buy_score,

            "sell_score": sell_score,

            "market_regime": market_regime,

            "reasons": reasons,

            "warnings": warnings

        }



# =====================================================
# HEALTH CHECK
# =====================================================

    def health_check(self):

        return {

            "engine": self.version,

            "status": "running",

            "minimum_confidence": self.minimum_confidence,

            "minimum_trend_confidence": self.minimum_trend_confidence,

            "minimum_strong_trend": self.minimum_strong_trend,

            "counter_trend_allowed": self.allow_counter_trend,

            "weights": self.weights,

            "statistics": self.signal_statistics,

            "modules": {

                "market": True,

                "trend": True,

                "multi_timeframe": True,

                "prediction": True,

                "smart_money": True,

                "fibonacci": True,

                "patterns": True,

                "volume": True,

                "liquidity": True,

                "order_blocks": True,

                "candles": True,

                "history": True,

                "news": True,

                "economic": self.economic is not None,

                "risk_manager": True

            }

        }


# =====================================================
# RESET STATISTICS
# =====================================================

    def reset_statistics(self):

        self.signal_statistics = {

            "buy": 0,

            "sell": 0,

            "wait": 0,

            "trend": 0,

            "success": 0,

            "failed": 0

        }

        return {

            "status": "reset"

        }


# =====================================================
# ENGINE INFORMATION
# =====================================================

    def info(self):

        return {

            "engine": self.version,

            "release": "FalconAI Production",

            "signal_confidence": self.minimum_confidence,

            "trend_confidence": self.minimum_trend_confidence,

            "confirmed_trend": self.minimum_strong_trend,

            "quality_gate": self.enable_quality_gate,

            "duplicate_protection": self.enable_duplicate_protection,

            "signal_validation": self.enable_signal_validation,

            "economic_filter": self.enable_economic_filter,

            "news_filter": self.enable_news_filter,

            "smart_money_filter": self.enable_smart_money_filter,

            "history_learning": True,

            "multi_timeframe": True,

            "institutional_mode": True

        }



# =====================================================
# MARKET REGIME DETECTION
# =====================================================

    def detect_market_regime(
        self,
        market,
        trend,
        multi_timeframe
    ):

        trend_strength = trend.get(
            "strength",
            trend.get("score", 0)
        )

        mtf = multi_timeframe.get(
            "confidence",
            0
        )

        volatility = market.get(
            "volatility",
            0
        )

        volume_ratio = market.get(
            "volume_ratio",
            1
        )

        spread = market.get(
            "spread_score",
            50
        )

        smart_pressure = market.get(
            "smart_money_pressure",
            0
        )

        if (
            trend_strength >= 95
            and mtf >= 90
            and volume_ratio >= 1.5
            and smart_pressure >= 80
        ):

            return "INSTITUTIONAL_TREND"

        if (
            trend_strength >= 85
            and mtf >= 85
            and volume_ratio >= 1.2
        ):

            return "STRONG_TREND"

        if (
            trend_strength >= 75
            and mtf >= 75
        ):

            return "TRENDING"

        if (
            volatility >= 8
            and spread < 40
        ):

            return "HIGH_VOLATILITY"

        if volatility <= 2:

            return "LOW_VOLATILITY"

        return "RANGING"


# =====================================================
# EARLY TREND AI
# =====================================================

    def detect_early_trend(

        self,

        market,

        opportunity,

        smart_money,

        multi_timeframe,

        volume,

        liquidity,

        order_blocks,

        candles,

        history

    ):

        bullish = 0
        bearish = 0

        if smart_money.get("signal") == "BUY":
            bullish += 20

        elif smart_money.get("signal") == "SELL":
            bearish += 20

        if volume.get("signal") == "BUY":
            bullish += 10

        elif volume.get("signal") == "SELL":
            bearish += 10

        if liquidity.get("signal") == "BUY":
            bullish += 10

        elif liquidity.get("signal") == "SELL":
            bearish += 10

        if order_blocks.get("signal") == "BUY":
            bullish += 10

        elif order_blocks.get("signal") == "SELL":
            bearish += 10

        if candles.get("signal") == "BUY":
            bullish += 10

        elif candles.get("signal") == "SELL":
            bearish += 10

        if history.get("signal") == "BUY":
            bullish += 15

        elif history.get("signal") == "SELL":
            bearish += 15

        if multi_timeframe.get("signal") == "BUY":
            bullish += 15

        elif multi_timeframe.get("signal") == "SELL":
            bearish += 15

        if opportunity.get("signal") == "BUY":
            bullish += 10

        elif opportunity.get("signal") == "SELL":
            bearish += 10

        if bullish >= 90:
            return "EARLY_BULLISH"

        if bearish >= 90:
            return "EARLY_BEARISH"

        return "NONE"



# =====================================================
# DATA QUALITY ENGINE
# =====================================================

    def evaluate_data_quality(
        self,
        candles
    ):

        count = len(candles)

        score = 0

        quality = "LOW"

        if count >= 500:

            score += 40

        elif count >= 300:

            score += 35

        elif count >= 200:

            score += 30

        elif count >= 100:

            score += 20

        else:

            score += 5

        # =============================================
        # Missing Candles
        # =============================================

        missing = 0

        for candle in candles:

            if candle is None:

                missing += 1

        if missing == 0:

            score += 20

        elif missing < 5:

            score += 10

        else:

            score -= 20

        # =============================================
        # Volume Quality
        # =============================================

        valid_volume = 0

        for candle in candles:

            if candle:

                volume = candle.get(
                    "volume",
                    0
                )

                if volume > 0:

                    valid_volume += 1

        volume_ratio = (

            valid_volume /

            max(

                len(candles),

                1

            )

        )

        if volume_ratio >= 0.95:

            score += 20

        elif volume_ratio >= 0.80:

            score += 10

        else:

            score -= 15

        # =============================================
        # Price Quality
        # =============================================

        valid_price = 0

        for candle in candles:

            if candle:

                if candle.get(
                    "close"
                ):

                    valid_price += 1

        price_ratio = (

            valid_price /

            max(

                len(candles),

                1

            )

        )

        if price_ratio >= 0.98:

            score += 20

        elif price_ratio >= 0.90:

            score += 10

        else:

            score -= 20

        # =============================================
        # FINAL QUALITY
        # =============================================

        if score >= 90:

            quality = "EXCELLENT"

        elif score >= 80:

            quality = "VERY_GOOD"

        elif score >= 70:

            quality = "GOOD"

        elif score >= 55:

            quality = "ACCEPTABLE"

        elif score >= 40:

            quality = "WEAK"

        else:

            quality = "LOW"

        return {

            "quality": quality,

            "score": score,

            "candles": count,

            "missing": missing,

            "volume_ratio": round(

                volume_ratio,

                2

            ),

            "price_ratio": round(

                price_ratio,

                2

            )

        }
