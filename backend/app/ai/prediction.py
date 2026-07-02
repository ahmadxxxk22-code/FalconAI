from app.ai.market_analyzer import MarketAnalyzer
from app.ai.patterns import PatternAnalyzer
from app.ai.smart_money import SmartMoneyAnalyzer


class PredictionEngine:

    def __init__(self):

        self.market = MarketAnalyzer()

        self.patterns = PatternAnalyzer()

        self.smart = SmartMoneyAnalyzer()

    def predict(self, symbol="BTCUSDT", interval="1h"):

        market = self.market.analyze(
            symbol,
            interval
        )

        patterns = self.patterns.detect(
            symbol,
            interval
        )

        smart = self.smart.analyze(
            symbol,
            interval
        )

        score = 0

        reasons = []

        # --------------------------
        # Market Trend
        # --------------------------

        if market["bullish"]:

            score += 35

            reasons.append(
                "Bullish Trend"
            )

        if market["bearish"]:

            score -= 35

            reasons.append(
                "Bearish Trend"
            )

        # --------------------------
        # Candlestick Patterns
        # --------------------------

        if patterns["signal"] == "BUY":

            score += 25

            reasons.append(
                patterns["pattern"]
            )

        elif patterns["signal"] == "SELL":

            score -= 25

            reasons.append(
                patterns["pattern"]
            )

        # --------------------------
        # Smart Money
        # --------------------------

        if smart["signal"] == "BUY":

            score += smart["confidence"]

            reasons.append(
                "Institutional Buying"
            )

        elif smart["signal"] == "SELL":

            score -= smart["confidence"]

            reasons.append(
                "Institutional Selling"
            )

        # --------------------------
        # Final Decision
        # --------------------------

        if score >= 60:

            signal = "BUY"

            confidence = min(score, 100)

        elif score <= -60:

            signal = "SELL"

            confidence = min(abs(score), 100)

        else:

            signal = "WAIT"

            confidence = abs(score)

        return {

            "signal": signal,

            "confidence": confidence,

            "score": score,

            "reasons": reasons

        }
