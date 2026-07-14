class LiquidityEngine:

    def analyze(self, candles):

        if len(candles) < 20:
            return {
                "liquidity": "UNKNOWN",
                "score": 0,
                "buy_liquidity": False,
                "sell_liquidity": False
            }

        highs = [c["high"] for c in candles[-20:]]
        lows = [c["low"] for c in candles[-20:]]

        highest = max(highs)
        lowest = min(lows)

        current = candles[-1]

        buy_liquidity = current["high"] >= highest
        sell_liquidity = current["low"] <= lowest

        score = 0

        if buy_liquidity:
            score += 20

        if sell_liquidity:
            score += 20

        liquidity = "NORMAL"

        if buy_liquidity:
            liquidity = "BUY_SIDE"

        if sell_liquidity:
            liquidity = "SELL_SIDE"

        if buy_liquidity and sell_liquidity:
            liquidity = "HIGH_VOLATILITY"

        return {
            "liquidity": liquidity,
            "score": score,
            "buy_liquidity": buy_liquidity,
            "sell_liquidity": sell_liquidity
        }
