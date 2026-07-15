from app.ai.opportunity.trend_engine import TrendEngine
from app.ai.opportunity.volume_engine import VolumeEngine
from app.ai.opportunity.liquidity_engine import LiquidityEngine
from app.ai.opportunity.order_blocks import OrderBlocksEngine
from app.ai.opportunity.support_resistance import SupportResistanceEngine
from app.ai.opportunity.candles_ai import CandlesAI
from app.ai.opportunity.historical_learning import HistoricalLearning


class OpportunityEngine:

    def __init__(self):

        self.trend = TrendEngine()

        self.volume = VolumeEngine()

        self.liquidity = LiquidityEngine()

        self.order_blocks = OrderBlocksEngine()

        self.support = SupportResistanceEngine()

        self.candles = CandlesAI()

        self.history = HistoricalLearning()

    def analyze(
        self,
        symbol,
        candles
    ):

        trend = self.trend.analyze(symbol)

        volume = self.volume.analyze(candles)

        liquidity = self.liquidity.analyze(candles)

        order_blocks = self.order_blocks.analyze(candles)

        candle_patterns = self.candles.analyze(candles)

        history = self.history.analyze(candles)

        highs = [c["high"] for c in candles]

        lows = [c["low"] for c in candles]

        closes = [c["close"] for c in candles]

        support = self.support.analyze(
            highs,
            lows,
            closes
        )

        score = 0

        reasons = []


        if trend.get("signal") == "BUY":

            score += 25

            reasons.append(
                "Trend BUY"
            )


        elif trend.get("signal") == "SELL":

            score -= 25

            reasons.append(
                "Trend SELL"
            )


        score += volume.get(
            "score",
            0
        )


        score += liquidity.get(
            "score",
            0
        )


        score += candle_patterns.get(
            "confidence",
            0
        )


        if order_blocks.get(
            "bullish_blocks"
        ):

            score += 15

            reasons.append(
                "Bullish Order Block"
            )


        if order_blocks.get(
            "bearish_blocks"
        ):

            score -= 15

            reasons.append(
                "Bearish Order Block"
            )


        if history.get(
            "bullish",
            False
        ):

            score += 20

            reasons.append(
                "Historical Bullish"
            )


        if history.get(
            "bearish",
            False
        ):

            score -= 20

            reasons.append(
                "Historical Bearish"
            )


        if score >= 40:

            signal = "BUY"

        elif score <= -40:

            signal = "SELL"

        else:

            signal = "WAIT"

        confidence = min(
            abs(score),
            100
        )

        return {

            "signal": signal,

            "confidence": confidence,

            "score": score,

            "reasons": reasons,

            "trend": trend,

            "volume": volume,

            "liquidity": liquidity,

            "order_blocks": order_blocks,

            "candles": candle_patterns,

            "history": history,

            "support": support

        }
