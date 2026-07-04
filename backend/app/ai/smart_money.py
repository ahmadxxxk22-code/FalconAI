from app.services.market_data import MarketData


class SmartMoneyAnalyzer:

    def __init__(self):

        self.market = MarketData()

    def analyze(
        self,
        symbol="BTCUSDT",
        interval="1h"
    ):

        candles = self.market.get_candles(
            symbol=symbol,
            interval=interval,
            limit=200
        )

        last = candles[-1]

        highs = [c["high"] for c in candles[-20:]]
        lows = [c["low"] for c in candles[-20:]]

        highest = max(highs)
        lowest = min(lows)

        bullish = False
        bearish = False

        signal = "WAIT"
        confidence = 50

        liquidity = "NONE"
        bos = False
        choch = False
        order_block = None
        fair_value_gap = None

        if last["close"] > highest * 0.995:

            bullish = True

            signal = "BUY"

            confidence = 85

            liquidity = "BUY_SIDE"

            bos = True

            order_block = highest

        elif last["close"] < lowest * 1.005:

            bearish = True

            signal = "SELL"

            confidence = 85

            liquidity = "SELL_SIDE"

            choch = True

            order_block = lowest

        if len(candles) >= 3:

            c1 = candles[-3]
            c2 = candles[-2]
            c3 = candles[-1]

            if c3["low"] > c1["high"]:

                fair_value_gap = {

                    "type": "BULLISH",

                    "top": c3["low"],

                    "bottom": c1["high"]

                }

            elif c3["high"] < c1["low"]:

                fair_value_gap = {

                    "type": "BEARISH",

                    "top": c1["low"],

                    "bottom": c3["high"]

                }

        return {

            "signal": signal,

            "bullish": bullish,

            "bearish": bearish,

            "confidence": confidence,

            "liquidity": liquidity,

            "bos": bos,

            "choch": choch,

            "order_block": order_block,

            "fair_value_gap": fair_value_gap

        }
