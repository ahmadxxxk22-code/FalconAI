from datetime import datetime

from app.ai.market_analyzer import MarketAnalyzer
from app.ai.patterns import PatternAnalyzer
from app.ai.smart_money import SmartMoneyAnalyzer
from app.ai.prediction import PredictionEngine
from app.ai.risk_manager import RiskManager
from app.ai.news_ai import NewsAnalyzer
from app.ai.fibonacci import FibonacciAnalyzer


class SignalEngine:

    def __init__(self):

        self.market = MarketAnalyzer()

        self.patterns = PatternAnalyzer()

        self.smart_money = SmartMoneyAnalyzer()

        self.prediction = PredictionEngine()

        self.risk = RiskManager()

        self.news = NewsAnalyzer()

        self.fibonacci = FibonacciAnalyzer()

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

        news = self.news.analyze(symbol)

        fibo = self.fibonacci.analyze(

            symbol,

            interval

        )

        confidence = self.calculate_confidence(

            market,

            patterns,

            smart,

            prediction,

            news,

            fibo

        )

        direction = self.choose_direction(

            market,

            prediction,

            smart

        )

        risk = self.risk.calculate(

            direction=direction,

            price=market["price"],

            confidence=confidence

        )

        return {

            "symbol": symbol,

            "interval": interval,

            "direction": direction,

            "confidence": confidence,

            "price": market["price"],

            "market": market,

            "patterns": patterns,

            "smart_money": smart,

            "prediction": prediction,

            "news": news,

            "fibonacci": fibo,

            "risk": risk,

            "created_at": datetime.utcnow().isoformat()

        }

    def calculate_confidence(

        self,

        market,

        patterns,

        smart,

        prediction,

        news,

        fibo

    ):

        score = 0

        if market["bullish"]:

            score += 20

        if prediction["bullish"]:

            score += 20

        if smart["bullish"]:

            score += 20

        if patterns["bullish"]:

            score += 15

        if news["bullish"]:

            score += 15

        if fibo["bullish"]:

            score += 10

        return min(score, 100)

    def choose_direction(

        self,

        market,

        prediction,

        smart

    ):

        bullish = 0

        bearish = 0

        if market["bullish"]:
            bullish += 1

        if prediction["bullish"]:
            bullish += 1

        if smart["bullish"]:
            bullish += 1

        if market["bearish"]:
            bearish += 1

        if prediction["bearish"]:
            bearish += 1

        if smart["bearish"]:
            bearish += 1

        if bullish >= 2:
            return "BUY"

        if bearish >= 2:
            return "SELL"

        return "WAIT"
