from app.ai.market_analyzer import MarketAnalyzer


class TrendEngine:

    def __init__(self):
        self.market = MarketAnalyzer()

    def analyze(self, symbol, timeframe="1h"):

        data = self.market.analyze(symbol, timeframe)

        score = 0
        reasons = []

        # الاتجاه العام
        if data["trend"] == "STRONG_BULL":
            score += 30
            reasons.append("Strong Bull Trend")

        elif data["trend"] == "BULL":
            score += 20
            reasons.append("Bull Trend")

        elif data["trend"] == "STRONG_BEAR":
            score -= 30
            reasons.append("Strong Bear Trend")

        elif data["trend"] == "BEAR":
            score -= 20
            reasons.append("Bear Trend")

        # RSI
        if data["rsi"] < 30:
            score += 15
            reasons.append("Oversold RSI")

        elif data["rsi"] > 70:
            score -= 15
            reasons.append("Overbought RSI")

        # EMA
        if data["last_price"] > data["ema"]:
            score += 10
            reasons.append("Price Above EMA")

        else:
            score -= 10
            reasons.append("Price Below EMA")

        # Volume
        if data["current_volume"] > data["avg_volume"]:
            score += 10
            reasons.append("High Volume")

        confidence = min(abs(score), 100)

        if score >= 30:
            signal = "BUY"

        elif score <= -30:
            signal = "SELL"

        else:
            signal = "WAIT"

        return {

            "signal": signal,

            "score": score,

            "confidence": confidence,

            "reasons": reasons

        }
