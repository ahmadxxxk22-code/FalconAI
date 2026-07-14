from app.ai.market_analyzer import MarketAnalyzer


class PredictionEngine:

    def __init__(self):
        self.market = MarketAnalyzer()

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

        bullish = False
        bearish = False

        trend = market_data["trend_strength"]
        rsi = market_data["rsi"]
        volume = market_data["volume_power"]
        ema = market_data["ema"]
        price = market_data["price"]

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

        elif bearish:
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
