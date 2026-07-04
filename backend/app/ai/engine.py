from app.ai.market_analyzer import MarketAnalyzer
from app.ai.patterns import PatternAnalyzer
from app.ai.smart_money import SmartMoneyAnalyzer
from app.ai.prediction import PredictionEngine
from app.ai.news_ai import NewsAnalyzer
from app.ai.fibonacci import FibonacciAnalyzer
from app.ai.risk_manager import RiskManager
from app.ai.learning import LearningEngine
from app.ai.assistant import FalconAssistant


class AIEngine:

    def __init__(self):

        self.market = MarketAnalyzer()

        self.patterns = PatternAnalyzer()

        self.smart_money = SmartMoneyAnalyzer()

        self.prediction = PredictionEngine()

        self.news = NewsAnalyzer()

        self.fibonacci = FibonacciAnalyzer()

        self.risk = RiskManager()

        self.learning = LearningEngine()

        self.assistant = FalconAssistant()

    def analyze(
        self,
        symbol="BTCUSDT",
        interval="1h"
    ):

        market = self.market.analyze(
            symbol,
            interval
        )

        patterns = self.patterns.analyze(
            symbol,
            interval
        )

        smart = self.smart_money.analyze(
            symbol,
            interval
        )

        prediction = self.prediction.predict(
            symbol,
            interval
        )

        news = self.news.analyze(
            symbol
        )

        fibonacci = self.fibonacci.analyze(
            symbol,
            interval
        )

        confidence = self.calculate_confidence(

            market,

            prediction,

            patterns,

            smart,

            news,

            fibonacci

        )

        direction = self.direction(

            market,

            prediction,

            smart

        )

        risk = self.risk.calculate(

            direction=direction,

            price=market["price"],

            confidence=confidence

        )

        analysis = {

            "symbol": symbol,

            "interval": interval,

            "direction": direction,

            "confidence": confidence,

            "market": market,

            "patterns": patterns,

            "smart_money": smart,

            "prediction": prediction,

            "news": news,

            "fibonacci": fibonacci,

            "risk": risk

        }

        return {

            "analysis": analysis,

            "assistant": self.assistant.explain(

                analysis

            )

        }

    def calculate_confidence(

        self,

        market,

        prediction,

        patterns,

        smart,

        news,

        fibonacci

    ):

        score = 0

        if market["bullish"]:
            score += 20

        if prediction["bullish"]:
            score += 20

        if patterns["bullish"]:
            score += 15

        if smart["bullish"]:
            score += 20

        if news["bullish"]:
            score += 15

        if fibonacci["bullish"]:
            score += 10

        return min(score, 100)

    def direction(

        self,

        market,

        prediction,

        smart

    ):

        buy = 0

        sell = 0

        if market["bullish"]:
            buy += 1

        if prediction["bullish"]:
            buy += 1

        if smart["bullish"]:
            buy += 1

        if market["bearish"]:
            sell += 1

        if prediction["bearish"]:
            sell += 1

        if smart["bearish"]:
            sell += 1

        if buy >= 2:
            return "BUY"

        if sell >= 2:
            return "SELL"

        return "WAIT"
