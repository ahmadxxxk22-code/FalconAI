from app.ai.signal_engine import SignalEngine


class MultiTimeframeEngine:

    def __init__(self):

        self.signal = SignalEngine()


    def analyze(
        self,
        symbol="BTCUSDT",
        market="crypto"
    ):

        intervals = [

            "1m",
            "5m",
            "15m",
            "1h",
            "4h",
            "1d"

        ]


        results = {}


        for interval in intervals:

            try:

                analysis = self.signal.analyze(
                    symbol=symbol,
                    interval=interval,
                    market=market
                )


                results[interval] = {

                    "direction":
                    analysis.get(
                        "direction"
                    ),

                    "confidence":
                    analysis.get(
                        "confidence"
                    ),

                    "price":
                    analysis.get(
                        "price"
                    ),

                    "reasons":
                    analysis.get(
                        "decision_reasons",
                        []
                    )

                }


            except Exception as e:

                results[interval] = {

                    "direction": "ERROR",

                    "confidence": 0,

                    "error": str(e)

                }


        return results
