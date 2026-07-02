class PatternAnalyzer:

    def detect(self, symbol="BTCUSDT", interval="1h"):

        # هنا لاحقاً ممكن نربطه ببيانات الشموع الحقيقية
        # حالياً نستخدم آخر بيانات السوق من MarketAnalyzer

        return {
            "pattern": "No Clear Pattern",
            "signal": "WAIT",
            "strength": 0
        }

    # ----------------------------
    # Bullish Engulfing (مستقبلي)
    # ----------------------------
    def bullish_engulfing(self, candles):

        if len(candles) < 2:
            return False

        prev = candles[-2]
        curr = candles[-1]

        return (
            prev["close"] < prev["open"] and
            curr["close"] > curr["open"] and
            curr["close"] > prev["open"]
        )

    # ----------------------------
    # Bearish Engulfing (مستقبلي)
    # ----------------------------
    def bearish_engulfing(self, candles):

        if len(candles) < 2:
            return False

        prev = candles[-2]
        curr = candles[-1]

        return (
            prev["close"] > prev["open"] and
            curr["close"] < curr["open"] and
            curr["close"] < prev["open"]
        )

    # ----------------------------
    # Doji
    # ----------------------------
    def doji(self, candle):

        body = abs(candle["close"] - candle["open"])

        return body < (candle["high"] - candle["low"]) * 0.1
