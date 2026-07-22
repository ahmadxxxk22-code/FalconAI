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

            trend_status in [
                "CONFIRMED",
                "POTENTIAL"
            ]

            and

            confidence >= self.minimum_alert_confidence

        )


        return report



# =====================================================
# DATA QUALITY ENGINE
# =====================================================

    def evaluate_data_quality(

        self,

        candles,

        provider_prices=None

    ) -> Dict[str, Any]:


        count = len(candles)


        score = 0


        missing_candles = 0

        valid_volume = 0

        valid_price = 0


        # =================================================
        # CANDLE CHECK
        # =================================================

        for candle in candles:


            if not candle:

                missing_candles += 1

                continue


            # السعر

            close = candle.get(
                "close",
                0
            )


            if close and close > 0:

                valid_price += 1



            # الحجم

            volume = candle.get(
                "volume",
                0
            )


            if volume and volume > 0:

                valid_volume += 1



        candle_quality = (

            100 -

            (

                missing_candles /

                max(count,1)

                * 100

            )

        )


        if candle_quality >= 98:

            score += 25

        elif candle_quality >= 90:

            score += 15

        else:

            score += 0



        # =================================================
        # PRICE QUALITY
        # =================================================

        price_quality = (

            valid_price /

            max(count,1)

        ) * 100



        if price_quality >= 98:

            score += 25

        elif price_quality >= 90:

            score += 15



        # =================================================
        # VOLUME QUALITY
        # =================================================

        volume_quality = (

            valid_volume /

            max(count,1)

        ) * 100



        if volume_quality >= 95:

            score += 20

        elif volume_quality >= 80:

            score += 10



        # =================================================
        # PROVIDER CONSISTENCY
        # =================================================

        provider_consistency = 100


        if provider_prices:


            prices = list(

                provider_prices.values()

            )


            if len(prices) > 1:


                max_price = max(prices)

                min_price = min(prices)


                difference = (

                    abs(max_price - min_price)

                    /

                    max_price

                ) * 100



                provider_consistency = (

                    100 - difference

                )



                if provider_consistency >= 99:

                    score += 30

                elif provider_consistency >= 97:

                    score += 15



        # =================================================
        # FINAL QUALITY
        # =================================================


        if score >= 90:

            quality = "EXCELLENT"


        elif score >= 75:

            quality = "GOOD"


        elif score >= 55:

            quality = "WEAK"


        else:

            quality = "LOW"



        return {


            "quality": quality,


            "score": score,


            "candles": count,


            "missing_candles": missing_candles,


            "price_quality": round(

                price_quality,

                2

            ),


            "volume_quality": round(

                volume_quality,

                2

            ),


            "provider_consistency": round(

                provider_consistency,

                2

            )

        }



# =====================================================
# MARKET REGIME DETECTION
# =====================================================

    def detect_market_regime(

        self,

        market,

        trend,

        multi_timeframe,

        volume_analysis=None

    ) -> str:


        trend_strength = trend.get(

            "strength",

            trend.get(

                "score",

                0

            )

        )


        mtf_confidence = multi_timeframe.get(

            "confidence",

            0

        )


        volatility = market.get(

            "volatility",

            0

        )


        if volume_analysis:

            volume_ratio = volume_analysis.get(

                "volume_ratio",

                market.get(

                    "volume_ratio",

                    1

                )

            )

        else:

            volume_ratio = market.get(

                "volume_ratio",

                1

            )



        # =================================================
        # STRONG TREND
        # =================================================


        if (

            trend_strength >= 95

            and

            mtf_confidence >= 90

            and

            volume_ratio >= 1.3

        ):

            return "STRONG_TREND"



        # =================================================
        # NORMAL TREND
        # =================================================


        if (

            trend_strength >= 75

            and

            mtf_confidence >= 80

        ):

            return "TRENDING"



        # =================================================
        # HIGH VOLATILITY
        # =================================================


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



        if smart_money.get(

            "signal"

        ) == "BUY":

            score += 20



        elif smart_money.get(

            "signal"

        ) == "SELL":

            score -= 20



        if volume.get(

            "confidence",

            0

        ) >= 80:

            score += 10



        if liquidity.get(

            "confidence",

            0

        ) >= 80:

            score += 10



        if order_blocks.get(

            "confidence",

            0

        ) >= 80:

            score += 10



        if candles.get(

            "confidence",

            0

        ) >= 75:

            score += 10



        if history.get(

            "confidence",

            0

        ) >= 80:

            score += 15



        if multi_timeframe.get(

            "confidence",

            0

        ) >= 85:

            score += 15



        if opportunity.get(

            "confidence",

            0

        ) >= 80:

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



        if economic.get(

            "risk"

        ) in [

            "HIGH",

            "EXTREME"

        ]:

            return False



        if news.get(

            "risk"

        ) == "HIGH":

            return False



        # يمنع الإشارات الضعيفة داخل السوق العرضي

        if (

            market_regime == "RANGING"

            and

            confidence < 90

        ):

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
                / sum(self.weights.values())
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
# PRODUCTION MONITORING SYSTEM
# =====================================================

    def production_status(self):

        return {

            "engine":

                self.version,


            "status":

                "ACTIVE",


            "uptime":

                datetime.utcnow().isoformat(),


            "signals_total":

                sum(
                    self.signal_statistics.values()
                ),


            "signals":

                self.signal_statistics,


            "filters":

            {

                "quality":

                    self.enable_quality_gate,


                "confidence":

                    self.enable_confidence_gate,


                "validation":

                    self.enable_signal_validation,


                "trend_protection":

                    self.enable_counter_trend_block,


                "fake_breakout":

                    self.enable_fake_breakout_filter

            },


            "ai_modules":

            {

                "market":

                    True,


                "trend":

                    True,


                "mtf":

                    True,


                "smart_money":

                    True,


                "prediction":

                    True,


                "risk":

                    True,


                "news":

                    True,


                "economic":

                    self.economic is not None

            }

        }



# =====================================================
# DUPLICATE SIGNAL PROTECTION
# =====================================================

    def check_duplicate_signal(

        self,

        symbol,

        signal

    ):


        if not hasattr(

            self,

            "last_signals"

        ):


            self.last_signals = {}



        previous = self.last_signals.get(

            symbol

        )


        if previous == signal:

            return True



        self.last_signals[symbol] = signal


        return False





# =====================================================
# SAVE SIGNAL HISTORY
# =====================================================

    def save_signal_history(

        self,

        report

    ):


        if not hasattr(

            self,

            "signal_history"

        ):


            self.signal_history = []



        self.signal_history.append(

            {

                "symbol":

                    report.get("symbol"),


                "signal":

                    report.get("signal"),


                "confidence":

                    report.get("confidence"),


                "time":

                    datetime.utcnow().isoformat()

            }

        )


        # الاحتفاظ بآخر 1000 إشارة فقط

        if len(self.signal_history) > 1000:


            self.signal_history = (

                self.signal_history[-1000:]

            )


        return True





# =====================================================
# GET SIGNAL HISTORY
# =====================================================

    def get_signal_history(

        self,

        limit=50

    ):


        if not hasattr(

            self,

            "signal_history"

        ):

            return []


        return self.signal_history[-limit:]



# =====================================================
# SIGNAL CONTROL & LEARNING MEMORY V1
# =====================================================

    def process_final_signal(

        self,

        report

    ):


        signal = report.get(

            "signal",

            "WAIT"

        )


        symbol = report.get(

            "symbol"

        )


        confidence = report.get(

            "confidence",

            0

        )


        # =================================================
        # DUPLICATE CHECK
        # =================================================


        if signal in [

            "BUY",

            "SELL"

        ]:


            duplicated = self.check_duplicate_signal(

                symbol,

                signal

            )


            if duplicated:


                report["signal"] = "WAIT"


                report["warning"] = (

                    "Duplicate signal blocked"

                )



        # =================================================
        # FINAL CONFIDENCE GATE
        # =================================================


        if (

            report.get("signal")

            in [

                "BUY",

                "SELL"

            ]

            and

            confidence < self.minimum_confidence

        ):


            report["signal"] = "WAIT"


            report["warning"] = (

                "Confidence below minimum"

            )



        # =================================================
        # SAVE LEARNING HISTORY
        # =================================================


        self.save_signal_history(

            report

        )



        # =================================================
        # UPDATE LAST DECISION
        # =================================================


        self.last_decision = {


            "signal":

                report.get("signal"),


            "confidence":

                confidence,


            "time":

                datetime.utcnow().isoformat()

        }



        return report





# =====================================================
# LAST AI DECISION
# =====================================================

    def get_last_decision(

        self

    ):


        if not hasattr(

            self,

            "last_decision"

        ):


            return {


                "signal":

                    "WAIT",


                "confidence":

                    0

            }


        return self.last_decision



# =====================================================
# TREND CERTIFICATION ENGINE V1
# =====================================================

    def certify_trend(

        self,

        trend,

        multi_timeframe,

        smart_money,

        volume,

        liquidity,

        order_blocks,

        fibonacci,

        history,

        market_regime

    ):


        score = 0

        reasons = []



        # =================================================
        # TREND STRENGTH
        # =================================================


        trend_strength = trend.get(

            "strength",

            0

        )


        if trend_strength >= 95:

            score += 25

            reasons.append(
                "Extreme Trend Strength"
            )


        elif trend_strength >= 85:

            score += 20

            reasons.append(
                "Strong Trend"
            )


        elif trend_strength >= 75:

            score += 10



        # =================================================
        # MULTI TIMEFRAME ALIGNMENT
        # =================================================


        mtf_conf = multi_timeframe.get(

            "confidence",

            0

        )


        if mtf_conf >= 90:

            score += 20

            reasons.append(
                "MTF Confirmed"
            )


        elif mtf_conf >= 80:

            score += 10



        # =================================================
        # SMART MONEY
        # =================================================


        smart_conf = smart_money.get(

            "confidence",

            0

        )


        if smart_conf >= 85:

            score += 15

            reasons.append(
                "Smart Money Confirmed"
            )



        # =================================================
        # MARKET PARTICIPATION
        # =================================================


        if volume.get(

            "confidence",

            0

        ) >= 80:


            score += 10

            reasons.append(
                "Volume Confirmed"
            )



        if liquidity.get(

            "confidence",

            0

        ) >= 80:


            score += 5



        if order_blocks.get(

            "confidence",

            0

        ) >= 80:


            score += 5



        if fibonacci.get(

            "confidence",

            0

        ) >= 80:


            score += 5



        if history.get(

            "confidence",

            0

        ) >= 80:


            score += 5



        # =================================================
        # MARKET REGIME FILTER
        # =================================================


        if market_regime == "INSTITUTIONAL_TREND":

            score += 10

            reasons.append(
                "Institutional Market"
            )


        elif market_regime == "RANGING":

            score -= 20

            reasons.append(
                "Range Market"
            )



        # =================================================
        # FINAL CERTIFICATION
        # =================================================


        status = "REJECTED"


        if score >= 90:

            status = "CONFIRMED"


        elif score >= 70:

            status = "POTENTIAL"



        return {

            "status":

                status,


            "score":

                min(score,100),


            "reasons":

                reasons

            }



