from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

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


# ==========================================================
# FALCONAI SIGNAL ENGINE V4 PRODUCTION
# ==========================================================

class SignalEngine:
    """
    FalconAI Institutional Production Signal Engine

    Responsibilities:
    - Validate market data
    - Detect market regime
    - Aggregate AI engines
    - Score opportunities
    - Calculate confidence
    - Risk filtering
    - Multi timeframe confirmation
    - Produce final signal
    """

    def __init__(self):

        # ==================================================
        # CORE ENGINES
        # ==================================================

        self.market = MarketAnalyzer()
        self.trend = TrendEngine()
        self.patterns = PatternAnalyzer()
        self.smart_money = SmartMoneyAnalyzer()
        self.prediction = PredictionEngine()
        self.risk = RiskManager()
        self.news = NewsAnalyzer()
        self.fibonacci = FibonacciAnalyzer()

        # ==================================================
        # OPPORTUNITY ENGINES
        # ==================================================

        self.opportunity = OpportunityEngine()
        self.multi_timeframe = MultiTimeframeEngine()
        self.volume = VolumeEngine()
        self.liquidity = LiquidityEngine()
        self.order_blocks = OrderBlocksEngine()
        self.candles_ai = CandlesAI()
        self.history = HistoricalLearning()

        # ==================================================
        # ECONOMIC FILTER
        # ==================================================

        self.enable_economic_filter = True

        if EconomicCalendar:
            self.economic = EconomicCalendar()
        else:
            self.economic = None

        # ==================================================
        # CONFIGURATION
        # ==================================================

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
            "1M",
        ]

        self.minimum_confidence = 60
        self.minimum_confirmations = 4

        self.maximum_confidence = 100

        self.minimum_score = 45
        self.maximum_score = 100

        self.reject_conflicting_signals = True

        self.minimum_data_quality = 70

        self.provider_difference_limit = 1.0

        # ==================================================
        # ENGINE STATE
        # ==================================================

        self.version = "V4_PRODUCTION"

        self.active = True

        self.last_signal = None

        self.analysis_count = 0

        self.success_count = 0

        self.error_count = 0

        self.last_analysis_time = None



# ==========================================================
# HEALTH CHECK
# ==========================================================

    def health_check(self):

        components = {

            "market": self.market is not None,

            "trend": self.trend is not None,

            "patterns": self.patterns is not None,

            "smart_money": self.smart_money is not None,

            "prediction": self.prediction is not None,

            "risk": self.risk is not None,

            "news": self.news is not None,

            "fibonacci": self.fibonacci is not None,

            "opportunity": self.opportunity is not None,

            "multi_timeframe": self.multi_timeframe is not None,

            "volume": self.volume is not None,

            "liquidity": self.liquidity is not None,

            "order_blocks": self.order_blocks is not None,

            "candles_ai": self.candles_ai is not None,

            "history": self.history is not None

        }

        healthy = all(

            components.values()

        )

        return {

            "status":

                "healthy"

                if healthy

                else

                "degraded",

            "version":

                self.version,

            "analysis_count":

                self.analysis_count,

            "success_count":

                self.success_count,

            "error_count":

                self.error_count,

            "components":

                components

        }


# ==========================================================
# MARKET DATA QUALITY
# ==========================================================

    def validate_market_data_quality(

        self,

        market_data,

        providers_data=None

    ):

        score = 100

        warnings = []

        candles = market_data.get(

            "candles",

            []

        )

        price = market_data.get(

            "price",

            0

        )

        volume = market_data.get(

            "volume",

            0

        )

        candle_count = len(

            candles

        )

        if candle_count < 50:

            score -= 30

            warnings.append(

                "MISSING_CANDLES"

            )

        elif candle_count < 100:

            score -= 15

        if price <= 0:

            score -= 40

            warnings.append(

                "INVALID_PRICE"

            )

        if volume <= 0:

            score -= 20

            warnings.append(

                "INVALID_VOLUME"

            )

        if providers_data:

            valid_prices = []

            for provider in providers_data:

                p = provider.get(

                    "price",

                    0

                )

                if p > 0:

                    valid_prices.append(

                        p

                    )

            if len(valid_prices) >= 2:

                highest = max(

                    valid_prices

                )

                lowest = min(

                    valid_prices

                )

                deviation = (

                    (

                        highest

                        -

                        lowest

                    )

                    /

                    lowest

                ) * 100

                if deviation > self.provider_difference_limit:

                    score -= 20

                    warnings.append(

                        "PROVIDER_MISMATCH"

                    )

        score = max(

            0,

            min(

                score,

                100

            )

        )

        if score >= 90:

            quality = "EXCELLENT"

        elif score >= 75:

            quality = "HIGH"

        elif score >= 60:

            quality = "MEDIUM"

        elif score >= 40:

            quality = "LOW"

        else:

            quality = "VERY_LOW"

        return {

            "score": score,

            "quality": quality,

            "warnings": warnings

        }


# ==========================================================
# MARKET REGIME
# ==========================================================

    def detect_market_regime(

        self,

        market_data

    ):

        trend = market_data.get(

            "trend",

            {}

        )

        volatility = market_data.get(

            "volatility",

            0

        )

        strength = trend.get(

            "strength",

            0

        )

        if strength >= 70 and volatility >= 60:

            return "TRENDING"

        if volatility >= 80:

            return "VOLATILE"

        return "RANGING"


