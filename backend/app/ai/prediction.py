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


        candles = market_data.get(
            "candles",
            []
        )


        opportunity = self.opportunity.analyze(

            symbol=symbol,

            candles=candles

        )


        prediction = opportunity.get(
            "signal",
            "WAIT"
        )


        confidence = opportunity.get(
            "confidence",
            0
        )


        bullish = False

        bearish = False



        if prediction == "BUY":

            bullish = True



        elif prediction == "SELL":

            bearish = True



        return {

            "prediction": prediction,


            "confidence": confidence,


            "bullish": bullish,


            "bearish": bearish,


            "trend": market_data.get(
                "trend_strength",
                0
            ),


            "rsi": market_data.get(
                "rsi",
                0
            ),


            "ema": market_data.get(
                "ema",
                0
            ),


            "price": market_data.get(
                "price",
                0
            ),


            "volume": market_data.get(
                "volume_power",
                0
            ),


            "opportunity": opportunity

        }
