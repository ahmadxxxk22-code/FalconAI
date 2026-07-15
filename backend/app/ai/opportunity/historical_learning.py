import statistics


class HistoricalLearning:

    def analyze(self, candles):

        if len(candles) < 300:

            return {

                "trend_probability": 50,

                "bullish": False,

                "bearish": False,

                "volatility": 0,

                "average_move": 0,

                "confidence": 0

            }

        closes = [

            candle["close"]

            for candle in candles

        ]

        returns = []

        for i in range(1, len(closes)):

            returns.append(

                (
                    closes[i] -

                    closes[i - 1]

                )

                /

                closes[i - 1]

            )

        average_move = statistics.mean(
            returns
        )

        volatility = statistics.stdev(
            returns
        )

        probability = 50

        bullish = False
        bearish = False

        if average_move > 0:

            probability += 20

            bullish = True

        else:

            probability -= 20

            bearish = True

        if volatility > 0.02:

            probability += 10

        probability = max(
            0,
            min(
                probability,
                100
            )
        )

        return {

            "trend_probability": probability,

            "bullish": bullish,

            "bearish": bearish,

            "volatility": round(
                volatility,
                4
            ),

            "average_move": round(
                average_move,
                4
            ),

            "confidence": probability

        }