# =====================================================
# AI EXPLANATION ENGINE V1
# =====================================================

    def generate_explanation(

        self,

        report

    ):


        signal = report.get(

            "signal",

            "WAIT"

        )


        confidence = report.get(

            "confidence",

            0

        )


        modules = report.get(

            "modules",

            {}

        )


        explanation = []

        strengths = []

        warnings = []



        # =================================================
        # SIGNAL DIRECTION
        # =================================================


        if signal == "BUY":

            explanation.append(

                "AI detected bullish market conditions"

            )


        elif signal == "SELL":

            explanation.append(

                "AI detected bearish market conditions"

            )


        else:

            explanation.append(

                "Market conditions are not strong enough"

            )



        # =================================================
        # TREND REASON
        # =================================================


        trend = modules.get(

            "trend",

            {}

        )


        if trend.get(

            "confidence",

            0

        ) >= 85:


            strengths.append(

                "Strong trend confirmation"

            )



        # =================================================
        # SMART MONEY
        # =================================================


        smart_money = modules.get(

            "smart_money",

            {}

        )


        if smart_money.get(

            "confidence",

            0

        ) >= 80:


            strengths.append(

                "Smart money activity confirmed"

            )



        # =================================================
        # VOLUME
        # =================================================


        volume = modules.get(

            "volume",

            {}

        )


        if volume.get(

            "confidence",

            0

        ) >= 80:


            strengths.append(

                "Volume supports movement"

            )



        # =================================================
        # LIQUIDITY
        # =================================================


        liquidity = modules.get(

            "liquidity",

            {}

        )


        if liquidity.get(

            "confidence",

            0

        ) >= 80:


            strengths.append(

                "Liquidity conditions are healthy"

            )



        # =================================================
        # WARNINGS
        # =================================================


        if confidence < 85:

            warnings.append(

                "Confidence below premium level"

            )



        if report.get(

            "market_regime"

        ) == "RANGING":


            warnings.append(

                "Market is moving sideways"

            )



        return {


            "summary":

                explanation,


            "strengths":

                strengths,


            "warnings":

                warnings,


            "confidence":

                confidence,


            "message":

                (

                    f"FalconAI confidence level: "

                    f"{confidence}%"

                )

        }



# =====================================================
# SURPRISE TREND DETECTOR V1
# =====================================================

    def detect_surprise_trend(

        self,

        market,

        volume,

        liquidity,

        smart_money,

        candles,

        opportunity

    ):


        score = 0

        reasons = []



        # =================================================
        # VOLUME EXPLOSION
        # =================================================


        volume_ratio = volume.get(

            "volume_ratio",

            1

        )


        if volume_ratio >= 2:


            score += 25

            reasons.append(

                "Volume explosion detected"

            )


        elif volume_ratio >= 1.5:


            score += 15



        # =================================================
        # SMART MONEY PRESSURE
        # =================================================


        smart_pressure = smart_money.get(

            "pressure",

            smart_money.get(

                "confidence",

                0

            )

        )


        if smart_pressure >= 90:


            score += 25

            reasons.append(

                "Smart money accumulation detected"

            )


        elif smart_pressure >= 80:


            score += 15



        # =================================================
        # LIQUIDITY MOVEMENT
        # =================================================


        liquidity_conf = liquidity.get(

            "confidence",

            0

        )


        if liquidity_conf >= 90:


            score += 15

            reasons.append(

                "Liquidity movement detected"

            )



        # =================================================
        # CANDLE IMPULSE
        # =================================================


        candle_signal = candles.get(

            "signal",

            "WAIT"

        )


        candle_strength = candles.get(

            "confidence",

            0

        )


        if (

            candle_signal in [

                "BUY",

                "SELL"

            ]

            and

            candle_strength >= 85

        ):


            score += 15

            reasons.append(

                "Strong candle impulse"

            )



        # =================================================
        # OPPORTUNITY ENGINE
        # =================================================


        opportunity_conf = opportunity.get(

            "confidence",

            0

        )


        if opportunity_conf >= 85:


            score += 10

            reasons.append(

                "Opportunity confirmed"

            )



        # =================================================
        # FINAL RESULT
        # =================================================


        status = "NONE"



        if score >= 80:


            status = "SURPRISE_TREND"



        elif score >= 60:


            status = "EARLY_MOVE"



        return {


            "status":

                status,


            "score":

                min(

                    score,

                    100

                ),


            "reasons":

                reasons

        }



# =====================================================
# ADAPTIVE AI LEARNING ENGINE V1
# =====================================================

    def update_learning_result(

        self,

        signal_id,

        result,

        module_scores=None

    ):


        if not hasattr(

            self,

            "learning_memory"

        ):


            self.learning_memory = []



        record = {


            "signal_id":

                signal_id,


            "result":

                result,


            "modules":

                module_scores or {},


            "time":

                datetime.utcnow().isoformat()

        }



        self.learning_memory.append(

            record

        )



        # الاحتفاظ بآخر 5000 نتيجة

        if len(self.learning_memory) > 5000:


            self.learning_memory = (

                self.learning_memory[-5000:]

            )



        if result == "SUCCESS":

            self.signal_statistics["success"] += 1


        elif result == "FAILED":

            self.signal_statistics["failed"] += 1



        return True





# =====================================================
# AI WEIGHT ADAPTATION
# =====================================================

    def adapt_ai_weights(

        self

    ):


        if not hasattr(

            self,

            "learning_memory"

        ):


            return self.weights



        total = len(

            self.learning_memory

        )


        if total < 100:


            return self.weights



        module_success = {}



        for item in self.learning_memory:


            modules = item.get(

                "modules",

                {}

            )


            success = 1 if item.get(

                "result"

            ) == "SUCCESS" else 0



            for name, score in modules.items():


                if name not in module_success:


                    module_success[name] = {


                        "success": 0,


                        "count": 0

                    }



                module_success[name]["success"] += success


                module_success[name]["count"] += 1





        # =================================================
        # ADJUST WEIGHTS
        # =================================================


        for module, data in module_success.items():


            accuracy = (

                data["success"]

                /

                max(

                    data["count"],

                    1

                )

            )



            if module in self.weights:


                if accuracy >= 0.70:


                    self.weights[module] += 1



                elif accuracy <= 0.40:


                    self.weights[module] -= 1





        # منع خروج الأوزان عن الحدود

        for module in self.weights:


            self.weights[module] = max(

                1,

                min(

                    self.weights[module],

                    25

                )

            )



        return self.weights





# =====================================================
# LEARNING STATUS
# =====================================================

    def learning_status(

        self

    ):


        return {


            "memory_size":

                len(

                    getattr(

                        self,

                        "learning_memory",

                        []

                    )

                ),


            "weights":

                self.weights,


            "success":

                self.signal_statistics.get(

                    "success",

                    0

                ),


            "failed":

                self.signal_statistics.get(

                    "failed",

                    0

                )

            }



# =====================================================
# RISK INTELLIGENCE ENGINE V2
# =====================================================

    def calculate_dynamic_risk(

        self,

        direction,

        price,

        confidence,

        atr,

        volatility,

        trend_strength,

        market_regime,

        smart_money,

        fibonacci,

        market

    ):


        risk_level = "MEDIUM"

        risk_score = 50



        # =================================================
        # CONFIDENCE EFFECT
        # =================================================


        if confidence >= 90:

            risk_score -= 20


        elif confidence < 70:

            risk_score += 25



        # =================================================
        # VOLATILITY EFFECT
        # =================================================


        if volatility >= 8:

            risk_score += 25


        elif volatility <= 3:

            risk_score -= 10



        # =================================================
        # TREND EFFECT
        # =================================================


        if trend_strength >= 90:

            risk_score -= 15


        elif trend_strength < 70:

            risk_score += 20



        # =================================================
        # MARKET REGIME
        # =================================================


        if market_regime == "INSTITUTIONAL_TREND":

            risk_score -= 20


        elif market_regime == "RANGING":

            risk_score += 20



        # =================================================
        # FINAL RISK LEVEL
        # =================================================


        risk_score = max(

            0,

            min(

                risk_score,

                100

            )

        )


        if risk_score <= 30:

            risk_level = "LOW"


        elif risk_score <= 60:

            risk_level = "MEDIUM"


        else:

            risk_level = "HIGH"



        # =================================================
        # DYNAMIC SL / TP
        # =================================================


        atr_value = max(

            atr,

            price * 0.005

        )


        stop_distance = atr_value * 1.5


        take_distance = atr_value * 3



        if direction == "BUY":


            stop_loss = price - stop_distance


            take_profit = price + take_distance



        elif direction == "SELL":


            stop_loss = price + stop_distance


            take_profit = price - take_distance



        else:


            stop_loss = 0


            take_profit = 0



        return {


            "risk_level":

                risk_level,


            "risk_score":

                risk_score,


            "stop_loss":

                round(

                    stop_loss,

                    8

                ),


            "take_profit":

                round(

                    take_profit,

                    8

                ),


            "risk_reward":

                2,


            "confidence":

                confidence

        }





# =====================================================
# POSITION SAFETY CHECK
# =====================================================

    def risk_safety_check(

        self,

        confidence,

        risk,

        market_regime

    ):


        if confidence < self.minimum_confidence:

            return False



        if risk.get(

            "risk_level"

        ) == "HIGH":

            return False



        if market_regime == "RANGING":

            return False



        return True