# ==========================================================
# CONFIDENCE ENGINE
# ==========================================================

    def calculate_confidence(

        self,

        buy_score,

        sell_score,

        confirmations=0

    ):

        confidence = max(

            buy_score,

            sell_score

        )

        confidence += min(

            confirmations * 2,

            10

        )

        confidence = max(

            0,

            min(

                confidence,

                self.maximum_confidence

            )

        )

        return round(

            confidence,

            2

            )



# ==========================================================
# SIGNAL QUALITY ENGINE
# ==========================================================

    def evaluate_signal_quality(

        self,

        confidence,

        confirmations,

        market_regime,

        market_quality,

        trend,

        smart_money,

        volume

    ):

        score = 0

        reasons = []

        if confidence >= 90:

            score += 30

        elif confidence >= 80:

            score += 25

        elif confidence >= 70:

            score += 20

        elif confidence >= 60:

            score += 10

        else:

            reasons.append(

                "LOW_CONFIDENCE"

            )

        if confirmations >= 8:

            score += 20

        elif confirmations >= 6:

            score += 15

        elif confirmations >= 4:

            score += 10

        else:

            reasons.append(

                "WEAK_CONFIRMATIONS"

            )

        if market_regime == "TRENDING":

            score += 10

        elif market_regime == "VOLATILE":

            score += 5

        else:

            score -= 10

            reasons.append(

                "RANGING_MARKET"

            )

        if market_quality.get(

            "score",

            0

        ) >= 90:

            score += 10

        elif market_quality.get(

            "score",

            0

        ) >= 75:

            score += 5

        else:

            score -= 10

            reasons.append(

                "BAD_DATA_QUALITY"

            )

        if trend.get(

            "strength",

            0

        ) >= 70:

            score += 5

        if smart_money.get(

            "bullish"

        ):

            score += 5

        if smart_money.get(

            "bearish"

        ):

            score += 5

        if volume.get(

            "score",

            0

        ) > 0:

            score += 5

        score = max(

            0,

            min(

                score,

                100

            )

        )

        if score >= 90:

            quality = "A+"

        elif score >= 80:

            quality = "A"

        elif score >= 70:

            quality = "B"

        elif score >= 60:

            quality = "C"

        else:

            quality = "D"

        return {

            "quality": quality,

            "score": score,

            "accepted": score >= self.minimum_score,

            "reasons": reasons

        }


