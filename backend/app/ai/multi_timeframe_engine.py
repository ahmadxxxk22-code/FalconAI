from app.ai.trend_engine import TrendEngine


class MultiTimeframeEngine:

    def __init__(self):

        self.trend = TrendEngine()

        self.timeframes = [

            "15m",

            "1h",

            "4h",

            "1d"

        ]

    def analyze(

        self,

        symbol="BTCUSDT",

        market="crypto"

    ):

        results = []

        total_score = 0

        for interval in self.timeframes:

            result = self.trend.analyze(

                symbol=symbol,

                interval=interval,

                market=market

            )

            results.append(result)

            total_score += result["score"]

        average_score = total_score / len(results)

        if average_score >= 70:

            signal = "STRONG_BUY"

        elif average_score >= 35:

            signal = "BUY"

        elif average_score <= -70:

            signal = "STRONG_SELL"

        elif average_score <= -35:

            signal = "SELL"

        else:

            signal = "WAIT"

        confidence = min(

            100,

            int(abs(average_score))

        )

        return {

            "symbol": symbol,

            "market": market,

            "signal": signal,

            "confidence": confidence,

            "average_score": average_score,

            "timeframes": results

        }
