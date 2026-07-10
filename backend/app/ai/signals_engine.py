from datetime import datetime

from app.ai.market_analyzer import MarketAnalyzer
from app.ai.trend_engine import TrendEngine
from app.ai.patterns import PatternAnalyzer
from app.ai.smart_money import SmartMoneyAnalyzer
from app.ai.prediction import PredictionEngine
from app.ai.risk_manager import RiskManager
from app.ai.news_ai import NewsAnalyzer
from app.ai.fibonacci import FibonacciAnalyzer


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


    def analyze(
        self,
        symbol="BTCUSDT",
        interval="1h",
        market="crypto"
    ):

        market_data = self.market.analyze(
            symbol,
            interval
        )

        trend = self.trend.analyze(
            symbol=symbol,
            interval=interval,
            market=market
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
            trend,
            patterns,
            smart,
            prediction,
            news,
            fibo
        )


        direction = self.choose_direction(
            trend,
            prediction,
            smart,
            patterns,
            fibo
        )


        risk = self.risk.calculate(
            direction=direction,
            price=market_data["price"],
            confidence=confidence
        )


        return {

            "symbol": symbol,
            "interval": interval,
            "direction": direction,
            "confidence": confidence,
            "price": market_data["price"],

            "trend": trend,
            "market": market_data,
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
        trend,
        patterns,
        smart,
        prediction,
        news,
        fibo
    ):

        score = 0


        if trend.get("score", 0) > 0:
            score += 25


        if prediction.get("bullish", False):
            score += 20


        if smart.get("bullish", False):
            score += 20


        if patterns.get("bullish", False):
            score += 15


        if news.get("bullish", False):
            score += 10


        if fibo.get("bullish", False):
            score += 10


        return min(score, 100)



    def choose_direction(
        self,
        trend,
        prediction,
        smart,
        patterns,
        fibo
    ):

        bullish = 0
        bearish = 0


        score = trend.get("score",0)


        if score > 0:
            bullish += 1

        elif score < 0:
            bearish += 1



        for item in [
            prediction,
            smart,
            patterns,
            fibo
        ]:

            if item.get("bullish",False):
                bullish += 1

            if item.get("bearish",False):
                bearish += 1



        if bullish >= 3:
            return "BUY"


        if bearish >= 3:
            return "SELL"


<<<<<<< HEAD
        return "WAIT"
=======
        return "WAIT"
>>>>>>> 3438409 (Fix SignalEngine and TrendEngine integration)