# ==========================================================
# DECISION ENGINE
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

        difference = abs(

            buy_score - sell_score

        )

        if difference < 10:

            return {

                "signal": "WAIT",

                "confidence": confidence,

                "reason": "NO_CLEAR_DIRECTION"

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



# ==========================================================
# MAIN ANALYSIS ENGINE
# ==========================================================

    def analyze(

        self,

        symbol,

        market="crypto",

        timeframe="15m"

    ):

        self.analysis_count += 1

        try:

            market_data = self.market.analyze(

                symbol,

                timeframe

            )

            if not market_data:

                self.error_count += 1

                return {

                    "signal": "WAIT",

                    "confidence": 0,

                    "reason": "NO_MARKET_DATA"

                }

            market_quality = self.validate_market_data_quality(

                market_data

            )

            if market_quality["score"] < self.minimum_data_quality:

                self.error_count += 1

                return {

                    "signal": "WAIT",

                    "confidence": 0,

                    "reason": "LOW_DATA_QUALITY",

                    "quality": market_quality

                }

            market_regime = self.detect_market_regime(

                market_data

            )

            trend_result = self.trend.analyze(

                market_data

            )

            pattern_result = self.patterns.analyze(

                market_data

            )

            smart_money_result = self.smart_money.analyze(

                market_data

            )

            prediction_result = self.prediction.predict(

                market_data

            )

            opportunity_result = self.opportunity.analyze(

                symbol,

                market,

                timeframe

            )

            timeframe_result = self.analyze_all_timeframes(

                symbol,

                market

            )

            risk_result = self.risk.analyze(

                market_data

            )

            buy_score = 0

            sell_score = 0

            confirmations = 0

            reasons = []

            if trend_result.get("direction") == "UP":

                buy_score += 20

                confirmations += 1

                reasons.append("TREND_UP")

            elif trend_result.get("direction") == "DOWN":

                sell_score += 20

                confirmations += 1

                reasons.append("TREND_DOWN")

            if smart_money_result.get("bullish"):

                buy_score += 20

                confirmations += 1

                reasons.append("SMART_MONEY_BUY")

            if smart_money_result.get("bearish"):

                sell_score += 20

                confirmations += 1

                reasons.append("SMART_MONEY_SELL")

            if opportunity_result.get("signal") == "BUY":

                buy_score += 20

                confirmations += 1

            elif opportunity_result.get("signal") == "SELL":

                sell_score += 20

                confirmations += 1

            if prediction_result.get("signal") == "BUY":

                buy_score += 15

                confirmations += 1

            elif prediction_result.get("signal") == "SELL":

                sell_score += 15

                confirmations += 1

            confidence = self.calculate_confidence(

                buy_score,

                sell_score,

                confirmations

            )

            quality = self.evaluate_signal_quality(

                confidence,

                confirmations,

                market_regime,

                market_quality,

                trend_result,

                smart_money_result,

                self.volume.analyze(market_data)

            )

            decision = self.make_decision(

                buy_score,

                sell_score,

                confidence

            )

            if not quality["accepted"]:

                decision["signal"] = "WAIT"

                reasons.extend(

                    quality["reasons"]

                )

            gate = self.external_risk_gate(

                confidence,

                risk_result,

                market_regime

            )

            if not gate["allowed"]:

                decision["signal"] = "WAIT"

                reasons.append(

                    gate["reason"]

                )

            self.success_count += 1

            self.last_signal = decision["signal"]

            self.last_analysis_time = datetime.utcnow()

            return {

                "symbol": symbol,

                "market": market,

                "timeframe": timeframe,

                "signal": decision["signal"],

                "confidence": confidence,

                "buy_score": buy_score,

                "sell_score": sell_score,

                "confirmations": confirmations,

                "quality": quality,

                "market_quality": market_quality,

                "market_regime": market_regime,

                "trend": trend_result,

                "patterns": pattern_result,

                "smart_money": smart_money_result,

                "prediction": prediction_result,

                "opportunity": opportunity_result,

                "multi_timeframe": timeframe_result,

                "risk": risk_result,

                "reasons": reasons

            }

        except Exception as e:

            self.error_count += 1

            return {

                "signal": "WAIT",

                "confidence": 0,

                "error": str(e)

                }



# ==========================================================
# SIGNAL HISTORY
# ==========================================================

    def get_last_signal(self):

        return self.last_signal


# ==========================================================
# ENGINE STATISTICS
# ==========================================================

    def get_statistics(self):

        success_rate = 0

        if self.analysis_count > 0:

            success_rate = (

                self.success_count

                /

                self.analysis_count

            ) * 100

        return {

            "version": self.version,

            "active": self.active,

            "analysis_count": self.analysis_count,

            "success_count": self.success_count,

            "error_count": self.error_count,

            "success_rate": round(

                success_rate,

                2

            ),

            "last_signal": self.last_signal,

            "last_analysis_time": self.last_analysis_time

        }


# ==========================================================
# ENGINE RESET
# ==========================================================

    def reset_statistics(self):

        self.analysis_count = 0

        self.success_count = 0

        self.error_count = 0

        self.last_signal = None

        self.last_analysis_time = None

        return True


# ==========================================================
# ENABLE / DISABLE ENGINE
# ==========================================================

    def enable(self):

        self.active = True


    def disable(self):

        self.active = False


# ==========================================================
# PROVIDER STATUS
# ==========================================================

    def provider_status(self):

        return {

            "market": self.market is not None,

            "trend": self.trend is not None,

            "patterns": self.patterns is not None,

            "smart_money": self.smart_money is not None,

            "prediction": self.prediction is not None,

            "risk": self.risk is not None,

            "news": self.news is not None,

            "fibonacci": self.fibonacci is not None,

            "opportunity": self.opportunity is not None,

            "multi_timeframe": self.multi_timeframe is not None,

            "volume": self.volume is not None,

            "liquidity": self.liquidity is not None,

            "order_blocks": self.order_blocks is not None,

            "candles_ai": self.candles_ai is not None,

            "history": self.history is not None,

            "economic":

                self.economic is not None

        }



# ==========================================================
# SIGNAL EXPLANATION
# ==========================================================

    def build_signal_explanation(

        self,

        signal,

        confidence,

        buy_score,

        sell_score,

        reasons

    ):

        explanation = []

        explanation.append(

            f"Final Signal : {signal}"

        )

        explanation.append(

            f"Confidence : {confidence:.2f}%"

        )

        explanation.append(

            f"Buy Score : {buy_score}"

        )

        explanation.append(

            f"Sell Score : {sell_score}"

        )

        if reasons:

            explanation.append(

                "Reasons:"

            )

            for reason in reasons:

                explanation.append(

                    f"- {reason}"

                )

        return explanation


# ==========================================================
# SIGNAL EXPORT
# ==========================================================

    def export_signal(

        self,

        signal_data

    ):

        return {

            "created":

                datetime.utcnow().isoformat(),

            "engine":

                self.version,

            "data":

                signal_data

        }


# ==========================================================
# CONFIRMATION ENGINE
# ==========================================================

    def count_confirmations(

        self,

        trend,

        smart_money,

        prediction,

        opportunity,

        volume

    ):

        confirmations = 0

        if trend.get("direction"):

            confirmations += 1

        if smart_money.get("bullish") or smart_money.get("bearish"):

            confirmations += 1

        if prediction.get("signal"):

            confirmations += 1

        if opportunity.get("signal"):

            confirmations += 1

        if volume.get("score", 0) > 0:

            confirmations += 1

        return confirmations


# ==========================================================
# SCORE NORMALIZATION
# ==========================================================

    def normalize_score(

        self,

        score

    ):

        return max(

            0,

            min(

                int(score),

                100

            )

        )


# ==========================================================
# ENGINE VERSION
# ==========================================================

    def get_version(

        self

    ):

        return self.version



# ==========================================================
# SIGNAL FUSION ENGINE
# ==========================================================

    def fuse_signals(

        self,

        trend,

        prediction,

        smart_money,

        opportunity,

        multi_timeframe

    ):

        buy_score = 0

        sell_score = 0

        signals = []

        # ======================================
        # Trend
        # ======================================

        if trend.get("direction") == "UP":

            buy_score += 20

            signals.append("TREND_BUY")

        elif trend.get("direction") == "DOWN":

            sell_score += 20

            signals.append("TREND_SELL")

        # ======================================
        # Prediction
        # ======================================

        if prediction.get("signal") == "BUY":

            buy_score += 15

            signals.append("AI_BUY")

        elif prediction.get("signal") == "SELL":

            sell_score += 15

            signals.append("AI_SELL")

        # ======================================
        # Smart Money
        # ======================================

        if smart_money.get("bullish"):

            buy_score += 25

            signals.append("SMART_BUY")

        if smart_money.get("bearish"):

            sell_score += 25

            signals.append("SMART_SELL")

        # ======================================
        # Opportunity
        # ======================================

        if opportunity.get("signal") == "BUY":

            buy_score += 20

            signals.append("ENTRY_BUY")

        elif opportunity.get("signal") == "SELL":

            sell_score += 20

            signals.append("ENTRY_SELL")

        # ======================================
        # Multi Timeframe
        # ======================================

        agreement = multi_timeframe.get(

            "agreement",

            0

        )

        if agreement >= 80:

            buy_score += 10

            sell_score += 10

        return {

            "buy_score": buy_score,

            "sell_score": sell_score,

            "signals": signals

        }


# ==========================================================
# SIGNAL FILTER
# ==========================================================

    def filter_signal(

        self,

        signal,

        confidence,

        agreement

    ):

        if signal == "WAIT":

            return False

        if confidence < self.minimum_confidence:

            return False

        if agreement < 50:

            return False

        return True



# ==========================================================
# ENTRY / EXIT ENGINE
# ==========================================================

    def calculate_trade_levels(

        self,

        signal,

        market_data,

        risk

    ):

        price = market_data.get(

            "price",

            0

        )

        atr = market_data.get(

            "atr",

            0

        )

        if atr <= 0:

            atr = price * 0.01

        if signal == "BUY":

            stop_loss = price - (atr * 2)

            take_profit_1 = price + (atr * 2)

            take_profit_2 = price + (atr * 4)

            take_profit_3 = price + (atr * 6)

        elif signal == "SELL":

            stop_loss = price + (atr * 2)

            take_profit_1 = price - (atr * 2)

            take_profit_2 = price - (atr * 4)

            take_profit_3 = price - (atr * 6)

        else:

            stop_loss = price

            take_profit_1 = price

            take_profit_2 = price

            take_profit_3 = price

        risk_reward = 0

        if abs(price - stop_loss) > 0:

            risk_reward = round(

                abs(

                    take_profit_2 - price

                )

                /

                abs(

                    price - stop_loss

                ),

                2

            )

        return {

            "entry": price,

            "stop_loss": round(stop_loss, 8),

            "tp1": round(take_profit_1, 8),

            "tp2": round(take_profit_2, 8),

            "tp3": round(take_profit_3, 8),

            "risk_reward": risk_reward

        }


# ==========================================================
# POSITION SIZE ENGINE
# ==========================================================

    def calculate_position_size(

        self,

        account_balance,

        risk_percent,

        entry,

        stop_loss

    ):

        risk_amount = (

            account_balance

            *

            risk_percent

            /

            100

        )

        distance = abs(

            entry - stop_loss

        )

        if distance <= 0:

            return 0

        position = risk_amount / distance

        return round(

            position,

            4

        )



# ==========================================================
# TRADE MANAGEMENT ENGINE
# ==========================================================

    def manage_open_position(

        self,

        signal,

        current_price,

        entry_price,

        stop_loss,

        take_profit

    ):

        status = "HOLD"

        pnl = 0

        if signal == "BUY":

            pnl = current_price - entry_price

            if current_price >= take_profit:

                status = "TAKE_PROFIT"

            elif current_price <= stop_loss:

                status = "STOP_LOSS"

        elif signal == "SELL":

            pnl = entry_price - current_price

            if current_price <= take_profit:

                status = "TAKE_PROFIT"

            elif current_price >= stop_loss:

                status = "STOP_LOSS"

        return {

            "status": status,

            "profit": round(

                pnl,

                8

            )

        }


# ==========================================================
# TRAILING STOP ENGINE
# ==========================================================

    def trailing_stop(

        self,

        signal,

        current_price,

        current_stop,

        atr

    ):

        if atr <= 0:

            return current_stop

        if signal == "BUY":

            new_stop = max(

                current_stop,

                current_price - atr * 1.5

            )

        elif signal == "SELL":

            new_stop = min(

                current_stop,

                current_price + atr * 1.5

            )

        else:

            new_stop = current_stop

        return round(

            new_stop,

            8

        )


# ==========================================================
# BREAK EVEN ENGINE
# ==========================================================

    def break_even(

        self,

        signal,

        entry,

        current_price,

        stop_loss,

        atr

    ):

        if atr <= 0:

            return stop_loss

        trigger = atr * 2

        if signal == "BUY":

            if current_price - entry >= trigger:

                return entry

        elif signal == "SELL":

            if entry - current_price >= trigger:

                return entry

        return stop_loss



# ==========================================================
# DYNAMIC TAKE PROFIT ENGINE
# ==========================================================

    def calculate_dynamic_targets(

        self,

        signal,

        entry,

        atr,

        confidence,

        market_regime

    ):

        multiplier = 2


        if confidence >= 90:

            multiplier = 4

        elif confidence >= 80:

            multiplier = 3


        if market_regime == "VOLATILE":

            multiplier += 1


        if signal == "BUY":

            targets = {

                "tp1":

                    entry + (atr * multiplier),

                "tp2":

                    entry + (atr * multiplier * 2),

                "tp3":

                    entry + (atr * multiplier * 3)

            }


        elif signal == "SELL":

            targets = {

                "tp1":

                    entry - (atr * multiplier),

                "tp2":

                    entry - (atr * multiplier * 2),

                "tp3":

                    entry - (atr * multiplier * 3)

            }


        else:

            targets = {

                "tp1": entry,

                "tp2": entry,

                "tp3": entry

            }


        return {

            "targets": {

                key: round(value, 8)

                for key, value in targets.items()

            },

            "multiplier": multiplier

        }



# ==========================================================
# PARTIAL EXIT MANAGEMENT
# ==========================================================

    def calculate_partial_exit(

        self,

        current_price,

        entry,

        tp1,

        tp2,

        tp3

    ):

        progress = 0

        if tp3 != entry:

            progress = (

                abs(current_price - entry)

                /

                abs(tp3 - entry)

            ) * 100


        if progress >= 100:

            stage = "FULL_EXIT"

            close_percent = 100


        elif progress >= 66:

            stage = "TP3"

            close_percent = 50


        elif progress >= 33:

            stage = "TP2"

            close_percent = 30


        elif progress > 0:

            stage = "TP1"

            close_percent = 20


        else:

            stage = "RUNNING"

            close_percent = 0


        return {

            "stage": stage,

            "close_percent": close_percent,

            "progress": round(

                progress,

                2

            )

        }



# ==========================================================
# POSITION MONITOR ENGINE
# ==========================================================

    def monitor_position(

        self,

        position,

        market_price

    ):

        entry = position.get(

            "entry",

            0

        )

        stop = position.get(

            "stop_loss",

            0

        )

        tp = position.get(

            "take_profit",

            0

        )

        signal = position.get(

            "signal",

            "WAIT"

        )


        result = {

            "status": "ACTIVE",

            "signal": signal,

            "distance_stop": abs(

                market_price - stop

            ),

            "distance_target": abs(

                tp - market_price

            )

        }


        if signal == "BUY":

            if market_price <= stop:

                result["status"] = "STOPPED"


            elif market_price >= tp:

                result["status"] = "TARGET_REACHED"


        elif signal == "SELL":

            if market_price >= stop:

                result["status"] = "STOPPED"


            elif market_price <= tp:

                result["status"] = "TARGET_REACHED"


        return result



# ==========================================================
# AI LEARNING FEEDBACK ENGINE
# ==========================================================

    def record_signal_result(

        self,

        signal,

        confidence,

        entry,

        exit_price,

        result

    ):

        profit = 0

        if signal == "BUY":

            profit = exit_price - entry

        elif signal == "SELL":

            profit = entry - exit_price


        success = profit > 0


        feedback = {

            "signal": signal,

            "confidence": confidence,

            "entry": entry,

            "exit": exit_price,

            "profit": round(

                profit,

                8

            ),

            "success": success,

            "timestamp":

                datetime.utcnow().isoformat()

        }


        if hasattr(

            self.history,

            "save"

        ):

            try:

                self.history.save(

                    feedback

                )

            except Exception:

                pass


        return feedback



# ==========================================================
# PERFORMANCE ANALYZER
# ==========================================================

    def analyze_performance(

        self,

        trades

    ):

        total = len(trades)

        if total == 0:

            return {

                "accuracy": 0,

                "wins": 0,

                "losses": 0

            }


        wins = 0

        losses = 0

        profit = 0


        for trade in trades:

            if trade.get(

                "success"

            ):

                wins += 1

            else:

                losses += 1


            profit += trade.get(

                "profit",

                0

            )


        accuracy = (

            wins

            /

            total

        ) * 100


        return {

            "total_trades": total,

            "wins": wins,

            "losses": losses,

            "accuracy": round(

                accuracy,

                2

            ),

            "net_profit": round(

                profit,

                8

            )

        }



# ==========================================================
# CONFIDENCE ADAPTATION ENGINE
# ==========================================================

    def adjust_confidence_from_history(

        self,

        confidence,

        performance

    ):

        accuracy = performance.get(

            "accuracy",

            0

        )


        adjusted = confidence


        if accuracy >= 75:

            adjusted += 5


        elif accuracy < 45:

            adjusted -= 10


        return min(

            max(

                adjusted,

                0

            ),

            100

        )



# ==========================================================
# MARKET MEMORY ENGINE
# ==========================================================

    def remember_market_state(

        self,

        symbol,

        market_regime,

        signal,

        confidence

    ):

        memory = {

            "symbol": symbol,

            "regime": market_regime,

            "signal": signal,

            "confidence": confidence,

            "time":

                datetime.utcnow().isoformat()

        }


        if hasattr(

            self.history,

            "store"

        ):

            try:

                self.history.store(

                    memory

                )

            except Exception:

                pass


        return memory



# ==========================================================
# INSTITUTIONAL SMART MONEY FILTER
# ==========================================================

    def institutional_filter(

        self,

        smart_money,

        liquidity,

        order_blocks,

        volume

    ):

        score = 0

        confirmations = []


        # ======================================
        # BOS / CHOCH
        # ======================================

        if smart_money.get("bos"):

            score += 20

            confirmations.append(

                "BREAK_OF_STRUCTURE"

            )


        if smart_money.get("choch"):

            score += 15

            confirmations.append(

                "CHANGE_OF_CHARACTER"

            )


        # ======================================
        # Liquidity
        # ======================================

        if liquidity.get("liquidity_sweep"):

            score += 20

            confirmations.append(

                "LIQUIDITY_SWEEP"

            )


        # ======================================
        # Order Blocks
        # ======================================

        if order_blocks.get("valid"):

            score += 20

            confirmations.append(

                "VALID_ORDER_BLOCK"

            )


        # ======================================
        # Volume Confirmation
        # ======================================

        if volume.get("score", 0) >= 70:

            score += 15

            confirmations.append(

                "STRONG_VOLUME"

            )


        accepted = score >= 50


        return {

            "institutional_score": min(

                score,

                100

            ),

            "accepted": accepted,

            "confirmations": confirmations

        }



# ==========================================================
# FAKE BREAKOUT DETECTOR
# ==========================================================

    def detect_fake_breakout(

        self,

        price_action,

        volume,

        support_resistance

    ):

        fake = False

        reasons = []


        breakout = price_action.get(

            "breakout",

            False

        )


        volume_strength = volume.get(

            "score",

            0

        )


        level_broken = support_resistance.get(

            "broken_level",

            False

        )


        if breakout and volume_strength < 40:

            fake = True

            reasons.append(

                "LOW_VOLUME_BREAKOUT"

            )


        if breakout and not level_broken:

            fake = True

            reasons.append(

                "INVALID_LEVEL_BREAK"

            )


        return {

            "fake_breakout": fake,

            "warnings": reasons

        }



# ==========================================================
# LIQUIDITY PROTECTION ENGINE
# ==========================================================

    def liquidity_protection(

        self,

        liquidity_data,

        signal

    ):

        blocked = False

        reason = None


        if liquidity_data.get(

            "trap"

        ):

            blocked = True

            reason = "LIQUIDITY_TRAP"


        if liquidity_data.get(

            "stop_hunt"

        ):

            blocked = True

            reason = "STOP_HUNT_DETECTED"


        return {

            "blocked": blocked,

            "reason": reason,

            "signal": signal

        }



# ==========================================================
# NEWS IMPACT FILTER ENGINE
# ==========================================================

    def news_impact_filter(

        self,

        news_data,

        signal

    ):

        impact = news_data.get(

            "impact",

            "LOW"

        )

        blocked = False

        reason = None


        if impact == "HIGH":

            blocked = True

            reason = "HIGH_IMPACT_NEWS"


        if news_data.get(

            "market_uncertainty"

        ):

            blocked = True

            reason = "MARKET_UNCERTAIN"


        return {

            "blocked": blocked,

            "reason": reason,

            "signal": signal,

            "impact": impact

        }



# ==========================================================
# ECONOMIC CALENDAR GATE
# ==========================================================

    def economic_filter(

        self,

        economic_data

    ):

        if not self.enable_economic_filter:

            return {

                "allowed": True,

                "reason": "DISABLED"

            }


        if self.economic is None:

            return {

                "allowed": True,

                "reason": "NO_ECONOMIC_ENGINE"

            }


        event = economic_data.get(

            "high_impact",

            False

        )


        if event:

            return {

                "allowed": False,

                "reason": "ECONOMIC_EVENT_NEAR"

            }


        return {

            "allowed": True,

            "reason": "CLEAR"

        }



# ==========================================================
# MARKET SHOCK PROTECTION ENGINE
# ==========================================================

    def market_shock_protection(

        self,

        market_data

    ):

        volatility = market_data.get(

            "volatility",

            0

        )


        price_change = market_data.get(

            "price_change",

            0

        )


        warnings = []


        shocked = False


        if volatility >= 90:

            shocked = True

            warnings.append(

                "EXTREME_VOLATILITY"

            )


        if abs(price_change) >= 10:

            shocked = True

            warnings.append(

                "ABNORMAL_PRICE_MOVE"

            )


        return {

            "shock": shocked,

            "warnings": warnings

        }



# ==========================================================
# FINAL SAFETY PIPELINE
# ==========================================================

    def final_safety_pipeline(

        self,

        signal,

        confidence,

        market_data,

        news_data=None,

        economic_data=None

    ):

        blocks = []


        if news_data:

            news_check = self.news_impact_filter(

                news_data,

                signal

            )

            if news_check["blocked"]:

                blocks.append(

                    news_check["reason"]

                )


        if economic_data:

            economic_check = self.economic_filter(

                economic_data

            )

            if not economic_check["allowed"]:

                blocks.append(

                    economic_check["reason"]

                )


        shock_check = self.market_shock_protection(

            market_data

        )


        if shock_check["shock"]:

            blocks.extend(

                shock_check["warnings"]

            )


        allowed = len(blocks) == 0


        return {

            "allowed": allowed,

            "signal":

                signal if allowed else "WAIT",

            "confidence":

                confidence,

            "blocks": blocks

            }



# ==========================================================
# ADVANCED RISK MANAGER ENGINE
# ==========================================================

    def calculate_dynamic_risk(

        self,

        confidence,

        volatility,

        market_regime,

        account_balance,

        stop_distance

    ):

        risk_score = 100

        warnings = []


        # ======================================
        # Confidence Impact
        # ======================================

        if confidence >= 85:

            risk_score += 5

        elif confidence < 60:

            risk_score -= 25

            warnings.append(

                "LOW_SIGNAL_CONFIDENCE"

            )


        # ======================================
        # Volatility Impact
        # ======================================

        if volatility >= 90:

            risk_score -= 30

            warnings.append(

                "EXTREME_VOLATILITY"

            )

        elif volatility >= 70:

            risk_score -= 15



        # ======================================
        # Market Condition
        # ======================================

        if market_regime == "RANGING":

            risk_score -= 20

            warnings.append(

                "RANGING_MARKET"

            )


        elif market_regime == "TRENDING":

            risk_score += 10



        # ======================================
        # Stop Distance
        # ======================================

        if stop_distance <= 0:

            risk_score -= 40

            warnings.append(

                "INVALID_STOP_DISTANCE"

            )


        # ======================================
        # Final Risk
        # ======================================

        risk_score = max(

            0,

            min(

                risk_score,

                100

            )

        )


        if risk_score >= 80:

            level = "LOW"


        elif risk_score >= 60:

            level = "MEDIUM"


        elif risk_score >= 40:

            level = "HIGH"


        else:

            level = "EXTREME"



        return {

            "risk_score": risk_score,

            "risk_level": level,

            "warnings": warnings

        }



# ==========================================================
# CAPITAL PROTECTION ENGINE
# ==========================================================

    def calculate_position_size(

        self,

        balance,

        risk_percent,

        entry,

        stop_loss

    ):

        if balance <= 0:

            return 0


        if entry <= 0 or stop_loss <= 0:

            return 0


        risk_amount = (

            balance

            *

            risk_percent

            /

            100

        )


        distance = abs(

            entry - stop_loss

        )


        if distance == 0:

            return 0


        position_size = (

            risk_amount

            /

            distance

        )


        return round(

            position_size,

            8

        )



# ==========================================================
# RISK REWARD CALCULATOR
# ==========================================================

    def calculate_risk_reward(

        self,

        entry,

        stop_loss,

        take_profit

    ):

        risk = abs(

            entry - stop_loss

        )


        reward = abs(

            take_profit - entry

        )


        if risk == 0:

            return 0


        return round(

            reward / risk,

            2

        )



# ==========================================================
# LOSS PROTECTION SYSTEM
# ==========================================================

    def loss_protection(

        self,

        daily_loss,

        max_loss

    ):

        if max_loss <= 0:

            return {

                "blocked": True,

                "reason": "INVALID_LIMIT"

            }


        if daily_loss >= max_loss:

            return {

                "blocked": True,

                "reason": "DAILY_LOSS_LIMIT"

            }


        return {

            "blocked": False,

            "reason": "SAFE"

        }



# ==========================================================
# SIGNAL FUSION ENGINE
# Institutional Decision Layer
# ==========================================================

    def fuse_all_signals(

        self,

        trend,

        smart_money,

        opportunity,

        prediction,

        timeframe,

        institutional

    ):

        buy_score = 0

        sell_score = 0

        confirmations = []



        # ======================================
        # Trend Engine
        # ======================================

        if trend.get(

            "direction"

        ) == "UP":

            buy_score += 20

            confirmations.append(

                "TREND_UP"

            )


        elif trend.get(

            "direction"

        ) == "DOWN":

            sell_score += 20

            confirmations.append(

                "TREND_DOWN"

            )



        # ======================================
        # Smart Money
        # ======================================

        if smart_money.get(

            "bullish"

        ):

            buy_score += 20

            confirmations.append(

                "SMART_MONEY_BULLISH"

            )


        if smart_money.get(

            "bearish"

        ):

            sell_score += 20

            confirmations.append(

                "SMART_MONEY_BEARISH"

            )



        # ======================================
        # Opportunity Engine
        # ======================================

        opportunity_signal = opportunity.get(

            "signal"

        )


        if opportunity_signal == "BUY":

            buy_score += 20

            confirmations.append(

                "OPPORTUNITY_BUY"

            )


        elif opportunity_signal == "SELL":

            sell_score += 20

            confirmations.append(

                "OPPORTUNITY_SELL"

            )



        # ======================================
        # Prediction AI
        # ======================================

        prediction_signal = prediction.get(

            "signal"

        )


        if prediction_signal == "BUY":

            buy_score += 15

            confirmations.append(

                "AI_PREDICTION_BUY"

            )


        elif prediction_signal == "SELL":

            sell_score += 15

            confirmations.append(

                "AI_PREDICTION_SELL"

            )



        # ======================================
        # Multi Timeframe Agreement
        # ======================================

        agreement = timeframe.get(

            "agreement",

            0

        )


        if agreement >= 70:

            if timeframe.get(

                "signal"

            ) == "BUY":

                buy_score += 15


            elif timeframe.get(

                "signal"

            ) == "SELL":

                sell_score += 15



            confirmations.append(

                "MULTI_TIMEFRAME_CONFIRMATION"

            )



        # ======================================
        # Institutional Filter
        # ======================================

        if institutional.get(

            "accepted"

        ):

            buy_score += 10

            sell_score += 10

            confirmations.append(

                "INSTITUTIONAL_CONFIRMATION"

            )



        # ======================================
        # Final Direction
        # ======================================

        signal = "WAIT"


        if buy_score > sell_score:

            signal = "BUY"


        elif sell_score > buy_score:

            signal = "SELL"



        confidence = self.calculate_confidence(

            buy_score,

            sell_score,

            len(confirmations)

        )



        return {

            "signal": signal,

            "buy_score": buy_score,

            "sell_score": sell_score,

            "confidence": confidence,

            "confirmations": confirmations,

            "confirmation_count": len(confirmations)

        }



# ==========================================================
# SIGNAL QUALITY GRADE
# ==========================================================

    def grade_signal(

        self,

        confidence,

        confirmations,

        risk_level

    ):

        grade = "D"


        if (

            confidence >= 90

            and

            confirmations >= 8

            and

            risk_level == "LOW"

        ):

            grade = "A+"



        elif (

            confidence >= 80

            and

            confirmations >= 6

        ):

            grade = "A"



        elif (

            confidence >= 70

            and

            confirmations >= 4

        ):

            grade = "B"



        elif confidence >= 60:

            grade = "C"



        return {

            "grade": grade,

            "tradeable":

                grade in ["A+", "A", "B"]

        }



# ==========================================================
# SIGNAL MEMORY UPDATE
# ==========================================================

    def update_signal_memory(

        self,

        symbol,

        result

    ):

        self.last_signal = {

            "symbol": symbol,

            "signal": result.get(

                "signal"

            ),

            "confidence": result.get(

                "confidence"

            ),

            "time":

                datetime.utcnow().isoformat()

        }


        self.analysis_count += 1


        return self.last_signal



# ==========================================================
# PRODUCTION SIGNAL OUTPUT FORMATTER
# ==========================================================

    def build_signal_response(

        self,

        symbol,

        market,

        timeframe,

        fusion_result,

        risk_result,

        regime,

        explanation

    ):

        signal = fusion_result.get(

            "signal",

            "WAIT"

        )


        confidence = fusion_result.get(

            "confidence",

            0

        )


        confirmations = fusion_result.get(

            "confirmation_count",

            0

        )


        risk_level = risk_result.get(

            "risk_level",

            "UNKNOWN"

        )



        grade = self.grade_signal(

            confidence,

            confirmations,

            risk_level

        )



        return {

            # ==========================
            # Market
            # ==========================

            "symbol":

                symbol,


            "market":

                market,


            "timeframe":

                timeframe,



            # ==========================
            # Final Signal
            # ==========================

            "signal":

                signal,


            "confidence":

                confidence,


            "grade":

                grade.get(

                    "grade"

                ),


            "tradeable":

                grade.get(

                    "tradeable"

                ),



            # ==========================
            # Scores
            # ==========================

            "buy_score":

                fusion_result.get(

                    "buy_score",

                    0

                ),


            "sell_score":

                fusion_result.get(

                    "sell_score",

                    0

                ),



            # ==========================
            # Confirmation
            # ==========================

            "confirmations":

                fusion_result.get(

                    "confirmations",

                    []

                ),


            "confirmation_count":

                confirmations,



            # ==========================
            # Risk
            # ==========================

            "risk":

                risk_result,


            # ==========================
            # Market State
            # ==========================

            "market_regime":

                regime,



            # ==========================
            # Explanation
            # ==========================

            "explanation":

                explanation,


            # ==========================
            # Engine
            # ==========================

            "engine":

                {

                    "version":

                        self.version,


                    "status":

                        "ACTIVE"

                }

        }



# ==========================================================
# SAFE ANALYSIS WRAPPER
# Production Protection Layer
# ==========================================================

    def safe_analyze(

        self,

        symbol,

        market="crypto",

        timeframe="15m"

    ):

        try:

            result = self.analyze(

                symbol,

                market,

                timeframe

            )


            if not result:

                return {

                    "signal":

                        "WAIT",

                    "confidence":

                        0,

                    "error":

                        "EMPTY_RESPONSE"

                }



            self.update_signal_memory(

                symbol,

                result

            )


            return result



        except Exception as e:


            self.error_count += 1


            return {

                "signal":

                    "WAIT",


                "confidence":

                    0,


                "error":

                    str(e),


                "engine_version":

                    self.version

            }



# ==========================================================
# ENGINE STATUS REPORT
# ==========================================================

    def get_engine_status(

        self

    ):


        return {

            "version":

                self.version,


            "active":

                self.active,


            "analyses":

                self.analysis_count,


            "errors":

                self.error_count,


            "last_signal":

                self.last_signal

                }
