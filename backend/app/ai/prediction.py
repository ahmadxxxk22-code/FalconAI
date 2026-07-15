from app.ai.market_analyzer import MarketAnalyzer
from app.ai.opportunity.opportunity_engine import OpportunityEngine


class PredictionEngine:

    def __init__(self):

        self.market = MarketAnalyzer()

        self.opportunity = OpportunityEngine()

    def predict(
        self,
        symbol="BTCUSDT",
        interval="1h",
        market="crypto"
    ):

        market_data = self.market.analyze(
            symbol=symbol,
            interval=interval,
            market=market
        )

        opportunity = self.opportunity.analyze(

            symbol=symbol,

            candles=market_data["candles"]

        )

        prediction = opportunity["signal"]

        confidence = opportunity["confidence"]

        bullish = prediction == "BUY"

        bearish = prediction == "SELL"

        return {

            "prediction": prediction,

            "confidence": confidence,

            "bullish": bullish,

            "bearish": bearish,

            "trend": market_data["trend_strength"],

            "rsi": market_data["rsi"],

            "ema": market_data["ema"],

            "price": market_data["price"],

            "volume": market_data["volume_power"],

            "opportunity": opportunity

        }
