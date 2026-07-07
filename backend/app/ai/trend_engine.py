        # ==========================
        # EMA Score
        # ==========================

        if last_price > ema20:
            score += 5
            reasons.append("Price above EMA20")
        else:
            score -= 5

        if last_price > ema50:
            score += 10
            reasons.append("Price above EMA50")
        else:
            score -= 10

        if last_price > ema100:
            score += 15
            reasons.append("Price above EMA100")
        else:
            score -= 15

        if last_price > ema200:
            score += 20
            reasons.append("Price above EMA200")
        else:
            score -= 20

        # ==========================
        # SMA200
        # ==========================

        if last_price > sma200:
            score += 10
            reasons.append("Above SMA200")
        else:
            score -= 10

        # ==========================
        # RSI
        # ==========================

        if rsi < RSI_OVERSOLD:
            score += 15
            reasons.append("RSI Oversold")

        elif rsi > RSI_OVERBOUGHT:
            score -= 15
            reasons.append("RSI Overbought")

        else:
            if rsi > 55:
                score += 5

            elif rsi < 45:
                score -= 5

        # ==========================
        # MACD
        # ==========================

        if macd > 0:
            score += 15
            reasons.append("MACD Bullish")
        else:
            score -= 15

        # ==========================
        # Momentum
        # ==========================

        if momentum > 0:
            score += 10
            reasons.append("Positive Momentum")
        else:
            score -= 10
        # ==========================
        # Trend Strength
        # ==========================

        if trend_strength > 10:
            score += 20
            reasons.append("Strong Up Trend")

        elif trend_strength > 5:
            score += 10
            reasons.append("Medium Up Trend")

        elif trend_strength < -10:
            score -= 20
            reasons.append("Strong Down Trend")

        elif trend_strength < -5:
            score -= 10
            reasons.append("Medium Down Trend")

        # ==========================
        # ATR Filter
        # ==========================

        if atr > 0:

            volatility_percent = (atr / last_price) * 100

        else:

            volatility_percent = 0

        if volatility_percent > 4:

            score -= 5

            reasons.append("High Volatility")

        # ==========================
        # Trend Classification
        # ==========================

        if score >= 70:

            trend = TREND_STRONG_BULL

        elif score >= 35:

            trend = TREND_BULL

        elif score <= -70:

            trend = TREND_STRONG_BEAR

        elif score <= -35:

            trend = TREND_BEAR

        else:

            trend = TREND_SIDEWAYS

        bullish = trend in (
            TREND_BULL,
            TREND_STRONG_BULL
        )

        bearish = trend in (
            TREND_BEAR,
            TREND_STRONG_BEAR
        )

        confidence = abs(score)

        if confidence > 100:
            confidence = 100

        if confidence < 5:
            confidence = 5

        return {

            "symbol": symbol,

            "interval": interval,

            "price": round(last_price, 4),

            "trend": trend,

            "trend_strength": trend_strength,

            "confidence": confidence,

            "bullish": bullish,

            "bearish": bearish,

            "score": score,

            "ema20": ema20,

            "ema50": ema50,

            "ema100": ema100,

            "ema200": ema200,

            "sma200": sma200,

            "rsi": rsi,

            "macd": macd,

            "momentum": momentum,

            "atr": atr,

            "volatility_percent": round(
                volatility_percent,
                2
            ),

            "reasons": reasons

        }
