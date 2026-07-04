from app.ai.market_analyzer import MarketAnalyzer


class PredictionEngine:

    def __init__(self):

        self.market = MarketAnalyzer()

    def predict(

        self,

        symbol="BTCUSDT",

        interval="1h"

    ):

        market = self.market.analyze(

            symbol,

            interval

        )

        bullish = False

        bearish = False

        confidence = 50

        trend = market["trend_strength"]

        rsi = market["rsi"]

        volume = market["volume_power"]

        ema = market["ema"]

        price = market["price"]

        score = 0

        if trend > 0:
            score += 20

        if price > ema:
            score += 20

        if volume > 1:
            score += 20

        if rsi < 35:
            score += 20

        if rsi > 65:
            score -= 20

        confidence = min(

            max(

                score,

                0

            ),

            100

        )

        if confidence >= 60:

            bullish = True

        if (

            trend < 0

            and price < ema

            and rsi > 65

        ):

            bearish = True

        prediction = "WAIT"

        if bullish:
            prediction = "BUY"

        if bearish:
            prediction = "SELL"

        return {

            "prediction": prediction,

            "confidence": confidence,

            "bullish": bullish,

            "bearish": bearish,

            "trend": trend,

            "rsi": rsi,

            "ema": ema,

            "price": price,

            "volume": volume

        }
