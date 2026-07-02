from app.ai.market_analyzer import MarketAnalyzer
from app.ai.patterns import PatternAnalyzer
from app.ai.smart_money import SmartMoneyAnalyzer
from app.ai.fibonacci import FibonacciAnalyzer
from app.ai.prediction import PredictionEngine
from app.ai.news_ai import NewsAnalyzer
from app.ai.risk_manager import RiskManager


class AIEngine:

    def __init__(self):

        self.market = MarketAnalyzer()
        self.patterns = PatternAnalyzer()
        self.smart_money = SmartMoneyAnalyzer()
        self.fibonacci = FibonacciAnalyzer()
        self.prediction = PredictionEngine()
        self.news = NewsAnalyzer()
        self.risk = RiskManager()

    def analyze(self, symbol, timeframe):

        market = self.market.analyze(symbol, timeframe)

        patterns = self.patterns.detect(symbol, timeframe)

        smart_money = self.smart_money.analyze(symbol, timeframe)

        fibonacci = self.fibonacci.analyze(symbol, timeframe)

        prediction = self.prediction.predict(symbol, timeframe)

        news = self.news.analyze(symbol)

        risk = self.risk.calculate(symbol, timeframe)

        score = 0
        reasons = []

        if market["trend"] == "BUY":
            score += 20
            reasons.append("Bullish Trend")

        if patterns["signal"] == "BUY":
            score += 20
            reasons.append(patterns["pattern"])

        if smart_money["signal"] == "BUY":
            score += 20
            reasons.append("Smart Money")

        if fibonacci["signal"] == "BUY":
            score += 15
            reasons.append("Fibonacci Support")

        if prediction["signal"] == "BUY":
            score += 15
            reasons.append("AI Prediction")

        if news["impact"] == "POSITIVE":
            score += 10
            reasons.append("Positive News")

        if score >= 70:
            signal = "BUY"

        elif score <= 30:
            signal = "SELL"

        else:
            signal = "WAIT"

        return {

            "symbol": symbol,

            "timeframe": timeframe,

            "signal": signal,

            "confidence": score,

            "reasons": reasons,

            "risk": risk

        }
