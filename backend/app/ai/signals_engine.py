from datetime import datetime
from typing import Dict, Any

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


class SignalEngine:

    def __init__(self):

        self.market = MarketAnalyzer()
        self.trend = TrendEngine()
        self.patterns = PatternAnalyzer()
        self.smart_money = SmartMoneyAnalyzer()
        self.prediction = PredictionEngine()
        self.risk = RiskManager()
        self.news = NewsAnalyzer()
        self.fibonacci = FibonacciAnalyzer()

        self.opportunity = OpportunityEngine()
        self.multi_timeframe = MultiTimeframeEngine()

        self.volume = VolumeEngine()
        self.liquidity = LiquidityEngine()
        self.order_blocks = OrderBlocksEngine()
        self.candles_ai = CandlesAI()
        self.history = HistoricalLearning()
        self.minimum_confidence = 60
        self.minimum_signal_score = 6

        self.maximum_confidence = 100

        self.allow_counter_trend = False

        self.enable_news_filter = True
        self.enable_fibonacci_filter = True
        self.enable_smart_money_filter = True
        self.enable_volume_filter = True
        self.enable_liquidity_filter = True
        self.enable_orderblock_filter = True
        self.enable_candle_filter = True
        self.enable_history_filter = True
        self.enable_mtf_filter = True

        self.weights = {

            "trend": 20,
            "multi_timeframe": 15,
            "opportunity": 15,
            "smart_money": 15,
            "prediction": 10,
            "patterns": 5,
            "market": 5,
            "news": 5,
            "fibonacci": 5,
            "volume": 5,
            "liquidity": 5,
            "order_blocks": 5,
            "candles": 5,
            "history": 5

        }

        self.signal_statistics = {

            "buy": 0,
            "sell": 0,
            "wait": 0,
            "success": 0,
            "failed": 0

        }

    

    # ==================================================
    # MAIN ANALYSIS
    # ==================================================

    def analyze(
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

        candles = market_data.get("candles", [])

        volume_analysis = self.volume.analyze(candles)
        liquidity_analysis = self.liquidity.analyze(candles)
        order_blocks_analysis = self.order_blocks.analyze(candles)
        candle_analysis = self.candles_ai.analyze(candles)
        historical_analysis = self.history.analyze(candles)

        trend = self.trend.analyze(
            symbol=symbol,
            interval=interval,
            market=market
        )

        multi_timeframe = self.multi_timeframe.analyze(
            symbol=symbol,
            market=market
        )

        if len(candles) < 50:

            opportunity = {
                "signal": "WAIT",
                "confidence": 0,
                "score": 0,
                "reasons": ["Not enough candles"]
            }

        else:

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

        news = self.news.analyze(symbol)



        # ==================================================
        # EARLY TREND
        # ==================================================

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

        # ==================================================
        # CONFIDENCE
        # ==================================================

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
            historical_analysis
        )

        # ==================================================
        # FINAL DECISION
        # ==================================================

        direction, reasons, warnings, scores = self.make_decision(
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
            historical_analysis
        )

        if direction == "WAIT":
            confidence = min(confidence, 40)

        # ==================================================
        # RISK
        # ==================================================

        risk = self.risk.calculate(
            direction=direction,
            price=market_data.get("price", 0),
            confidence=confidence,
            atr=market_data.get("atr", 0),
            volatility=market_data.get("volatility", 0),
            trend_strength=market_data.get("trend_strength", 0),
            market_state=market_data.get(
                "market_state",
                "UNKNOWN"
            ),
            smart_money=smart_money,
            fibonacci=fibonacci,
            market=market
        )

        return {

            "symbol": symbol,
            "interval": interval,
            "market": market,

            "direction": direction,
            "confidence": confidence,
            "confidence_details": confidence_details,

            "decision_reasons": reasons,
            "warnings": warnings,
            "signal_strength": scores,

            "early_trend": early_trend,

            "price": market_data.get("price", 0),

            "market_analysis": market_data,
            "trend": trend,
            "multi_timeframe": multi_timeframe,
            "opportunity": opportunity,
            "smart_money": smart_money,
            "prediction": prediction,
            "patterns": patterns,
            "fibonacci": fibonacci,
            "news": news,

            "volume_analysis": volume_analysis,
            "liquidity_analysis": liquidity_analysis,
            "order_blocks": order_blocks_analysis,
            "candle_analysis": candle_analysis,
            "historical_learning": historical_analysis,

            "risk": risk,

            "created_at": datetime.utcnow().isoformat()

        }



    # ==================================================
    # CALCULATE CONFIDENCE
    # ==================================================

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

        volume_analysis,

        liquidity_analysis,

        order_blocks_analysis,

        candle_analysis,

        historical_analysis

    ):

        score = 0

        details = []

        # -----------------------------
        # Trend
        # -----------------------------

        trend_score = abs(
            trend.get("score", 0)
        )

        if trend_score >= 70:

            score += 25

            details.append(
                "اتجاه قوي جداً"
            )

        elif trend_score >= 35:

            score += 15

            details.append(
                "اتجاه واضح"
            )

        # -----------------------------
        # Multi Timeframe
        # -----------------------------

        mtf_conf = multi_timeframe.get(
            "confidence",
            0
        )

        if mtf_conf >= 80:

            score += 20

            details.append(
                "توافق قوي بين الفريمات"
            )

        elif mtf_conf >= 50:

            score += 10

            details.append(
                "توافق متوسط بين الفريمات"
            )

        # -----------------------------
        # Smart Money
        # -----------------------------

        smart_conf = smart_money.get(
            "confidence",
            0
        )

        if smart_conf >= 80:

            score += 20

            details.append(
                "Smart Money قوي"
            )

        elif smart_conf >= 50:

            score += 10

        # -----------------------------
        # Opportunity
        # -----------------------------

        opp_conf = opportunity.get(
            "confidence",
            0
        )

        if opp_conf >= 70:

            score += 15

            details.append(
                "فرصة تداول قوية"
            )

        elif opp_conf >= 40:

            score += 8

        # -----------------------------
        # Market Momentum
        # -----------------------------

        if market.get("volume_power", 0) > 1:

            score += 5

            details.append(
                "حجم التداول داعم"
            )

        if market.get("momentum", 0) > 0:

            score += 5

        # -----------------------------
        # News
        # -----------------------------

        if news.get("confidence", 0) >= 70:

            score += 5

            details.append(
                "الأخبار مؤثرة"
            )

        # -----------------------------
        # Fibonacci
        # -----------------------------

        if fibonacci.get(
            "signal",
            "WAIT"
        ) != "WAIT":

            score += 5

            details.append(
                "فيبوناتشي يدعم المنطقة"
            )



        # -----------------------------
        # Patterns
        # -----------------------------

        if patterns.get(
            "confidence",
            0
        ) >= 30:

            score += 5

            details.append(
                "نموذج سعري داعم"
            )

        # -----------------------------
        # Volume
        # -----------------------------

        if volume_analysis.get(
            "signal",
            "WAIT"
        ) != "WAIT":

            score += 5

            details.append(
                "تحليل الحجم يدعم الاتجاه"
            )

        # -----------------------------
        # Liquidity
        # -----------------------------

        if liquidity_analysis.get(
            "signal",
            "WAIT"
        ) != "WAIT":

            score += 5

            details.append(
                "السيولة تدعم القرار"
            )

        # -----------------------------
        # Order Blocks
        # -----------------------------

        if order_blocks_analysis.get(
            "signal",
            "WAIT"
        ) != "WAIT":

            score += 5

            details.append(
                "Order Block مؤثر"
            )

        # -----------------------------
        # Candle AI
        # -----------------------------

        if candle_analysis.get(
            "confidence",
            0
        ) >= 60:

            score += 5

            details.append(
                "نموذج شموع قوي"
            )

        # -----------------------------
        # Historical Learning
        # -----------------------------

        if historical_analysis.get(
            "confidence",
            0
        ) >= 60:

            score += 5

            details.append(
                "التاريخ يدعم السيناريو"
            )

        return (
            min(score, 100),
            details
        )

    # ==================================================
    # EARLY TREND DETECTOR
    # ==================================================

    def detect_early_trend(

        self,

        market,

        opportunity,

        smart_money,

        multi_timeframe,

        volume_analysis=None,

        liquidity_analysis=None,

        order_blocks_analysis=None,

        candle_analysis=None,

        historical_analysis=None

    ):

        bullish = 0
        bearish = 0

        if market.get(
            "momentum",
            0
        ) > 0:

            bullish += 1

        else:

            bearish += 1

        if opportunity.get(
            "signal",
            "WAIT"
        ) == "BUY":

            bullish += 2

        elif opportunity.get(
            "signal",
            "WAIT"
        ) == "SELL":

            bearish += 2

        if smart_money.get(
            "bullish",
            False
        ):

            bullish += 2

        if smart_money.get(
            "bearish",
            False
        ):

            bearish += 2



        mtf_signal = multi_timeframe.get(
            "signal",
            "WAIT"
        )

        if mtf_signal in [
            "BUY",
            "STRONG_BUY"
        ]:
            bullish += 1

        elif mtf_signal in [
            "SELL",
            "STRONG_SELL"
        ]:
            bearish += 1

        if volume_analysis:

            if volume_analysis.get(
                "bullish",
                False
            ):
                bullish += 1

            if volume_analysis.get(
                "bearish",
                False
            ):
                bearish += 1

        if liquidity_analysis:

            if liquidity_analysis.get(
                "bullish",
                False
            ):
                bullish += 1

            if liquidity_analysis.get(
                "bearish",
                False
            ):
                bearish += 1

        if order_blocks_analysis:

            if order_blocks_analysis.get(
                "bullish",
                False
            ):
                bullish += 1

            if order_blocks_analysis.get(
                "bearish",
                False
            ):
                bearish += 1

        if candle_analysis:

            if candle_analysis.get(
                "bullish",
                False
            ):
                bullish += 1

            if candle_analysis.get(
                "bearish",
                False
            ):
                bearish += 1

        if historical_analysis:

            if historical_analysis.get(
                "bullish",
                False
            ):
                bullish += 1

            if historical_analysis.get(
                "bearish",
                False
            ):
                bearish += 1

        if bullish >= 5 and bullish > bearish:
            return "EARLY_BULLISH"

        if bearish >= 5 and bearish > bullish:
            return "EARLY_BEARISH"

        return "NO_EARLY_SIGNAL"

    # ==================================================
    # FINAL DECISION
    # ==================================================

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

        volume_analysis=None,

        liquidity_analysis=None,

        order_blocks_analysis=None,

        candle_analysis=None,

        historical_analysis=None

    ):

        bullish = 0
        bearish = 0

        reasons = []
        warnings = []



        # ==========================
        # Trend
        # ==========================

        trend_score = trend.get("score", 0)

        if trend_score > 0:
            bullish += 2
            reasons.append("الاتجاه العام صاعد")

        elif trend_score < 0:
            bearish += 2
            reasons.append("الاتجاه العام هابط")

        # ==========================
        # Multi Timeframe
        # ==========================

        mtf_signal = multi_timeframe.get("signal", "WAIT")

        if mtf_signal in ("BUY", "STRONG_BUY"):
            bullish += 3
            reasons.append("توافق الفريمات يدعم الصعود")

        elif mtf_signal in ("SELL", "STRONG_SELL"):
            bearish += 3
            reasons.append("توافق الفريمات يدعم الهبوط")

        # ==========================
        # Opportunity Engine
        # ==========================

        opportunity_signal = opportunity.get("signal", "WAIT")

        if opportunity_signal == "BUY":
            bullish += 2
            reasons.append("Opportunity Engine BUY")

        elif opportunity_signal == "SELL":
            bearish += 2
            reasons.append("Opportunity Engine SELL")

        # ==========================
        # Smart Money
        # ==========================

        if smart_money.get("bullish", False):
            bullish += 2
            reasons.append("Smart Money Accumulation")

        if smart_money.get("bearish", False):
            bearish += 2
            reasons.append("Smart Money Distribution")

        # ==========================
        # Prediction AI
        # ==========================

        if prediction.get("bullish", False):
            bullish += 1

        if prediction.get("bearish", False):
            bearish += 1

        # ==========================
        # Fibonacci
        # ==========================

        fib_signal = fibonacci.get("signal", "WAIT")

        if fib_signal == "BUY":
            bullish += 1
            reasons.append("Fibonacci يدعم الشراء")

        elif fib_signal == "SELL":
            bearish += 1
            reasons.append("Fibonacci يدعم البيع")

        # ==========================
        # News AI
        # ==========================

        if news.get("bullish", False):
            bullish += 1
            reasons.append("الأخبار إيجابية")

        if news.get("bearish", False):
            bearish += 1
            reasons.append("الأخبار سلبية")

        # ==========================
        # Early Trend
        # ==========================

        if early_trend == "EARLY_BULLISH":
            bullish += 1
            reasons.append("بداية اتجاه صاعد مبكر")

        elif early_trend == "EARLY_BEARISH":
            bearish += 1
            reasons.append("بداية اتجاه هابط مبكر")



        # ==========================
        # Volume Analysis
        # ==========================

        if volume_analysis:

            if volume_analysis.get("bullish", False):
                bullish += 1
                reasons.append("الحجم يدعم الصعود")

            if volume_analysis.get("bearish", False):
                bearish += 1
                reasons.append("الحجم يدعم الهبوط")

        # ==========================
        # Liquidity Analysis
        # ==========================

        if liquidity_analysis:

            if liquidity_analysis.get("bullish", False):
                bullish += 1
                reasons.append("السيولة تشير للصعود")

            if liquidity_analysis.get("bearish", False):
                bearish += 1
                reasons.append("السيولة تشير للهبوط")

        # ==========================
        # Order Blocks
        # ==========================

        if order_blocks_analysis:

            if order_blocks_analysis.get("bullish", False):
                bullish += 1
                reasons.append("Bullish Order Block")

            if order_blocks_analysis.get("bearish", False):
                bearish += 1
                reasons.append("Bearish Order Block")

        # ==========================
        # Candle AI
        # ==========================

        if candle_analysis:

            if candle_analysis.get("bullish", False):
                bullish += 1
                reasons.append("شموع تدعم الشراء")

            if candle_analysis.get("bearish", False):
                bearish += 1
                reasons.append("شموع تدعم البيع")

        # ==========================
        # Historical Learning
        # ==========================

        if historical_analysis:

            if historical_analysis.get("bullish", False):
                bullish += 1
                reasons.append("التاريخ يدعم الصعود")

            if historical_analysis.get("bearish", False):
                bearish += 1
                reasons.append("التاريخ يدعم الهبوط")

        # ==========================
        # Signal Conflict Protection
        # ==========================

        if (
            bullish >= 5
            and
            bearish >= 5
            and
            abs(bullish - bearish) <= 2
        ):

            warnings.append(
                "تعارض بين محركات الذكاء الاصطناعي"
            )

            self.signal_statistics["wait"] += 1

            return (

                "WAIT",

                reasons,

                warnings,

                {
                    "bullish": bullish,
                    "bearish": bearish
                }

            )


        # ==========================
        # Final Signal
        # ==========================

        if (
            bullish >= self.minimum_signal_score
            and
            bullish > bearish
        ):

            reasons.append(
                "توافق عدة محركات للشراء"
            )

            self.signal_statistics["buy"] += 1

            return (

                "BUY",

                reasons,

                warnings,

                {
                    "bullish": bullish,
                    "bearish": bearish
                }

            )


        if (
            bearish >= self.minimum_signal_score
            and
            bearish > bullish
        ):

            reasons.append(
                "توافق عدة محركات للبيع"
            )

            self.signal_statistics["sell"] += 1

            return (

                "SELL",

                reasons,

                warnings,

                {
                    "bullish": bullish,
                    "bearish": bearish
                }

            )


        warnings.append(
            "لا يوجد توافق كافي"
        )

        self.signal_statistics["wait"] += 1


        return (

            "WAIT",

            reasons,

            warnings,

            {
                "bullish": bullish,
                "bearish": bearish
            }

            )



        # ==========================
        # Order Blocks
        # ==========================

        if order_blocks_analysis:

            if order_blocks_analysis.get("bullish", False):

                bullish += 1

                reasons.append(
                    "Bullish Order Block"
                )


            if order_blocks_analysis.get("bearish", False):

                bearish += 1

                reasons.append(
                    "Bearish Order Block"
                )


        # ==========================
        # Candle AI
        # ==========================

        if candle_analysis:

            if candle_analysis.get("bullish", False):

                bullish += 1

                reasons.append(
                    "شموع تدعم الشراء"
                )


            if candle_analysis.get("bearish", False):

                bearish += 1

                reasons.append(
                    "شموع تدعم البيع"
                )


        # ==========================
        # Historical Learning
        # ==========================

        if historical_analysis:

            if historical_analysis.get("bullish", False):

                bullish += 1

                reasons.append(
                    "التاريخ يدعم الصعود"
                )


            if historical_analysis.get("bearish", False):

                bearish += 1

                reasons.append(
                    "التاريخ يدعم الهبوط"
                )


        # ==========================
        # Filters
        # ==========================

        if self.enable_news_filter:

            if news.get("confidence", 0) < 20:

                warnings.append(
                    "ضعف تأثير الأخبار"
                )


        if self.enable_fibonacci_filter:

            if fibonacci.get(
                "signal",
                "WAIT"
            ) == "WAIT":

                warnings.append(
                    "لا يوجد دعم فيبوناتشي"
                )


        if self.enable_mtf_filter:

            if multi_timeframe.get(
                "confidence",
                0
            ) < 40:

                warnings.append(
                    "ضعف توافق الفريمات"
                )


        # ==========================
        # Conflict Detection
        # ==========================

        if (
            bullish >= 5
            and
            bearish >= 5
            and
            abs(bullish - bearish) <= 2
        ):

            warnings.append(
                "تعارض بين المحركات"
            )

            return (

                "WAIT",

                reasons,

                warnings,

                {
                    "bullish": bullish,
                    "bearish": bearish
                }

            )


        # ==========================
        # Final Signal
        # ==========================

        if bullish >= self.minimum_signal_score and bullish > bearish:

            self.signal_statistics["buy"] += 1

            reasons.append(
                "توافق المحركات للشراء"
            )

            return (

                "BUY",

                reasons,

                warnings,

                {
                    "bullish": bullish,
                    "bearish": bearish
                }

            )


        if bearish >= self.minimum_signal_score and bearish > bullish:

            self.signal_statistics["sell"] += 1

            reasons.append(
                "توافق المحركات للبيع"
            )

            return (

                "SELL",

                reasons,

                warnings,

                {
                    "bullish": bullish,
                    "bearish": bearish
                }

            )


        self.signal_statistics["wait"] += 1

        warnings.append(
            "لا يوجد توافق كافي"
        )


        return (

            "WAIT",

            reasons,

            warnings,

            {
                "bullish": bullish,
                "bearish": bearish
            }

                )



    # ==================================================
    # ENGINE STATUS
    # ==================================================

    def get_engine_status(
        self
    ) -> Dict[str, Any]:

        return {

            "engine": "SignalEngine",

            "status": "running",

            "configuration": {

                "minimum_confidence": self.minimum_confidence,

                "minimum_signal_score": self.minimum_signal_score,

                "maximum_confidence": self.maximum_confidence,

                "counter_trend": self.allow_counter_trend

            },


            "filters": {

                "news": self.enable_news_filter,

                "fibonacci": self.enable_fibonacci_filter,

                "smart_money": self.enable_smart_money_filter,

                "volume": self.enable_volume_filter,

                "liquidity": self.enable_liquidity_filter,

                "order_blocks": self.enable_orderblock_filter,

                "candles": self.enable_candle_filter,

                "history": self.enable_history_filter,

                "multi_timeframe": self.enable_mtf_filter

            },


            "modules": {

                "market": True,

                "trend": True,

                "patterns": True,

                "smart_money": True,

                "prediction": True,

                "risk": True,

                "news": True,

                "fibonacci": True,

                "opportunity": True,

                "multi_timeframe": True,

                "volume": True,

                "liquidity": True,

                "order_blocks": True,

                "candles_ai": True,

                "historical_learning": True

            },


            "statistics": self.signal_statistics

        }