# =====================================================
# ADVANCED DATA QUALITY VALIDATOR V3
# =====================================================

def validate_market_data_quality(
    self,
    candles=None,
    providers_data=None,
    market_data=None
):

    result = {
        "quality": "LOW",
        "score": 0,
        "issues": [],
        "warnings": []
    }

    # =====================================
    # Support both old and new formats
    # =====================================

    if market_data is not None:

        candles = market_data.get(
            "candles",
            candles or []
        )

        price = market_data.get(
            "price",
            0
        )

        volume = market_data.get(
            "volume",
            0
        )

    else:

        price = 0
        volume = 0

    # =====================================
    # Basic validation
    # =====================================

    if not candles:

        result["issues"].append("NO_CANDLES")
        return result

    score = 100

    # =====================================
    # Candle count
    # =====================================

    if len(candles) < 100:

        score -= 25
        result["issues"].append("LOW_HISTORY")

    # =====================================
    # Price validation
    # =====================================

    if price <= 0:

        score -= 15
        result["issues"].append("INVALID_PRICE")

    # =====================================
    # Volume validation
    # =====================================

    if volume < 0:

        score -= 10
        result["issues"].append("INVALID_VOLUME")

    # =====================================
    # Candle integrity
    # =====================================

    for candle in candles:

        high = candle.get("high", 0)
        low = candle.get("low", 0)
        open_price = candle.get("open", 0)
        close = candle.get("close", 0)

        if high < low:

            score -= 3
            result["warnings"].append("HIGH_LOW_ERROR")

        if high < open_price or high < close:

            score -= 2

        if low > open_price or low > close:

            score -= 2

    # =====================================
    # Multi Provider Validation
    # =====================================

    if providers_data:

        valid_prices = []

        for provider in providers_data.values():

            if isinstance(provider, dict):

                p = provider.get("price")

                if isinstance(p, (int, float)):

                    valid_prices.append(p)

        if len(valid_prices) >= 2:

            average = sum(valid_prices) / len(valid_prices)

            deviation = max(

                abs(p - average)

                for p in valid_prices

            )

            if average > 0:

                deviation = deviation / average

                if deviation > 0.02:

                    score -= 20

                    result["warnings"].append(
                        "PROVIDER_PRICE_MISMATCH"
                    )



        # =================================================
        # FINAL QUALITY
        # =================================================


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

            quality = "GOOD"


        elif quality_score >= 50:

            quality = "WEAK"


        else:

            quality = "LOW"



        return {


            "quality":

                quality,


            "score":

                quality_score,


            "warnings":

                warnings

        }





# =====================================================
# DATA PROVIDER STATUS
# =====================================================

    def provider_status(

        self,

        providers

    ):


        status = {}


        for provider in providers:


            status[

                provider

            ] = {


                "active":

                    True,


                "last_check":

                    datetime.utcnow().isoformat()

            }



        return status



# =====================================================
# AI MARKET MEMORY ENGINE V1
# =====================================================

    def save_market_memory(

        self,

        symbol,

        interval,

        market_state,

        signal,

        confidence,

        result=None

    ):


        if not hasattr(

            self,

            "market_memory"

        ):


            self.market_memory = []



        memory = {


            "symbol":

                symbol,


            "interval":

                interval,


            "market_state":

                market_state,


            "signal":

                signal,


            "confidence":

                confidence,


            "result":

                result,


            "time":

                datetime.utcnow().isoformat()

        }



        self.market_memory.append(

            memory

        )



        # الاحتفاظ بآخر 10000 حالة

        if len(

            self.market_memory

        ) > 10000:


            self.market_memory = (

                self.market_memory[-10000:]

            )



        return True





# =====================================================
# HISTORICAL PATTERN MATCHING
# =====================================================

    def find_similar_market_cases(

        self,

        market_state,

        signal=None

    ):


        if not hasattr(

            self,

            "market_memory"

        ):


            return []



        matches = []



        for case in self.market_memory:


            if case.get(

                "market_state"

            ) == market_state:


                if (

                    signal is None

                    or

                    case.get("signal") == signal

                ):


                    matches.append(

                        case

                    )



        return matches[-100:]





# =====================================================
# HISTORICAL CONFIDENCE BOOST
# =====================================================

    def calculate_history_boost(

        self,

        market_state,

        signal

    ):


        cases = self.find_similar_market_cases(

            market_state,

            signal

        )



        if len(cases) < 20:


            return {


                "boost":

                    0,


                "cases":

                    len(cases)

            }



        success = 0



        total = len(

            cases

        )



        for case in cases:


            if case.get(

                "result"

            ) == "SUCCESS":


                success += 1



        accuracy = (

            success

            /

            total

        ) * 100



        boost = 0



        if accuracy >= 75:


            boost = 10


        elif accuracy >= 60:


            boost = 5



        return {


            "boost":

                boost,


            "accuracy":

                round(

                    accuracy,

                    2

                ),


            "cases":

                total

        }





# =====================================================
# MARKET MEMORY STATUS
# =====================================================

    def market_memory_status(

        self

    ):


        return {


            "memory_size":

                len(

                    getattr(

                        self,

                        "market_memory",

                        []

                    )

                ),


            "last_update":

                datetime.utcnow().isoformat()

               }


    

