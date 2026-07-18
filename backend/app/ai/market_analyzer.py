from typing import Dict, List

from app.services.market_data import MarketData
from app.services.indicator_engine import IndicatorEngine


class MarketAnalyzer:

    def __init__(self):

        self.market = MarketData()

        self.indicators = IndicatorEngine()

        # ==========================
        # Dynamic Weights
        # ==========================

        self.weights = {

            "trend": 25,

            "ema": 20,

            "macd": 15,

            "rsi": 10,

            "volume": 10,

            "momentum": 10,

            "support": 5,

            "resistance": 5

        }


    # ==================================================
    # MAIN ANALYSIS
    # ==================================================

    def analyze(

        self,

        symbol="BTCUSDT",

        interval="1h",

        market="crypto"

    ) -> Dict:


        candles = self.market.get_candles(

            symbol=symbol,

            interval=interval,

            limit=500,

            market=market

        )


        if not candles:

            raise Exception(

                "No market candles received."

            )


        prices = [

            candle["close"]

            for candle in candles

        ]


        volumes = [

            candle["volume"]

            for candle in candles

        ]


        highs = [

            candle["high"]

            for candle in candles

        ]


        lows = [

            candle["low"]

            for candle in candles

        ]


        opens = [

            candle["open"]

            for candle in candles

        ]


        price = prices[-1]


        # ==========================
        # EMA
        # ==========================

        ema20 = self.indicators.ema(

            prices,

            20

        )


        ema50 = self.indicators.ema(

            prices,

            50

        )


        ema100 = self.indicators.ema(

            prices,

            100

        )


        ema200 = self.indicators.ema(

            prices,

            200

        )


        sma200 = self.indicators.sma(

            prices,

            200

        )


        # ==========================
        # Oscillators
        # ==========================

        rsi = self.indicators.rsi(

            prices

        )


        macd = self.indicators.macd(

            prices

        )


        momentum = self.indicators.momentum(

            prices

        )


        trend_strength = self.indicators.trend_strength(

            prices

        )


        volatility = self.indicators.volatility(

            prices

        )


        atr = self.indicators.atr(

            candles

        )



        # ==========================
        # Advanced Indicators
        # ==========================

        try:

            adx = self.indicators.adx(

                candles

            )

        except Exception:

            adx = 0


        try:

            bollinger = self.indicators.bollinger(

                prices

            )

        except Exception:

            bollinger = {

                "upper": price,

                "middle": price,

                "lower": price

            }


        try:

            vwap = self.indicators.vwap(

                candles

            )

        except Exception:

            vwap = price


        # ==========================
        # Volume
        # ==========================

        volume_average = self.indicators.volume_average(

            volumes

        )


        volume_ratio = self.indicators.volume_ratio(

            volumes

        )


        # ==========================
        # Price Change
        # ==========================

        price_change = self.indicators.price_change(

            prices

        )


        # ==========================
        # Support / Resistance
        # ==========================

        sr = self.indicators.support_resistance_detection(

            prices

        )


        support = sr.get(

            "support"

        )


        resistance = sr.get(

            "resistance"

        )


        # ==========================
        # Internal Scores
        # ==========================

        bullish_score = 0

        bearish_score = 0

        reasons = []



        # ==========================
        # EMA
        # ==========================

        if price > ema20:

            bullish_score += self.weights["ema"]

            reasons.append(

                "السعر أعلى من EMA20"

            )

        else:

            bearish_score += self.weights["ema"]

            reasons.append(

                "السعر أسفل EMA20"

            )


        if ema20 > ema50 > ema100 > ema200:

            bullish_score += 10

            reasons.append(

                "ترتيب EMA صاعد"

            )


        elif ema20 < ema50 < ema100 < ema200:

            bearish_score += 10

            reasons.append(

                "ترتيب EMA هابط"

            )


        # ==========================
        # Trend
        # ==========================

        if trend_strength > 2:

            bullish_score += self.weights["trend"]

            reasons.append(

                "اتجاه صاعد قوي"

            )


        elif trend_strength > 0:

            bullish_score += 10

            reasons.append(

                "اتجاه صاعد"

            )


        elif trend_strength < -2:

            bearish_score += self.weights["trend"]

            reasons.append(

                "اتجاه هابط قوي"

            )


        elif trend_strength < 0:

            bearish_score += 10

            reasons.append(

                "اتجاه هابط"

            )


        # ==========================
        # ADX
        # ==========================

        if adx > 25:

            reasons.append(

                "ADX يؤكد قوة الاتجاه"

            )


        else:

            reasons.append(

                "الاتجاه ضعيف"

            )


        # ==========================
        # RSI
        # ==========================

        if rsi <= 30:

            bullish_score += self.weights["rsi"]

            reasons.append(

                "تشبع بيعي"

            )


        elif rsi >= 70:

            bearish_score += self.weights["rsi"]

            reasons.append(

                "تشبع شرائي"

        )



        # ==========================
        # MACD
        # ==========================

        if macd > 0:

            bullish_score += self.weights["macd"]

            reasons.append(

                "MACD إيجابي"

            )

        elif macd < 0:

            bearish_score += self.weights["macd"]

            reasons.append(

                "MACD سلبي"

            )


        # ==========================
        # Momentum
        # ==========================

        if momentum > 0:

            bullish_score += self.weights["momentum"]

            reasons.append(

                "الزخم إيجابي"

            )

        elif momentum < 0:

            bearish_score += self.weights["momentum"]

            reasons.append(

                "الزخم سلبي"

            )


        # ==========================
        # Volume
        # ==========================

        if volume_ratio >= 1.5:

            bullish_score += self.weights["volume"]

            reasons.append(

                "حجم تداول قوي"

            )

        elif volume_ratio >= 1:

            bullish_score += 5

            reasons.append(

                "حجم تداول جيد"

            )

        elif volume_ratio < 0.7:

            bearish_score += self.weights["volume"]

            reasons.append(

                "ضعف حجم التداول"

            )


        # ==========================
        # Price Change
        # ==========================

        if price_change > 2:

            bullish_score += 10

            reasons.append(

                "اندفاع سعري قوي"

            )

        elif price_change > 0:

            bullish_score += 5

            reasons.append(

                "السعر يتحرك للأعلى"

            )

        elif price_change < -2:

            bearish_score += 10

            reasons.append(

                "اندفاع هبوطي قوي"

            )

        elif price_change < 0:

            bearish_score += 5

            reasons.append(

                "السعر يتحرك للأسفل"

            )


        # ==========================
        # Support / Resistance
        # ==========================

        if support and price <= support:

            bullish_score += self.weights["support"]

            reasons.append(

                "السعر عند دعم"

            )


        if resistance and price >= resistance:

            bearish_score += self.weights["resistance"]

            reasons.append(

                "السعر عند مقاومة"

            )



        # ==========================
        # Market State
        # ==========================

        market_state = self.market_condition(
            trend_strength,
            volatility,
            rsi
        )

        # ==========================
        # Final Signal
        # ==========================

        difference = bullish_score - bearish_score

        if difference >= 20:
            signal = "BUY"

        elif difference <= -20:
            signal = "SELL"

        else:
            signal = "WAIT"

        # ==========================
        # Confidence
        # ==========================

        confidence = self.calculate_confidence(
            bullish_score,
            bearish_score,
            trend_strength,
            adx,
            volume_ratio,
            volatility
        )

        # ==========================
        # Market Power
        # ==========================

        market_power = round(
            (
                abs(trend_strength)
                + abs(momentum)
                + volume_ratio
            ),
            2
        )

        # ==========================
        # Return
        # ==========================

        return {

            "symbol": symbol,
            "market": market,
            "interval": interval,

            "price": price,

            "ema20": ema20,
            "ema50": ema50,
            "ema100": ema100,
            "ema200": ema200,

            "sma200": sma200,

            "rsi": rsi,
            "macd": macd,
            "adx": adx,

            "momentum": momentum,

            "volatility": volatility,
            "atr": atr,

            "vwap": vwap,
            "bollinger": bollinger,

            "volume_average": volume_average,
            "volume_ratio": volume_ratio,

            "price_change": price_change,

            "support": support,
            "resistance": resistance,

            "market_state": market_state,
            "market_power": market_power,

            "signal": signal,
            "confidence": confidence,

            "bullish_score": bullish_score,
            "bearish_score": bearish_score,

            "analysis_reasons": reasons,

            "candles": candles

        }


    # ==================================================
    # Confidence Engine
    # ==================================================

    def calculate_confidence(
        self,
        bullish,
        bearish,
        trend,
        adx,
        volume_ratio,
        volatility
    ):

        total = bullish + bearish

        if total <= 0:
            return 0

        confidence = (
            (max(bullish, bearish) / total) * 60
            + min(abs(trend) * 5, 15)
            + min(adx, 15)
            + min(volume_ratio * 5, 5)
            + min(volatility, 5)
        )

        return round(
            min(confidence, 100),
            2
        )
