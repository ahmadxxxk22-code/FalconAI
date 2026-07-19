from typing import Dict, Any

from app.ai.opportunity.trend_engine import TrendEngine
from app.ai.opportunity.volume_engine import VolumeEngine
from app.ai.opportunity.liquidity_engine import LiquidityEngine
from app.ai.opportunity.order_blocks import OrderBlocksEngine
from app.ai.opportunity.support_resistance import SupportResistanceEngine
from app.ai.opportunity.candles_ai import CandlesAI
from app.ai.opportunity.historical_learning import HistoricalLearning
from app.ai.smart_money import SmartMoneyAnalyzer


class OpportunityEngine:

    def __init__(self):

        self.trend = TrendEngine()
        self.volume = VolumeEngine()
        self.liquidity = LiquidityEngine()
        self.order_blocks = OrderBlocksEngine()
        self.support = SupportResistanceEngine()
        self.candles = CandlesAI()
        self.history = HistoricalLearning()

        self.smart_money = SmartMoneyAnalyzer()

        self.weights = {
            "smart_money": 25,
            "trend": 18,
            "volume": 10,
            "liquidity": 12,
            "order_blocks": 12,
            "candles": 8,
            "history": 8,
            "support_resistance": 7
        }

        self.minimum_score = 45
        self.maximum_score = 100

        self.minimum_confidence = 60
        self.minimum_confirmations = 4

        self.reject_conflicting_signals = True

        self.bos_bonus = 6
        self.choch_bonus = 8
        self.displacement_bonus = 5
        self.orderblock_bonus = 5
        self.discount_bonus = 4
        self.premium_bonus = 4

        self.conflict_penalty = 12
        self.weak_volume_penalty = 8

    # ==================================================
    # MAIN OPPORTUNITY ANALYSIS
    # ==================================================

    def analyze(
        self,
        symbol: str,
        candles: list,
        interval: str = "1h",
        market: str = "crypto"
    ) -> Dict[str, Any]:

        if not candles or len(candles) < 120:
            return self.empty_result()

        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]
        closes = [c["close"] for c in candles]
        current_price = closes[-1]

        trend = self.trend.analyze(symbol)
        volume = self.volume.analyze(candles)
        liquidity = self.liquidity.analyze(candles)
        order_blocks = self.order_blocks.analyze(candles)
        candle_patterns = self.candles.analyze(candles)
        history = self.history.analyze(candles)

        support = self.support.analyze(
            highs,
            lows,
            closes
        )

        smart_money = self.smart_money.analyze(
            symbol=symbol,
            interval=interval,
            market=market
        )

        bullish_score = 0
        bearish_score = 0
        confirmations = 0
        reasons = []



        # ==================================================
        # SMART MONEY
        # ==================================================

        sm_score = smart_money.get("smart_money_score", 0)

        if smart_money.get("bullish", False):

            bullish_score += min(
                sm_score,
                self.weights["smart_money"]
            )

            confirmations += 1

            reasons.append("Smart Money Bullish")

        elif smart_money.get("bearish", False):

            bearish_score += min(
                sm_score,
                self.weights["smart_money"]
            )

            confirmations += 1

            reasons.append("Smart Money Bearish")

        if smart_money.get("bos", False):

            confirmations += 1

            if smart_money.get("bos_direction") == "BULLISH":

                bullish_score += self.bos_bonus
                reasons.append("Bullish BOS")

            elif smart_money.get("bos_direction") == "BEARISH":

                bearish_score += self.bos_bonus
                reasons.append("Bearish BOS")

        if smart_money.get("choch", False):

            confirmations += 1

            if smart_money.get("choch_direction") == "BULLISH":

                bullish_score += self.choch_bonus
                reasons.append("Bullish CHOCH")

            elif smart_money.get("choch_direction") == "BEARISH":

                bearish_score += self.choch_bonus
                reasons.append("Bearish CHOCH")

        if smart_money.get("internal_bos", False):

            confirmations += 1

            if smart_money.get("bullish"):

                bullish_score += 4

            elif smart_money.get("bearish"):

                bearish_score += 4

            reasons.append("Internal BOS")

        if smart_money.get("liquidity_sweep", False):

            confirmations += 1

            if smart_money.get("liquidity_side") == "SELL_SIDE":

                bullish_score += 6
                reasons.append("Sell Side Sweep")

            elif smart_money.get("liquidity_side") == "BUY_SIDE":

                bearish_score += 6
                reasons.append("Buy Side Sweep")

        if smart_money.get("displacement", False):

            confirmations += 1

            if smart_money.get("bullish"):

                bullish_score += self.displacement_bonus

            elif smart_money.get("bearish"):

                bearish_score += self.displacement_bonus

            reasons.append("Strong Displacement")

        if smart_money.get("order_block"):

            confirmations += 1

            if smart_money.get("bullish"):

                bullish_score += self.orderblock_bonus

            elif smart_money.get("bearish"):

                bearish_score += self.orderblock_bonus

            reasons.append("Institutional Order Block")

        if smart_money.get("breaker_block"):

            confirmations += 1

            if smart_money.get("bullish"):

                bullish_score += 4

            elif smart_money.get("bearish"):

                bearish_score += 4

            reasons.append("Breaker Block")

        if smart_money.get("mitigation_block"):

            confirmations += 1

            if smart_money.get("bullish"):

                bullish_score += 3

            elif smart_money.get("bearish"):

                bearish_score += 3

            reasons.append("Mitigation Block")

        if smart_money.get("premium_discount") == "DISCOUNT":

            bullish_score += self.discount_bonus
            reasons.append("Discount Zone")

        elif smart_money.get("premium_discount") == "PREMIUM":

            bearish_score += self.premium_bonus
            reasons.append("Premium Zone")



        # ==================================================
        # TREND ENGINE
        # ==================================================

        trend_signal = trend.get("signal", "WAIT")

        if trend_signal == "BUY":

            bullish_score += self.weights["trend"]
            confirmations += 1
            reasons.append("Trend Bullish")

        elif trend_signal == "SELL":

            bearish_score += self.weights["trend"]
            confirmations += 1
            reasons.append("Trend Bearish")

        # ==================================================
        # VOLUME ENGINE
        # ==================================================

        volume_score = volume.get("score", 0)

        if volume_score > 0:

            bullish_score += min(
                volume_score,
                self.weights["volume"]
            )

            confirmations += 1
            reasons.append("Bullish Volume")

        elif volume_score < 0:

            bearish_score += min(
                abs(volume_score),
                self.weights["volume"]
            )

            confirmations += 1
            reasons.append("Bearish Volume")

        else:

            bullish_score -= self.weak_volume_penalty / 2
            bearish_score -= self.weak_volume_penalty / 2

            reasons.append("Weak Volume")

        # ==================================================
        # LIQUIDITY ENGINE
        # ==================================================

        liquidity_score = liquidity.get("score", 0)

        if liquidity_score > 0:

            bullish_score += min(
                liquidity_score,
                self.weights["liquidity"]
            )

            confirmations += 1
            reasons.append("Liquidity Supports Buyers")

        elif liquidity_score < 0:

            bearish_score += min(
                abs(liquidity_score),
                self.weights["liquidity"]
            )

            confirmations += 1
            reasons.append("Liquidity Supports Sellers")

        # ==================================================
        # ORDER BLOCK ENGINE
        # ==================================================

        if order_blocks.get("bullish_blocks", False):

            bullish_score += self.weights["order_blocks"]
            confirmations += 1
            reasons.append("Bullish Order Block")

        if order_blocks.get("bearish_blocks", False):

            bearish_score += self.weights["order_blocks"]
            confirmations += 1
            reasons.append("Bearish Order Block")

        # ==================================================
        # CANDLE AI
        # ==================================================

        candle_confidence = candle_patterns.get(
            "confidence",
            0
        )

        if candle_patterns.get("bullish", False):

            bullish_score += min(
                candle_confidence,
                self.weights["candles"]
            )

            confirmations += 1
            reasons.append("Bullish Candle Pattern")

        elif candle_patterns.get("bearish", False):

            bearish_score += min(
                candle_confidence,
                self.weights["candles"]
            )

            confirmations += 1
            reasons.append("Bearish Candle Pattern")

        # ==================================================
        # HISTORICAL LEARNING
        # ==================================================

        history_confidence = history.get(
            "confidence",
            0
        )

        if history.get("bullish", False):

            bullish_score += min(
                history_confidence,
                self.weights["history"]
            )

            confirmations += 1
            reasons.append("Historical Bullish Match")

        elif history.get("bearish", False):

            bearish_score += min(
                history_confidence,
                self.weights["history"]
            )

            confirmations += 1
            reasons.append("Historical Bearish Match")

        # ==================================================
        # SUPPORT / RESISTANCE
        # ==================================================

        if support.get("support_strength", 0) >= 60:

            bullish_score += self.weights["support_resistance"]
            reasons.append("Strong Support")

        if support.get("resistance_strength", 0) >= 60:

            bearish_score += self.weights["support_resistance"]
            reasons.append("Strong Resistance")



        # ==================================================
        # FINAL SCORE
        # ==================================================

        final_score = bullish_score - bearish_score

        # ==================================================
        # منع الإشارات المتضاربة
        # ==================================================

        if self.reject_conflicting_signals:

            if bullish_score > 0 and bearish_score > 0:

                difference = abs(
                    bullish_score - bearish_score
                )

                if difference <= self.conflict_penalty:

                    reasons.append("Conflicting Signals")

                    return {
                        "signal": "WAIT",
                        "confidence": 0,
                        "score": 0,
                        "bullish_score": bullish_score,
                        "bearish_score": bearish_score,
                        "confirmations": confirmations,
                        "reasons": reasons,
                        "engine": "OpportunityEngine"
                    }

        # ==================================================
        # الحد الأدنى للتأكيدات
        # ==================================================

        if confirmations < self.minimum_confirmations:

            reasons.append(
                f"Not enough confirmations ({confirmations})"
            )

            return {
                "signal": "WAIT",
                "confidence": 0,
                "score": final_score,
                "bullish_score": bullish_score,
                "bearish_score": bearish_score,
                "confirmations": confirmations,
                "reasons": reasons,
                "engine": "OpportunityEngine"
            }

        # ==================================================
        # تحديد الإشارة
        # ==================================================

        signal = "WAIT"

        if bullish_score >= self.minimum_score and bullish_score > bearish_score:
            signal = "BUY"

        elif bearish_score >= self.minimum_score and bearish_score > bullish_score:
            signal = "SELL"

        # ==================================================
        # حساب الثقة
        # ==================================================

        total = bullish_score + bearish_score

        if total > 0:

            confidence = int(
                (max(bullish_score, bearish_score) / total) * 100
            )

        else:

            confidence = 0

        confidence = min(confidence, self.maximum_score)

        if confidence < self.minimum_confidence:

            signal = "WAIT"

            reasons.append(
                "Low confidence"
                      )



        # ==================================================
        # QUALITY FILTER
        # ==================================================

        quality_score = 0

        if smart_money.get("bos"):
            quality_score += 2

        if smart_money.get("choch"):
            quality_score += 2

        if smart_money.get("liquidity_sweep"):
            quality_score += 2

        if smart_money.get("order_block"):
            quality_score += 2

        if smart_money.get("displacement"):
            quality_score += 1

        if trend.get("signal") == signal:
            quality_score += 2

        if volume.get("score", 0) > 0 and signal == "BUY":
            quality_score += 1

        if volume.get("score", 0) < 0 and signal == "SELL":
            quality_score += 1

        if candle_patterns.get("confidence", 0) >= 70:
            quality_score += 1

        if history.get("confidence", 0) >= 70:
            quality_score += 1

        if signal == "BUY":

            if support.get("support_strength", 0) >= 70:
                quality_score += 1

        elif signal == "SELL":

            if support.get("resistance_strength", 0) >= 70:
                quality_score += 1

        # ==========================================
        # FINAL QUALITY
        # ==========================================

        if quality_score >= 12:
            quality = "A+"

        elif quality_score >= 10:
            quality = "A"

        elif quality_score >= 8:
            quality = "B"

        elif quality_score >= 6:
            quality = "C"

        else:
            quality = "D"

        if quality in ["C", "D"]:

            signal = "WAIT"

            reasons.append(
                "Signal rejected because quality is too low"
            )

        # ==================================================
        # RISK / REWARD
        # ==================================================

        risk_reward = 0.0
        stop_loss = None
        take_profit = None

        if signal == "BUY" and support.get("nearest_support"):

            stop_loss = support["nearest_support"]["price"]

            risk = current_price - stop_loss

            if risk > 0:

                take_profit = current_price + (risk * 3)

                reward = take_profit - current_price

                risk_reward = reward / risk

        elif signal == "SELL" and support.get("nearest_resistance"):

            stop_loss = support["nearest_resistance"]["price"]

            risk = stop_loss - current_price

            if risk > 0:

                take_profit = current_price - (risk * 3)

                reward = current_price - take_profit

                risk_reward = reward / risk

        if signal != "WAIT" and risk_reward < 2:

            signal = "WAIT"

            reasons.append(
                f"Risk Reward too low ({risk_reward:.2f})"
            )

        return {

            "signal": signal,

            "confidence": confidence,

            "quality": quality,

            "quality_score": quality_score,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "risk_reward": round(risk_reward, 2),

            "score": final_score,

            "bullish_score": bullish_score,

            "bearish_score": bearish_score,

            "confirmations": confirmations,

            "reasons": reasons,

            "trend": trend,

            "volume": volume,

            "liquidity": liquidity,

            "order_blocks": order_blocks,

            "candles": candle_patterns,

            "history": history,

            "support": support,

            "smart_money": smart_money,

            "engine": "OpportunityEngine",

            "status": "completed"

        }

    def empty_result(self):

        return {

            "signal": "WAIT",

            "confidence": 0,

            "quality": "D",

            "quality_score": 0,

            "score": 0,

            "bullish_score": 0,

            "bearish_score": 0,

            "confirmations": 0,

            "stop_loss": None,
            "take_profit": None,
            "risk_reward": 0.0,

            "trend": {},
            "volume": {},
            "liquidity": {},
            "order_blocks": {},
            "candles": {},
            "history": {},
            "support": {},
            "smart_money": {},
            
            "reasons": [

                "Not enough candles"

            ],

            "engine": "OpportunityEngine",

            "status": "empty"

            }
