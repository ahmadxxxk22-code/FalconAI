class OrderBlocksEngine:

    def analyze(self, candles):

        if len(candles) < 10:
            return {
                "bullish_blocks": [],
                "bearish_blocks": [],
                "nearest_block": None
            }

        bullish_blocks = []
        bearish_blocks = []

        for i in range(1, len(candles) - 1):

            prev = candles[i - 1]
            current = candles[i]
            nxt = candles[i + 1]

            # Bullish Order Block
            if (
                current["close"] < current["open"]
                and nxt["close"] > current["high"]
            ):

                bullish_blocks.append({
                    "low": current["low"],
                    "high": current["high"],
                    "index": i
                })

            # Bearish Order Block
            if (
                current["close"] > current["open"]
                and nxt["close"] < current["low"]
            ):

                bearish_blocks.append({
                    "low": current["low"],
                    "high": current["high"],
                    "index": i
                })

        nearest = None

        if bullish_blocks:
            nearest = bullish_blocks[-1]

        elif bearish_blocks:
            nearest = bearish_blocks[-1]

        return {

            "bullish_blocks": bullish_blocks,

            "bearish_blocks": bearish_blocks,

            "nearest_block": nearest

        }