# =====================================================
# NEWS ECONOMIC FILTER
# =====================================================

    def external_risk_gate(

        self,

        

        if not intelligence.get(

            "safe",

            False

        ):


            return False



        if intelligence.get(

            "warnings"

        ):


            if len(

                intelligence["warnings"]

            ) >= 2:


                return False



        return True



# =====================================================
# INSTITUTIONAL SMART MONEY ENGINE V1
# =====================================================

    def analyze_institutional_flow(

        self,

        candles,

        volume,

        liquidity,

        order_blocks

    ):


        bullish = 0

        bearish = 0

        reasons = []



        # =================================================
        # VOLUME PRESSURE
        # =================================================


        volume_signal = volume.get(

            "signal",

            "WAIT"

        )


        volume_conf = volume.get(

            "confidence",

            0

        )


        if volume_signal == "BUY" and volume_conf >= 80:


            bullish += 20


            reasons.append(

                "Institutional buying volume"

            )



        elif volume_signal == "SELL" and volume_conf >= 80:


            bearish += 20


            reasons.append(

                "Institutional selling volume"

            )



        # =================================================
        # LIQUIDITY FLOW
        # =================================================


        liquidity_signal = liquidity.get(

            "signal",

            "WAIT"

        )


        liquidity_conf = liquidity.get(

            "confidence",

            0

        )


        if liquidity_signal == "BUY" and liquidity_conf >= 80:


            bullish += 15


            reasons.append(

                "Liquidity accumulation"

            )



        elif liquidity_signal == "SELL" and liquidity_conf >= 80:


            bearish += 15


            reasons.append(

                "Liquidity distribution"

            )



        # =================================================
        # ORDER BLOCK CONFIRMATION
        # =================================================


        block_signal = order_blocks.get(

            "signal",

            "WAIT"

        )


        block_conf = order_blocks.get(

            "confidence",

            0

        )


        if block_signal == "BUY" and block_conf >= 80:


            bullish += 20


            reasons.append(

                "Bullish order block"

            )



        elif block_signal == "SELL" and block_conf >= 80:


            bearish += 20


            reasons.append(

                "Bearish order block"

            )



        # =================================================
        # CANDLE FLOW ANALYSIS
        # =================================================


        if candles:


            last = candles[-1]


            open_price = last.get(

                "open",

                0

            )


            close_price = last.get(

                "close",

                0

            )


            if close_price > open_price:


                bullish += 5



            elif close_price < open_price:


                bearish += 5



        # =================================================
        # FINAL PRESSURE
        # =================================================


        total = bullish + bearish


        confidence = 0


        if total > 0:


            confidence = (

                max(

                    bullish,

                    bearish

                )

                /

                total

            ) * 100



        signal = "WAIT"


        if bullish > bearish and confidence >= 70:


            signal = "BUY"



        elif bearish > bullish and confidence >= 70:


            signal = "SELL"



        return {


            "signal":

                signal,


            "bullish_pressure":

                bullish,


            "bearish_pressure":

                bearish,


            "confidence":

                round(

                    confidence,

                    2

                ),


            "reasons":

                reasons

        }





# =====================================================
# SMART MONEY STATUS
# =====================================================

    def smart_money_status(

        self

    ):


        return {


            "module":

                "Institutional Flow AI",


            "status":

                "ACTIVE",


            "time":

                datetime.utcnow().isoformat()

            }



# =====================================================
# FALSE BREAKOUT DETECTION ENGINE V1
# =====================================================

    def detect_false_breakout(

        self,

        candles,

        volume,

        liquidity,

        trend

    ):


        if not candles or len(candles) < 20:

            return {

                "false_breakout":

                    False,

                "confidence":

                    0,

                "reason":

                    "NOT_ENOUGH_DATA"

            }



        score = 0

        warnings = []



        # =================================================
        # PRICE BREAK CHECK
        # =================================================


        previous_high = max(

            candle.get(

                "high",

                0

            )

            for candle in candles[-20:-1]

        )


        previous_low = min(

            candle.get(

                "low",

                0

            )

            for candle in candles[-20:-1]

        )


        last_candle = candles[-1]


        close = last_candle.get(

            "close",

            0

        )


        high = last_candle.get(

            "high",

            0

        )


        low = last_candle.get(

            "low",

            0

        )



        breakout_up = close > previous_high

        breakout_down = close < previous_low



        # =================================================
        # VOLUME CONFIRMATION
        # =================================================


        volume_conf = volume.get(

            "confidence",

            0

        )


        volume_signal = volume.get(

            "signal",

            "WAIT"

        )



        if breakout_up:


            if (

                volume_signal != "BUY"

                or

                volume_conf < 70

            ):


                score += 25


                warnings.append(

                    "Weak breakout volume"

                )



        if breakout_down:


            if (

                volume_signal != "SELL"

                or

                volume_conf < 70

            ):


                score += 25


                warnings.append(

                    "Weak breakdown volume"

                )



        # =================================================
        # LIQUIDITY CONFIRMATION
        # =================================================


        liquidity_conf = liquidity.get(

            "confidence",

            0

        )


        if (

            (breakout_up or breakout_down)

            and

            liquidity_conf < 70

        ):


            score += 20


            warnings.append(

                "Liquidity not confirmed"

            )



        # =================================================
        # CANDLE REJECTION
        # =================================================


        candle_body = abs(

            close - last_candle.get(

                "open",

                close

            )

        )


        candle_range = high - low



        if candle_range > 0:


            rejection = (

                candle_range

                -

                candle_body

            ) / candle_range



            if rejection > 0.6:


                score += 25


                warnings.append(

                    "Strong candle rejection"

                )



        # =================================================
        # TREND ALIGNMENT
        # =================================================


        trend_signal = trend.get(

            "signal",

            "WAIT"

        )


        if breakout_up and trend_signal != "BUY":


            score += 15


            warnings.append(

                "Counter trend breakout"

            )



        if breakout_down and trend_signal != "SELL":


            score += 15


            warnings.append(

                "Counter trend breakdown"

            )



        # =================================================
        # FINAL RESULT
        # =================================================


        confidence = min(

            score,

            100

        )


        return {


            "false_breakout":

                confidence >= 60,


            "confidence":

                confidence,


            "warnings":

                warnings

        }





# =====================================================
# BREAKOUT SAFETY FILTER
# =====================================================

    def breakout_validation_gate(

        self,

        breakout_data

    ):


        if not self.enable_fake_breakout_filter:

            return True



        if breakout_data.get(

            "false_breakout",

            False

        ):

            return False



        return True



# =====================================================
# CANDLE INTELLIGENCE ENGINE V2
# =====================================================

    def analyze_candle_patterns(

        self,

        candles

    ):


        if not candles or len(candles) < 5:

            return {

                "signal":

                    "WAIT",

                "confidence":

                    0,

                "patterns":

                    []

            }



        patterns = []

        bullish = 0

        bearish = 0



        current = candles[-1]

        previous = candles[-2]



        current_open = current.get(

            "open",

            0

        )

        current_close = current.get(

            "close",

            0

        )

        current_high = current.get(

            "high",

            0

        )

        current_low = current.get(

            "low",

            0

        )



        previous_open = previous.get(

            "open",

            0

        )

        previous_close = previous.get(

            "close",

            0

        )



        body = abs(

            current_close - current_open

        )


        candle_range = (

            current_high

            -

            current_low

        )



        # =================================================
        # BULLISH ENGULFING
        # =================================================


        if (

            current_close > current_open

            and

            previous_close < previous_open

            and

            current_close > previous_open

            and

            current_open < previous_close

        ):


            bullish += 30

            patterns.append(

                "BULLISH_ENGULFING"

            )



        # =================================================
        # BEARISH ENGULFING
        # =================================================


        if (

            current_close < current_open

            and

            previous_close > previous_open

            and

            current_close < previous_open

            and

            current_open > previous_close

        ):


            bearish += 30

            patterns.append(

                "BEARISH_ENGULFING"

            )



        # =================================================
        # PIN BAR DETECTION
        # =================================================


        if candle_range > 0:


            upper_wick = (

                current_high

                -

                max(

                    current_open,

                    current_close

                )

            )


            lower_wick = (

                min(

                    current_open,

                    current_close

                )

                -

                current_low

            )



            if lower_wick > body * 2:


                bullish += 20

                patterns.append(

                    "BULLISH_PIN_BAR"

                )



            if upper_wick > body * 2:


                bearish += 20

                patterns.append(

                    "BEARISH_PIN_BAR"

                )



        # =================================================
        # STRONG BODY CONFIRMATION
        # =================================================


        if candle_range > 0:


            body_strength = (

                body

                /

                candle_range

            ) * 100



            if body_strength >= 70:


                if current_close > current_open:


                    bullish += 15


                    patterns.append(

                        "STRONG_BULLISH_BODY"

                    )


                elif current_close < current_open:


                    bearish += 15


                    patterns.append(

                        "STRONG_BEARISH_BODY"

                    )



        # =================================================
        # FINAL RESULT
        # =================================================


        total = bullish + bearish


        confidence = 0


        if total > 0:


            confidence = (

                max(

                    bullish,

                    bearish

                )

                /

                total

            ) * 100



        signal = "WAIT"



        if bullish > bearish and confidence >= 70:


            signal = "BUY"



        elif bearish > bullish and confidence >= 70:


            signal = "SELL"



        return {


            "signal":

                signal,


            "confidence":

                round(

                    confidence,

                    2

                ),


            "bullish_score":

                bullish,


            "bearish_score":

                bearish,


            "patterns":

                patterns

        }





# =====================================================
# PATTERN CONFIRMATION GATE
# =====================================================

    def pattern_confirmation_gate(

        self,

        candle_data,

        pattern_data

    ):


        if not self.enable_candle_filter:

            return True



        candle_signal = candle_data.get(

            "signal",

            "WAIT"

        )


        pattern_signal = pattern_data.get(

            "signal",

            "WAIT"

        )



        if (

            candle_signal != "WAIT"

            and

            pattern_signal != "WAIT"

            and

            candle_signal != pattern_signal

        ):


            return False



        return True



# =====================================================
# LIQUIDITY & ORDER BLOCK INTELLIGENCE V2
# =====================================================

    def analyze_liquidity_zones(

        self,

        candles

    ):


        if not candles or len(candles) < 20:


            return {


                "signal":

                    "WAIT",


                "confidence":

                    0,


                "zones":

                    []

            }



        highs = []

        lows = []



        for candle in candles[-20:]:


            highs.append(

                candle.get(

                    "high",

                    0

                )

            )


            lows.append(

                candle.get(

                    "low",

                    0

                )

            )



        resistance = max(

            highs

        )


        support = min(

            lows

        )


        current_price = candles[-1].get(

            "close",

            0

        )



        zones = []


        bullish = 0

        bearish = 0



        # =================================================
        # LIQUIDITY SWEEP DETECTION
        # =================================================


        if current_price > resistance:


            bearish += 20


            zones.append(

                "BUY_SIDE_LIQUIDITY_SWEEP"

            )



        if current_price < support:


            bullish += 20


            zones.append(

                "SELL_SIDE_LIQUIDITY_SWEEP"

            )



        # =================================================
        # SUPPORT LIQUIDITY
        # =================================================


        distance_support = abs(

            current_price - support

        )



        if support > 0:


            if distance_support / support < 0.01:


                bullish += 20


                zones.append(

                    "SUPPORT_LIQUIDITY_ZONE"

                )



        # =================================================
        # RESISTANCE LIQUIDITY
        # =================================================


        distance_resistance = abs(

            resistance - current_price

        )



        if resistance > 0:


            if distance_resistance / resistance < 0.01:


                bearish += 20


                zones.append(

                    "RESISTANCE_LIQUIDITY_ZONE"

                )



        total = bullish + bearish


        confidence = 0


        if total:


            confidence = (

                max(

                    bullish,

                    bearish

                )

                /

                total

            ) * 100



        signal = "WAIT"



        if bullish > bearish and confidence >= 70:


            signal = "BUY"



        elif bearish > bullish and confidence >= 70:


            signal = "SELL"



        return {


            "signal":

                signal,


            "confidence":

                round(

                    confidence,

                    2

                ),


            "zones":

                zones,


            "support":

                support,


            "resistance":

                resistance

        }





# =====================================================
# ORDER BLOCK INTELLIGENCE V2
# =====================================================

    def analyze_order_blocks_v2(

        self,

        candles

    ):


        if not candles or len(candles) < 10:


            return {


                "signal":

                    "WAIT",


                "confidence":

                    0,


                "blocks":

                    []

            }



        blocks = []

        bullish = 0

        bearish = 0



        for candle in candles[-10:]:


            open_price = candle.get(

                "open",

                0

            )


            close_price = candle.get(

                "close",

                0

            )


            volume = candle.get(

                "volume",

                0

            )



            if close_price > open_price and volume:


                bullish += 10


                blocks.append(

                    "BULLISH_ORDER_FLOW"

                )



            elif close_price < open_price and volume:


                bearish += 10


                blocks.append(

                    "BEARISH_ORDER_FLOW"

                )



        total = bullish + bearish


        confidence = 0



        if total:


            confidence = (

                max(

                    bullish,

                    bearish

                )

                /

                total

            ) * 100



        signal = "WAIT"



        if bullish > bearish and confidence >= 70:


            signal = "BUY"



        elif bearish > bullish and confidence >= 70:


            signal = "SELL"



        return {


            "signal":

                signal,


            "confidence":

                round(

                    confidence,

                    2

                ),


            "blocks":

                blocks

                }



# =====================================================
# MULTI TIMEFRAME INTELLIGENCE ENGINE V2
# =====================================================

    def analyze_multi_timeframe_v2(

        self,

        symbol,

        market="crypto"

    ):


        timeframes = [

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



        results = {}

        bullish = 0

        bearish = 0

        total_confidence = 0



        # =================================================
        # ANALYZE EACH TIMEFRAME
        # =================================================


        for timeframe in timeframes:


            try:


                trend = self.trend.analyze(

                    symbol=symbol,

                    interval=timeframe,

                    market=market

                )



                confidence = trend.get(

                    "confidence",

                    0

                )



                signal = trend.get(

                    "signal",

                    "WAIT"

                )



                results[timeframe] = {


                    "signal":

                        signal,


                    "confidence":

                        confidence

                }



                total_confidence += confidence



                if signal == "BUY":


                    bullish += confidence



                elif signal == "SELL":


                    bearish += confidence



            except Exception:


                results[timeframe] = {


                    "signal":

                        "WAIT",


                    "confidence":

                        0

                }





        # =================================================
        # CALCULATE ALIGNMENT
        # =================================================


        average_confidence = 0



        if len(timeframes):


            average_confidence = (

                total_confidence

                /

                len(timeframes)

            )



        alignment = 0



        if bullish > bearish:


            alignment = (

                bullish

                /

                (

                    bullish

                    +

                    bearish

                    +

                    1

                )

            ) * 100



            final_signal = "BUY"



        elif bearish > bullish:


            alignment = (

                bearish

                /

                (

                    bullish

                    +

                    bearish

                    +

                    1

                )

            ) * 100



            final_signal = "SELL"



        else:


            final_signal = "WAIT"



        # =================================================
        # HIGHER TIMEFRAME PROTECTION
        # =================================================


        higher_timeframes = [

            "4h",

            "1d"

        ]


        higher_conflict = False



        for tf in higher_timeframes:


            tf_signal = results[tf].get(

                "signal",

                "WAIT"

            )



            if (

                final_signal == "BUY"

                and

                tf_signal == "SELL"

            ):


                higher_conflict = True



            if (

                final_signal == "SELL"

                and

                tf_signal == "BUY"

            ):


                higher_conflict = True





        if higher_conflict:


            final_signal = "WAIT"





        return {


            "signal":

                final_signal,


            "confidence":

                round(

                    average_confidence,

                    2

                ),


            "alignment":

                round(

                    alignment,

                    2

                ),


            "higher_timeframe_conflict":

                higher_conflict,


            "timeframes":

                results

        }





# =====================================================
# MTF VALIDATION GATE
# =====================================================

    def validate_multi_timeframe(

        self,

        mtf_data

    ):


        if not self.enable_mtf_filter:


            return True



        if mtf_data.get(

            "higher_timeframe_conflict",

            False

        ):


            return False



        if mtf_data.get(

            "confidence",

            0

        ) < self.minimum_mtf_confidence:


            return False



        return True



# =====================================================
# RISK MANAGER ENGINE V2
# =====================================================

    def calculate_dynamic_risk(

        self,

        direction,

        price,

        confidence,

        atr,

        volatility,

        trend_strength,

        market_state,

        smart_money=None,

        fibonacci=None,

        market="crypto"

    ):


        if not price or price <= 0:


            return {


                "risk":

                    "INVALID_PRICE",


                "stop_loss":

                    0,


                "take_profit":

                    []

            }



        # =================================================
        # MARKET SETTINGS
        # =================================================


        atr_multiplier = 2.0


        if market == "forex":


            atr_multiplier = 1.5



        elif market == "stocks":


            atr_multiplier = 1.8



        elif market == "crypto":


            atr_multiplier = 2.5



        # =================================================
        # VOLATILITY ADJUSTMENT
        # =================================================


        if volatility >= 8:


            atr_multiplier += 1



        elif volatility <= 2:


            atr_multiplier -= 0.5



        atr_distance = (

            atr

            *

            atr_multiplier

        )



        # =================================================
        # STOP LOSS
        # =================================================


        if direction == "BUY":


            stop_loss = (

                price

                -

                atr_distance

            )



        elif direction == "SELL":


            stop_loss = (

                price

                +

                atr_distance

            )



        else:


            stop_loss = price





        # =================================================
        # RISK REWARD MODEL
        # =================================================


        reward_ratio = 2.0



        if confidence >= 90:


            reward_ratio = 3.0



        elif confidence < 75:


            reward_ratio = 1.5





        take_profit = []



        if direction == "BUY":


            tp1 = price + (

                atr_distance

                *

                reward_ratio

            )


            tp2 = price + (

                atr_distance

                *

                reward_ratio

                *

                1.5

            )


            tp3 = price + (

                atr_distance

                *

                reward_ratio

                *

                2

            )



        elif direction == "SELL":


            tp1 = price - (

                atr_distance

                *

                reward_ratio

            )


            tp2 = price - (

                atr_distance

                *

                reward_ratio

                *

                1.5

            )


            tp3 = price - (

                atr_distance

                *

                reward_ratio

                *

                2

            )


        else:


            tp1 = price

            tp2 = price

            tp3 = price





        take_profit = [


            round(tp1, 8),


            round(tp2, 8),


            round(tp3, 8)

        ]



        # =================================================
        # RISK LEVEL
        # =================================================


        risk_level = "MEDIUM"



        if confidence >= 90 and trend_strength >= 85:


            risk_level = "LOW"



        if volatility >= 10:


            risk_level = "HIGH"





        return {


            "direction":

                direction,


            "entry":

                price,


            "stop_loss":

                round(

                    stop_loss,

                    8

                ),


            "take_profit":

                take_profit,


            "reward_ratio":

                reward_ratio,


            "risk_level":

                risk_level,


            "confidence":

                confidence,


            "market_state":

                market_state

        }





# =====================================================
# POSITION SIZE CALCULATOR
# =====================================================

    def calculate_position_size(

        self,

        capital,

        risk_percent,

        entry,

        stop_loss

    ):


        if (

            not capital

            or

            not entry

            or

            not stop_loss

        ):


            return 0



        risk_amount = (

            capital

            *

            risk_percent

            /

            100

        )



        distance = abs(

            entry

            -

            stop_loss

        )



        if distance == 0:


            return 0



        position = (

            risk_amount

            /

            distance

        )



        return round(

            position,

            6

        )



# =====================================================
# AI SIGNAL EXPLANATION ENGINE V2
# =====================================================

    def generate_signal_explanation(

        self,

        report

    ):


        signal = report.get(

            "signal",

            "WAIT"

        )


        confidence = report.get(

            "confidence",

            0

        )


        modules = report.get(

            "modules",

            {}

        )


        explanation = []

        strengths = []

        weaknesses = []

        recommendations = []



        # =================================================
        # SIGNAL DESCRIPTION
        # =================================================


        if signal == "BUY":


            explanation.append(

                "Artificial Intelligence recommends BUY."

            )


        elif signal == "SELL":


            explanation.append(

                "Artificial Intelligence recommends SELL."

            )


        else:


            explanation.append(

                "Artificial Intelligence recommends WAIT."

            )



        # =================================================
        # TREND
        # =================================================


        trend = modules.get(

            "trend",

            {}

        )


        if trend.get(

            "confidence",

            0

        ) >= 85:


            strengths.append(

                "Trend confirmed."

            )


        else:


            weaknesses.append(

                "Trend confirmation is weak."

            )



        # =================================================
        # MULTI TIMEFRAME
        # =================================================


        mtf = modules.get(

            "multi_timeframe",

            {}

        )


        if mtf.get(

            "confidence",

            0

        ) >= 80:


            strengths.append(

                "Multi timeframe agreement."

            )


        else:


            weaknesses.append(

                "Timeframes disagree."

            )



        # =================================================
        # SMART MONEY
        # =================================================


        smart = modules.get(

            "smart_money",

            {}

        )


        if smart.get(

            "confidence",

            0

        ) >= 80:


            strengths.append(

                "Institutional activity detected."

            )



        # =================================================
        # LIQUIDITY
        # =================================================


        liquidity = modules.get(

            "liquidity",

            {}

        )


        if liquidity.get(

            "confidence",

            0

        ) >= 80:


            strengths.append(

                "Liquidity supports movement."

            )



        # =================================================
        # ORDER BLOCKS
        # =================================================


        blocks = modules.get(

            "order_blocks",

            {}

        )


        if blocks.get(

            "confidence",

            0

        ) >= 80:


            strengths.append(

                "Order Blocks confirmed."

            )



        # =================================================
        # NEWS
        # =================================================


        news = modules.get(

            "news",

            {}

        )


        if news.get(

            "risk"

        ) == "HIGH":


            weaknesses.append(

                "High impact news."

            )



        # =================================================
        # ECONOMIC
        # =================================================


        economic = report.get(

            "economic",

            {}

        )


        if economic.get(

            "risk"

        ) in [

            "HIGH",

            "EXTREME"

        ]:


            weaknesses.append(

                "Economic event risk."

            )



        # =================================================
        # RECOMMENDATIONS
        # =================================================


        if signal == "BUY":


            recommendations.append(

                "Wait for confirmation before entry."

            )


            recommendations.append(

                "Respect Stop Loss."

            )



        elif signal == "SELL":


            recommendations.append(

                "Avoid emotional trading."

            )


            recommendations.append(

                "Respect Stop Loss."

            )



        else:


            recommendations.append(

                "Wait for stronger confirmation."

            )



        return {

            "summary":

                explanation,


            "strengths":

                strengths,


            "weaknesses":

                weaknesses,


            "recommendations":

                recommendations,


            "confidence":

                confidence

        }



# =====================================================
# HUMAN FRIENDLY MESSAGE
# =====================================================

    def explain_for_user(

        self,

        report

    ):


        data = self.generate_signal_explanation(

            report

        )


        text = []


        text.extend(

            data["summary"]

        )


        if data["strengths"]:


            text.append(

                "Strengths:"

            )


            text.extend(

                data["strengths"]

            )


        if data["weaknesses"]:


            text.append(

                "Warnings:"

            )


            text.extend(

                data["weaknesses"]

            )


        if data["recommendations"]:


            text.append(

                "Recommendations:"

            )


            text.extend(

                data["recommendations"]

            )


        return "\n".join(text)



# =====================================================
# AI SELF PROTECTION ENGINE V1
# =====================================================

    def self_protection_check(

        self,

        market_data,

        trend,

        prediction,

        smart_money,

        multi_timeframe

    ):

        issues = []

        safe = True

        score = 100

        # =============================================
        # MARKET DATA
        # =============================================

        if not market_data:

            issues.append("No market data")

            safe = False

            score -= 40

        # =============================================
        # TREND ENGINE
        # =============================================

        if trend.get("confidence", 0) < 50:

            issues.append("Weak trend engine")

            score -= 15

        # =============================================
        # PREDICTION ENGINE
        # =============================================

        if prediction.get("confidence", 0) < 50:

            issues.append("Prediction confidence too low")

            score -= 15

        # =============================================
        # SMART MONEY
        # =============================================

        if smart_money.get("confidence", 0) < 50:

            issues.append("Smart Money unavailable")

            score -= 10

        # =============================================
        # MULTI TIMEFRAME
        # =============================================

        if multi_timeframe.get("confidence", 0) < 50:

            issues.append("MTF disagreement")

            score -= 10

        # =============================================
        # FINAL
        # =============================================

        if score < 60:

            safe = False

        return {

            "safe": safe,

            "health_score": max(score, 0),

            "issues": issues

        }


# =====================================================
# PROVIDER FAILOVER
# =====================================================

    def provider_failover(

        self,

        provider_name

    ):

        providers = [

            "binance",

            "bybit",

            "okx",

            "coinbase",

            "kraken"

        ]

        if provider_name in providers:

            providers.remove(provider_name)

        return providers


# =====================================================
# SIGNAL SAFETY GATE
# =====================================================

    def signal_safety_gate(

        self,

        protection_report

    ):

        if not protection_report.get("safe", False):

            return False

        if protection_report.get("health_score", 0) < 70:

            return False

        return True



# =====================================================
# AI LEARNING ENGINE V2
# =====================================================

    def learn_from_signal_result(

        self,

        symbol,

        signal,

        confidence,

        result

    ):


        if not hasattr(

            self,

            "learning_memory"

        ):

            self.learning_memory = []



        record = {

            "symbol":

                symbol,

            "signal":

                signal,

            "confidence":

                confidence,

            "result":

                result,

            "time":

                datetime.utcnow().isoformat()

        }



        self.learning_memory.append(

            record

        )



        # الاحتفاظ بآخر 5000 تجربة

        if len(self.learning_memory) > 5000:


            self.learning_memory = (

                self.learning_memory[-5000:]

            )



        return True





# =====================================================
# AI PERFORMANCE ANALYSIS
# =====================================================

    def analyze_learning_performance(

        self

    ):


        if not hasattr(

            self,

            "learning_memory"

        ):


            return {


                "samples":

                    0,


                "accuracy":

                    0

            }



        total = len(

            self.learning_memory

        )


        success = 0



        for item in self.learning_memory:


            if item.get(

                "result"

            ) == "SUCCESS":


                success += 1



        accuracy = 0



        if total > 0:


            accuracy = (

                success

                /

                total

            ) * 100



        return {


            "samples":

                total,


            "successful":

                success,


            "accuracy":

                round(

                    accuracy,

                    2

                )

        }





# =====================================================
# CONFIDENCE ADAPTATION
# =====================================================

    def adaptive_confidence_adjustment(

        self,

        confidence

    ):


        performance = self.analyze_learning_performance()



        accuracy = performance.get(

            "accuracy",

            0

        )



        adjustment = 0



        if accuracy >= 80:


            adjustment = 5



        elif accuracy < 50:


            adjustment = -10



        new_confidence = (

            confidence

            +

            adjustment

        )



        return max(

            0,

            min(

                new_confidence,

                100

            )

    )



# =====================================================
# REAL MARKET DATA QUALITY ENGINE V2
# =====================================================

    def advanced_data_quality_check(

        self,

        candles,

        providers_data=None

    ):


        score = 100

        problems = []



        # =================================================
        # CANDLE CHECK
        # =================================================

        if not candles:


            return {


                "quality":

                    "INVALID",


                "score":

                    0,


                "problems":

                    [

                        "No candles"

                    ]

            }



        candle_count = len(

            candles

        )



        if candle_count < 50:


            score -= 30


            problems.append(

                "Not enough candles"

            )



        # =================================================
        # MISSING CANDLE DETECTION
        # =================================================


        missing = 0



        for i in range(

            1,

            len(candles)

        ):


            previous = candles[i-1].get(

                "time",

                0

            )


            current = candles[i].get(

                "time",

                0

            )



            if current <= previous:


                missing += 1



        if missing > 0:


            score -= 20


            problems.append(

                "Missing or invalid candles"

            )



        # =================================================
        # PRICE QUALITY
        # =================================================


        for candle in candles[-20:]:


            close = candle.get(

                "close",

                0

            )


            high = candle.get(

                "high",

                0

            )


            low = candle.get(

                "low",

                0

            )



            if (

                close <= 0

                or

                high <= 0

                or

                low <= 0

            ):


                score -= 20


                problems.append(

                    "Invalid price data"

                )


                break



        # =================================================
        # VOLUME QUALITY
        # =================================================


        volume_available = True



        for candle in candles[-20:]:


            if candle.get(

                "volume",

                0

            ) <= 0:


                volume_available = False


                break



        if not volume_available:


            score -= 15


            problems.append(

                "Weak volume data"

            )



        # =================================================
        # PROVIDER CONSISTENCY
        # =================================================


        if providers_data:


            prices = []



            for provider in providers_data:


                price = provider.get(

                    "price",

                    0

                )


                if price:


                    prices.append(

                        price

                    )



            if len(prices) >= 2:


                max_price = max(

                    prices

                )


                min_price = min(

                    prices

                )


                difference = (

                    (

                        max_price

                        -

                        min_price

                    )

                    /

                    min_price

                ) * 100



                if difference > 1:


                    score -= 20


                    problems.append(

                        "Provider price mismatch"

                    )



        # =================================================
        # FINAL QUALITY
        # =================================================


        score = max(

            0,

            score

        )


        quality = "LOW"



        if score >= 90:

            quality = "EXCELLENT"


        elif score >= 75:

            quality = "GOOD"


        elif score >= 50:

            quality = "ACCEPTABLE"



        return {


            "quality":

                quality,


            "score":

                score,


            "problems":

                problems,


            "candles":

                candle_count

        }



# =====================================================
# DATA PROVIDER AUTO SWITCH ENGINE V1
# =====================================================

    def get_best_market_provider(

        self,

        symbol,

        market="crypto"

    ):


        providers_status = []


        providers = self.get_market_providers(

            market

        )


        selected_provider = None



        # =================================================
        # PROVIDER HEALTH CHECK
        # =================================================


        for provider in providers:


            try:


                health = provider.health_check()



                status = {


                    "provider":

                        provider.name,


                    "status":

                        health.get(

                            "status",

                            "UNKNOWN"

                        )

                }


                providers_status.append(

                    status

                )



                if (

                    health.get(

                        "status"

                    )

                    ==

                    "ACTIVE"

                    and

                    selected_provider is None

                ):


                    selected_provider = provider



            except Exception as error:



                providers_status.append(


                    {


                        "provider":

                            getattr(

                                provider,

                                "name",

                                "UNKNOWN"

                            ),


                        "status":

                            "FAILED",


                        "error":

                            str(error)

                    }

                )



        return {


            "selected":

                selected_provider,


            "providers":

                providers_status

        }





# =====================================================
# PROVIDER DATA FALLBACK
# =====================================================

    def fetch_with_fallback(

        self,

        symbol,

        interval,

        market="crypto"

    ):


        providers = self.get_market_providers(

            market

        )


        errors = []



        for provider in providers:


            try:


                data = provider.get_candles(

                    symbol,

                    interval

                )



                if (

                    data

                    and

                    len(data) > 0

                ):


                    return {


                        "provider":

                            provider.name,


                        "candles":

                            data,


                        "status":

                            "SUCCESS"

                    }



            except Exception as error:


                errors.append(


                    {


                        "provider":

                            getattr(

                                provider,

                                "name",

                                "UNKNOWN"

                            ),


                        "error":

                            str(error)

                    }

                )



        return {


            "provider":

                None,


            "candles":

                [],


            "status":

                "FAILED",


            "errors":

                errors

        }





# =====================================================
# PROVIDER RELIABILITY SCORE
# =====================================================

    def calculate_provider_score(

        self,

        provider_data

    ):


        score = 100



        if provider_data.get(

            "status"

        ) != "SUCCESS":


            score -= 50



        candles = provider_data.get(

            "candles",

            []

        )



        if len(candles) < 100:


            score -= 30



        return max(

            0,

            score

            )



# =====================================================
# SURPRISE TREND DETECTION ENGINE V1
# =====================================================

    def detect_surprise_trend(

        self,

        candles,

        volume,

        liquidity,

        smart_money,

        order_blocks,

        multi_timeframe

    ):


        if not candles or len(candles) < 50:


            return {


                "alert":

                    False,


                "direction":

                    "NONE",


                "confidence":

                    0

            }



        bullish_score = 0

        bearish_score = 0

        reasons = []



        # =================================================
        # VOLUME EXPANSION
        # =================================================


        volume_ratio = volume.get(

            "volume_ratio",

            1

        )


        volume_signal = volume.get(

            "signal",

            "WAIT"

        )



        if volume_ratio >= 1.5:


            if volume_signal == "BUY":


                bullish_score += 20


                reasons.append(

                    "Volume expansion bullish"

                )


            elif volume_signal == "SELL":


                bearish_score += 20


                reasons.append(

                    "Volume expansion bearish"

                )



        # =================================================
        # SMART MONEY PRESSURE
        # =================================================


        smart_signal = smart_money.get(

            "signal",

            "WAIT"

        )


        smart_conf = smart_money.get(

            "confidence",

            0

        )



        if smart_conf >= 80:


            if smart_signal == "BUY":


                bullish_score += 25


                reasons.append(

                    "Smart money accumulation"

                )


            elif smart_signal == "SELL":


                bearish_score += 25


                reasons.append(

                    "Smart money distribution"

                )



        # =================================================
        # LIQUIDITY BUILDUP
        # =================================================


        liquidity_conf = liquidity.get(

            "confidence",

            0

        )


        liquidity_signal = liquidity.get(

            "signal",

            "WAIT"

        )



        if liquidity_conf >= 80:


            if liquidity_signal == "BUY":


                bullish_score += 15


                reasons.append(

                    "Liquidity accumulation"

                )


            elif liquidity_signal == "SELL":


                bearish_score += 15


                reasons.append(

                    "Liquidity pressure down"

                )



        # =================================================
        # ORDER BLOCK CONFIRMATION
        # =================================================


        block_conf = order_blocks.get(

            "confidence",

            0

        )


        block_signal = order_blocks.get(

            "signal",

            "WAIT"

        )



        if block_conf >= 75:


            if block_signal == "BUY":


                bullish_score += 15



                reasons.append(

                    "Bullish order block"

                )



            elif block_signal == "SELL":


                bearish_score += 15



                reasons.append(

                    "Bearish order block"

                )



        # =================================================
        # HIGHER TIMEFRAME SUPPORT
        # =================================================


        mtf_signal = multi_timeframe.get(

            "signal",

            "WAIT"

        )


        mtf_conf = multi_timeframe.get(

            "confidence",

            0

        )



        if mtf_conf >= 85:


            if mtf_signal == "BUY":


                bullish_score += 15



            elif mtf_signal == "SELL":


                bearish_score += 15



        # =================================================
        # FINAL CALCULATION
        # =================================================


        total = (

            bullish_score

            +

            bearish_score

        )


        confidence = 0



        if total > 0:


            confidence = (

                max(

                    bullish_score,

                    bearish_score

                )

                /

                total

            ) * 100



        direction = "NONE"



        if bullish_score > bearish_score:


            direction = "BULLISH"



        elif bearish_score > bullish_score:


            direction = "BEARISH"





        return {


            "alert":

                confidence >= 80,


            "direction":

                direction,


            "bullish_score":

                bullish_score,


            "bearish_score":

                bearish_score,


            "confidence":

                round(

                    confidence,

                    2

                ),


            "reasons":

                reasons

        }





# =====================================================
# SURPRISE ALERT FILTER
# =====================================================

    def surprise_alert_gate(

        self,

        surprise_data

    ):


        if not surprise_data.get(

            "alert",

            False

        ):


            return False



        if surprise_data.get(

            "confidence",

            0

        ) < self.minimum_alert_confidence:


            return False



        return True



# =====================================================
# NEWS IMPACT AI ENGINE V2
# =====================================================

    def analyze_news_impact(

        self,

        news_data

    ):


        if not news_data:


            return {


                "risk":

                    "UNKNOWN",


                "confidence":

                    0,


                "impact":

                    "NONE"

            }



        risk = news_data.get(

            "risk",

            "LOW"

        )


        confidence = news_data.get(

            "confidence",

            0

        )


        impact = news_data.get(

            "impact",

            "NONE"

        )



        score = 100



        if risk == "HIGH":


            score -= 40



        elif risk == "MEDIUM":


            score -= 20



        elif risk == "LOW":


            score -= 5





        return {


            "risk":

                risk,


            "impact":

                impact,


            "confidence":

                max(

                    0,

                    score

                ),


            "raw":

                news_data

        }





# =====================================================
# ECONOMIC EVENT PROTECTION V2
# =====================================================

    def analyze_economic_risk(

        self,

        economic_event

    ):


        result = {


            "available":

                False,


            "risk":

                "LOW",


            "confidence":

                100,


            "block_signal":

                False

        }



        if not economic_event:


            return result





        result["available"] = True



        importance = economic_event.get(

            "importance",

            "LOW"

        )


        minutes = economic_event.get(

            "minutes_remaining",

            999

        )



        # =================================================
        # HIGH IMPACT EVENTS
        # =================================================


        if importance == "HIGH":


            result["risk"] = "HIGH"


            result["confidence"] = 50



            if minutes <= 30:


                result["block_signal"] = True



        # =================================================
        # EXTREME EVENTS
        # =================================================


        if (

            importance == "EXTREME"

        ):


            result["risk"] = "EXTREME"


            result["confidence"] = 20


            result["block_signal"] = True



        return result





# =====================================================
# NEWS & ECONOMIC FILTER
# =====================================================

    def news_economic_gate(

        self,

        news,

        economic

    ):



        if self.enable_news_filter:


            if news.get(

                "risk"

            ) == "HIGH":


                return False



        if self.enable_economic_filter:


            if economic.get(

                "block_signal",

                False

            ):


                return False



        return True



# =====================================================
# AI MARKET MEMORY ENGINE V2
# =====================================================

    def store_market_pattern(

        self,

        symbol,

        interval,

        market_state,

        signal,

        confidence,

        result=None

    ):


        if not hasattr(

            self,

            "market_memory"

        ):


            self.market_memory = []



        pattern = {


            "symbol":

                symbol,


            "interval":

                interval,


            "market_state":

                market_state,


            "signal":

                signal,


            "confidence":

                confidence,


            "result":

                result,


            "time":

                datetime.utcnow().isoformat()

        }



        self.market_memory.append(

            pattern

        )



        # حفظ آخر 10000 حالة

        if len(

            self.market_memory

        ) > 10000:


            self.market_memory = (

                self.market_memory[-10000:]

            )



        return True





# =====================================================
# HISTORICAL PATTERN MATCHING
# =====================================================

    def find_similar_patterns(

        self,

        symbol,

        market_state,

        interval

    ):


        if not hasattr(

            self,

            "market_memory"

        ):


            return []



        matches = []



        for item in self.market_memory:


            if (

                item.get("symbol")

                ==

                symbol

                and

                item.get("interval")

                ==

                interval

                and

                item.get("market_state")

                ==

                market_state

            ):


                matches.append(

                    item

                )



        return matches[-50:]





# =====================================================
# HISTORICAL SUCCESS RATE
# =====================================================

    def calculate_historical_accuracy(

        self,

        symbol,

        market_state,

        interval

    ):


        patterns = self.find_similar_patterns(

            symbol,

            market_state,

            interval

        )



        if not patterns:


            return {


                "samples":

                    0,


                "accuracy":

                    0

            }



        success = 0



        for item in patterns:


            if item.get(

                "result"

            ) == "SUCCESS":


                success += 1



        accuracy = (

            success

            /

            len(patterns)

        ) * 100



        return {


            "samples":

                len(patterns),


            "success":

                success,


            "accuracy":

                round(

                    accuracy,

                    2

                )

        }





# =====================================================
# HISTORICAL LEARNING BOOST
# =====================================================

    def historical_confidence_boost(

        self,

        confidence,

        historical_data

    ):


        accuracy = historical_data.get(

            "accuracy",

            0

        )


        boost = 0



        if accuracy >= 80:


            boost = 10



        elif accuracy >= 65:


            boost = 5



        elif accuracy < 40:


            boost = -10





        final_confidence = (

            confidence

            +

            boost

        )



        return max(

            0,

            min(

                final_confidence,

                100

            )

        )



# =====================================================
# CANDLE AI ADVANCED PATTERN ENGINE V2
# =====================================================

    def analyze_candle_patterns(

        self,

        candles

    ):


        if not candles or len(candles) < 3:


            return {


                "signal":

                    "WAIT",


                "confidence":

                    0,


                "patterns":

                    []

            }



        patterns = []

        bullish_score = 0

        bearish_score = 0



        current = candles[-1]

        previous = candles[-2]



        current_open = current.get(

            "open",

            0

        )


        current_close = current.get(

            "close",

            0

        )


        current_high = current.get(

            "high",

            0

        )


        current_low = current.get(

            "low",

            0

        )



        previous_open = previous.get(

            "open",

            0

        )


        previous_close = previous.get(

            "close",

            0

        )



        body = abs(

            current_close

            -

            current_open

        )



        candle_range = (

            current_high

            -

            current_low

        )



        if candle_range == 0:


            return {


                "signal":

                    "WAIT",


                "confidence":

                    0,


                "patterns":

                    []

            }



        # =================================================
        # BULLISH ENGULFING
        # =================================================


        if (

            current_close > current_open

            and

            previous_close < previous_open

            and

            current_close > previous_open

            and

            current_open < previous_close

        ):


            bullish_score += 30


            patterns.append(

                "BULLISH_ENGULFING"

            )



        # =================================================
        # BEARISH ENGULFING
        # =================================================


        if (

            current_close < current_open

            and

            previous_close > previous_open

            and

            current_open > previous_close

            and

            current_close < previous_open

        ):


            bearish_score += 30


            patterns.append(

                "BEARISH_ENGULFING"

            )



        # =================================================
        # PIN BAR DETECTION
        # =================================================


        upper_wick = (

            current_high

            -

            max(

                current_open,

                current_close

            )

        )


        lower_wick = (

            min(

                current_open,

                current_close

            )

            -

            current_low

        )



        if lower_wick > body * 2:


            bullish_score += 20


            patterns.append(

                "BULLISH_PIN_BAR"

            )



        if upper_wick > body * 2:


            bearish_score += 20


            patterns.append(

                "BEARISH_PIN_BAR"

            )



        # =================================================
        # DOJI
        # =================================================


        if body <= candle_range * 0.1:


            patterns.append(

                "DOJI"

            )



        # =================================================
        # STRONG CANDLE
        # =================================================


        strength = (

            body

            /

            candle_range

        ) * 100



        if strength >= 80:


            patterns.append(

                "STRONG_MOMENTUM_CANDLE"

            )



            if current_close > current_open:


                bullish_score += 15


            else:


                bearish_score += 15





        # =================================================
        # FINAL RESULT
        # =================================================


        signal = "WAIT"

        confidence = 0



        if bullish_score > bearish_score:


            signal = "BUY"


            confidence = bullish_score



        elif bearish_score > bullish_score:


            signal = "SELL"


            confidence = bearish_score





        return {


            "signal":

                signal,


            "confidence":

                min(

                    confidence,

                    100

                ),


            "bullish_score":

                bullish_score,


            "bearish_score":

                bearish_score,


            "patterns":

                patterns

        }





# =====================================================
# FAKE BREAKOUT CANDLE FILTER
# =====================================================

    def detect_fake_breakout(

        self,

        candles

    ):


        if not candles or len(candles) < 5:


            return False



        last = candles[-1]


        previous_high = max(

            c.get(

                "high",

                0

            )

            for c in candles[-5:-1]

        )


        previous_low = min(

            c.get(

                "low",

                0

            )

            for c in candles[-5:-1]

        )



        close = last.get(

            "close",

            0

        )


        high = last.get(

            "high",

            0

        )


        low = last.get(

            "low",

            0

        )



        if (

            high > previous_high

            and

            close < previous_high

        ):


            return True



        if (

            low < previous_low

            and

            close > previous_low

        ):


            return True



        return False



        # =============================================
        # CANDLE COUNT
        # =============================================

        candle_count = len(candles)


        if candle_count < 50:

            score -= 40

            result["issues"].append(
                "NOT_ENOUGH_CANDLES"
            )


        elif candle_count < 200:

            score -= 10



        # =============================================
        # MISSING CANDLES CHECK
        # =============================================

        missing = self.check_missing_candles(

            candles

        )


        if missing:

            score -= 20

            result["issues"].append(
                "MISSING_CANDLES"
            )



        # =============================================
        # PRICE QUALITY
        # =============================================

        price_quality = self.check_price_quality(

            candles

        )


        if not price_quality:

            score -= 20

            result["issues"].append(
                "BAD_PRICE_DATA"
            )



        # =============================================
        # VOLUME QUALITY
        # =============================================

        volume_quality = self.check_volume_quality(

            candles

        )


        if not volume_quality:

            score -= 15

            result["issues"].append(
                "BAD_VOLUME_DATA"
            )



        # =============================================
        # PROVIDERS CONSISTENCY
        # =============================================

        if providers_data:


            if not self.check_provider_consistency(

                providers_data

            ):

                score -= 20

                result["issues"].append(
                    "PROVIDER_MISMATCH"
                )



        score = max(

            0,

            score

        )



        if score >= 90:

            quality = "EXCELLENT"

        elif score >= 75:

            quality = "GOOD"

        elif score >= 50:

            quality = "WEAK"

        else:

            quality = "LOW"



        result["quality"] = quality

        result["score"] = score


        return result





# =====================================================
# MISSING CANDLE DETECTOR
# =====================================================

    def check_missing_candles(

        self,

        candles

    ):


        if len(candles) < 2:

            return True



        for i in range(

            1,

            len(candles)

        ):

            if (

                candles[i].get("time",0)

                <=

                candles[i-1].get("time",0)

            ):

                return True



        return False





# =====================================================
# PRICE DATA VALIDATION
# =====================================================

    def check_price_quality(

        self,

        candles

    ):


        for candle in candles:


            if (

                candle.get("open",0) <= 0

                or

                candle.get("high",0) <= 0

                or

                candle.get("low",0) <= 0

                or

                candle.get("close",0) <= 0

            ):

                return False



        return True





# =====================================================
# VOLUME DATA VALIDATION
# =====================================================

    def check_volume_quality(

        self,

        candles

    ):


        valid = 0


        for candle in candles:


            if candle.get(

                "volume",

                0

            ) > 0:

                valid += 1



        return (

            valid

            /

            len(candles)

        ) >= 0.8





# =====================================================
# PROVIDER CONSISTENCY CHECK
# =====================================================

    def check_provider_consistency(

        self,

        providers

    ):


        prices = []



        for item in providers:


            price = item.get(

                "price"

            )


            if price:

                prices.append(

                    price

                )



        if len(prices) < 2:

            return True



        average = sum(prices) / len(prices)



        for price in prices:


            difference = abs(

                price - average

            ) / average * 100



            if difference > 1:

                return False



        return True



# =====================================================
# PRODUCTION ERROR PROTECTION SYSTEM V2
# =====================================================

    def safe_execute(

        self,

        function,

        *args,

        default=None,

        **kwargs

    ):


        try:

            return function(

                *args,

                **kwargs

            )


        except Exception as e:


            if not hasattr(

                self,

                "errors"

            ):


                self.errors = []



            self.errors.append(

                {

                    "function":

                        function.__name__,


                    "error":

                        str(e),


                    "time":

                        datetime.utcnow().isoformat()

                }

            )


            return default





# =====================================================
# ENGINE ERROR REPORT
# =====================================================

    def get_errors(

        self,

        limit=50

    ):


        if not hasattr(

            self,

            "errors"

        ):


            return []



        return self.errors[-limit:]





# =====================================================
# CLEAR ENGINE ERRORS
# =====================================================

    def clear_errors(

        self

    ):


        self.errors = []


        return {


            "status":

                "cleared"

        }





# =====================================================
# PRODUCTION READY CHECK
# =====================================================

    def production_ready(

        self

    ):


        checks = {


            "market":

                self.market is not None,


            "trend":

                self.trend is not None,


            "prediction":

                self.prediction is not None,


            "risk":

                self.risk is not None,


            "smart_money":

                self.smart_money is not None,


            "multi_timeframe":

                self.multi_timeframe is not None,


            "history":

                self.history is not None,


            "news":

                self.news is not None

        }



        ready = all(

            checks.values()

        )



        return {


            "ready":

                ready,


            "checks":

                checks,


            "version":

                self.version

        }





# =====================================================
# FINAL ENGINE SUMMARY
# =====================================================

    def summary(

        self

    ):


        return {


            "engine":

                self.version,


            "status":

                "PRODUCTION",


            "modules":

            len(

                self.weights

            ),


            "filters_enabled":

            sum(

                [

                    self.enable_quality_gate,

                    self.enable_confidence_gate,

                    self.enable_signal_validation,

                    self.enable_news_filter,

                    self.enable_economic_filter,

                    self.enable_volume_filter,

                    self.enable_liquidity_filter

                ]

            ),


            "statistics":

                self.signal_statistics,


            "time":

                datetime.utcnow().isoformat()

            }



# =====================================================
# FINAL PRODUCTION CLEANUP CONTROLLER
# =====================================================


    def cleanup_check(self):


        duplicates = []


        required_modules = [

            "market",

            "trend",

            "patterns",

            "smart_money",

            "prediction",

            "risk",

            "news",

            "fibonacci",

            "opportunity",

            "multi_timeframe",

            "volume",

            "liquidity",

            "order_blocks",

            "candles_ai",

            "history"

        ]


        for module in required_modules:


            if not hasattr(

                self,

                module

            ):


                duplicates.append(

                    f"Missing module: {module}"

                )



        return {


            "status":

                "CLEAN"

                if not duplicates

                else

                "CHECK_REQUIRED",


            "issues":

                duplicates,


            "engine":

                self.version

        }





# =====================================================
# FINAL VALIDATION BEFORE SIGNAL
# =====================================================


    def final_validation(

        self,

        report

    ):


        checks = {



            "confidence":

                report.get(

                    "confidence",

                    0

                ) >= self.minimum_confidence,



            "quality":

                report.get(

                    "quality",

                    {}

                ).get(

                    "quality",

                    "LOW"

                )

                not in [

                    "LOW",

                    "WEAK"

                ],



            "trend":

                report.get(

                    "trend_status"

                )

                !=

                "REJECTED",



            "risk":

                report.get(

                    "risk",

                    {}

                ).get(

                    "level",

                    "LOW"

                )

                not in [

                    "HIGH",

                    "EXTREME"

                ]

        }



        return {


            "approved":

                all(

                    checks.values()

                ),


            "checks":

                checks

        }





# =====================================================
# ENGINE VERSION CONTROL
# =====================================================


    def version_info(

        self

    ):


        return {


            "name":

                "FalconAI",


            "engine":

                self.version,


            "stage":

                "Production V3",


            "architecture":

            [

                "Market AI",

                "Trend AI",

                "Prediction AI",

                "Smart Money",

                "Risk Engine",

                "News AI",

                "Historical Learning",

                "Multi Timeframe AI"

            ]

    }



# =====================================================
# FINAL ENGINE INTEGRITY CHECK V1
# =====================================================


    def integrity_check(

        self

    ):


        modules = {


            "market":

                hasattr(

                    self,

                    "market"

                ),


            "trend":

                hasattr(

                    self,

                    "trend"

                ),


            "prediction":

                hasattr(

                    self,

                    "prediction"

                ),


            "risk":

                hasattr(

                    self,

                    "risk"

                ),


            "news":

                hasattr(

                    self,

                    "news"

                ),


            "economic":

                hasattr(

                    self,

                    "economic"

                ),


            "history":

                hasattr(

                    self,

                    "history"

                ),


            "multi_timeframe":

                hasattr(

                    self,

                    "multi_timeframe"

                )

        }



        missing = []


        for name, status in modules.items():


            if not status:


                missing.append(

                    name

                )



        return {


            "healthy":

                len(missing) == 0,


            "missing":

                missing,


            "engine":

                self.version

        }





# =====================================================
# ACTIVE FILTER STATUS
# =====================================================


    def filter_status(

        self

    ):


        return {


            "quality_gate":

                self.enable_quality_gate,


            "confidence_gate":

                self.enable_confidence_gate,


            "signal_validation":

                self.enable_signal_validation,


            "news_filter":

                self.enable_news_filter,


            "economic_filter":

                self.enable_economic_filter,


            "volume_filter":

                self.enable_volume_filter,


            "liquidity_filter":

                self.enable_liquidity_filter,


            "smart_money_filter":

                self.enable_smart_money_filter,


            "history_filter":

                self.enable_history_filter,


            "mtf_filter":

                self.enable_mtf_filter

        }





# =====================================================
# FULL SYSTEM STATUS
# =====================================================


    def full_status(

        self

    ):


        return {


            "engine":

                self.version,


            "integrity":

                self.integrity_check(),


            "filters":

                self.filter_status(),


            "production":

                self.production_status(),


            "summary":

                self.summary(),


            "time":

                datetime.utcnow().isoformat()

        }



# =====================================================
# FINAL PRODUCTION CHECKLIST V1
# =====================================================


    def production_checklist(

        self

    ):


        checklist = {


            "engine_loaded":

                True,


            "market_analysis":

                hasattr(

                    self,

                    "market"

                ),


            "trend_engine":

                hasattr(

                    self,

                    "trend"

                ),


            "prediction_engine":

                hasattr(

                    self,

                    "prediction"

                ),


            "risk_management":

                hasattr(

                    self,

                    "risk"

                ),


            "smart_money":

                hasattr(

                    self,

                    "smart_money"

                ),


            "multi_timeframe":

                hasattr(

                    self,

                    "multi_timeframe"

                ),


            "historical_learning":

                hasattr(

                    self,

                    "history"

                ),


            "news_ai":

                hasattr(

                    self,

                    "news"

                ),


            "quality_protection":

                self.enable_quality_gate,


            "signal_validation":

                self.enable_signal_validation,


            "duplicate_protection":

                self.enable_duplicate_protection

        }



        passed = sum(

            checklist.values()

        )


        total = len(

            checklist

        )



        return {


            "production_ready":

                passed == total,


            "passed":

                passed,


            "total":

                total,


            "percentage":

                round(

                    (

                        passed

                        /

                        total

                    )

                    *

                    100,

                    2

                ),


            "details":

                checklist

        }





# =====================================================
# FINAL ENGINE SHUTDOWN INFO
# =====================================================


    def shutdown_info(

        self

    ):


        return {


            "engine":

                self.version,


            "status":

                "READY_FOR_PRODUCTION",


            "message":

                "FalconAI Signal Engine closed successfully",


            "statistics":

                self.signal_statistics,


            "time":

                datetime.utcnow().isoformat()

        }
