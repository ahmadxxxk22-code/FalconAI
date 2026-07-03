class FibonacciAnalyzer:

    def analyze(self, high=0, low=0, current_price=0):

        if high <= low:
            return {
                "signal": "WAIT",
                "levels": {},
                "nearest_level": None
            }

        diff = high - low

        levels = {

            "0.236": high - diff * 0.236,

            "0.382": high - diff * 0.382,

            "0.500": high - diff * 0.500,

            "0.618": high - diff * 0.618,

            "0.786": high - diff * 0.786

        }

        nearest = min(
            levels,
            key=lambda x: abs(levels[x] - current_price)
        )

        signal = "WAIT"

        if current_price <= levels["0.618"]:

            signal = "BUY"

        elif current_price >= levels["0.236"]:

            signal = "SELL"

        return {

            "signal": signal,

            "levels": levels,

            "nearest_level": nearest

        }
