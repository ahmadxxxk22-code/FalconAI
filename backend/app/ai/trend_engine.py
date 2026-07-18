from typing import Dict

from app.services.market_data import MarketData
from app.services.indicator_engine import IndicatorEngine

from app.ai.core.constants import (
    TREND_STRONG_BULL,
    TREND_BULL,
    TREND_SIDEWAYS,
    TREND_BEAR,
    TREND_STRONG_BEAR,
    EMA_FAST,
    EMA_MEDIUM,
    EMA_SLOW,
    EMA_LONG,
    SMA_LONG,
    RSI_OVERSOLD,
    RSI_OVERBOUGHT
)


class TrendEngine:

    def __init__(self):

        self.market = MarketData()

        self.indicators = IndicatorEngine()

        self.weights = {

            "ema": 25,

            "trend": 25,

            "macd": 15,

            "rsi": 10,

            "momentum": 10,

            "adx": 10,

            "volume": 5

        }


    def analyze(

        self,

        symbol="BTCUSDT",

        interval="1h",

        market="crypto"

    ) -> Dict:


        prices = self.market.get_close_prices(

            symbol=symbol,

            interval=interval,

            limit=500,

            market=market

        )


        candles = self.market.get_candles(

            symbol=symbol,

            interval=interval,

            limit=500,

            market=market

        )


        if len(prices) < EMA_LONG:

            raise Exception(

                "Not enough candles."

            )


        last_price = prices[-1]


        ema20 = self.indicators.ema(prices, EMA_FAST)

        ema50 = self.indicators.ema(prices, EMA_MEDIUM)

        ema100 = self.indicators.ema(prices, EMA_SLOW)

        ema200 = self.indicators.ema(prices, EMA_LONG)

        sma200 = self.indicators.sma(prices, SMA_LONG)


        rsi = self.indicators.rsi(prices)

        macd = self.indicators.macd(prices)

        momentum = self.indicators.momentum(prices)

        atr = self.indicators.atr(candles)

        trend_strength = self.indicators.trend_strength(prices)

        volatility = self.indicators.volatility(prices)


        try:

            adx = self.indicators.adx(candles)

        except Exception:

            adx = 0


        try:

            volume_ratio = self.indicators.volume_ratio(

                [

                    candle["volume"]

                    for candle in candles

                ]

            )

        except Exception:

            volume_ratio = 1


        score = 0

        reasons = []



        # ==========================
        # EMA SCORE
        # ==========================

        if last_price > ema20:

            score += 5

            reasons.append(
                "Price above EMA20"
            )

        else:

            score -= 5


        if last_price > ema50:

            score += 8

            reasons.append(
                "Price above EMA50"
            )

        else:

            score -= 8


        if last_price > ema100:

            score += 10

            reasons.append(
                "Price above EMA100"
            )

        else:

            score -= 10


        if last_price > ema200:

            score += self.weights["ema"]

            reasons.append(
                "Price above EMA200"
            )

        else:

            score -= self.weights["ema"]


        # ==========================
        # EMA ALIGNMENT
        # ==========================

        if ema20 > ema50 > ema100 > ema200:

            score += 15

            reasons.append(
                "Bullish EMA Alignment"
            )

        elif ema20 < ema50 < ema100 < ema200:

            score -= 15

            reasons.append(
                "Bearish EMA Alignment"
            )


        # ==========================
        # EMA200 SLOPE
        # ==========================

        previous_ema200 = self.indicators.ema(
            prices[:-1],
            EMA_LONG
        )

        if ema200 > previous_ema200:

            score += 10

            reasons.append(
                "EMA200 Rising"
            )

        elif ema200 < previous_ema200:

            score -= 10

            reasons.append(
                "EMA200 Falling"
            )


        # ==========================
        # SMA200
        # ==========================

        if last_price > sma200:

            score += 10

            reasons.append(
                "Above SMA200"
            )

        else:

            score -= 10


        # ==========================
        # ADX
        # ==========================

        if adx >= 30:

            score += self.weights["adx"]

            reasons.append(
                "Strong Trend (ADX)"
            )

        elif adx >= 20:

            score += 5

            reasons.append(
                "Medium Trend (ADX)"
            )

        else:

            reasons.append(
                "Weak Trend"
            )



        # ==========================
        # RSI
        # ==========================

        if rsi <= RSI_OVERSOLD:

            score += self.weights["rsi"]

            reasons.append(
                "RSI Oversold"
            )

        elif rsi >= RSI_OVERBOUGHT:

            score -= self.weights["rsi"]

            reasons.append(
                "RSI Overbought"
            )

        elif rsi > 55:

            score += 5

            reasons.append(
                "RSI Bullish"
            )

        elif rsi < 45:

            score -= 5

            reasons.append(
                "RSI Bearish"
            )


        # ==========================
        # MACD
        # ==========================

        if macd > 0:

            score += self.weights["macd"]

            reasons.append(
                "MACD Bullish"
            )

        elif macd < 0:

            score -= self.weights["macd"]

            reasons.append(
                "MACD Bearish"
            )


        # ==========================
        # MOMENTUM
        # ==========================

        if momentum > 0:

            score += self.weights["momentum"]

            reasons.append(
                "Positive Momentum"
            )

        elif momentum < 0:

            score -= self.weights["momentum"]

            reasons.append(
                "Negative Momentum"
            )


        # ==========================
        # VOLUME
        # ==========================

        if volume_ratio >= 1.5:

            score += self.weights["volume"]

            reasons.append(
                "Strong Buying Volume"
            )

        elif volume_ratio <= 0.7:

            score -= self.weights["volume"]

            reasons.append(
                "Weak Volume"
            )


        # ==========================
        # ATR CONFIRMATION
        # ==========================

        try:

            avg_atr = self.indicators.atr(

                candles[:-20]

            )

        except Exception:

            avg_atr = atr


        if atr > avg_atr:

            score += 5

            reasons.append(
                "ATR confirms movement"
            )

        else:

            score -= 2

            reasons.append(
                "Weak volatility"
            )


        # ==========================
        # VOLATILITY
        # ==========================

        if volatility > atr:

            score += 3

            reasons.append(
                "High Market Activity"
            )



        # ==========================
        # FINAL TREND
        # ==========================

        if score >= 90:

            trend = TREND_STRONG_BULL

        elif score >= 45:

            trend = TREND_BULL

        elif score <= -90:

            trend = TREND_STRONG_BEAR

        elif score <= -45:

            trend = TREND_BEAR

        else:

            trend = TREND_SIDEWAYS


        # ==========================
        # MARKET QUALITY
        # ==========================

        market_quality = round(

            (

                abs(score)

                +

                adx

                +

                volume_ratio * 10

            ) / 3,

            2

        )


        # ==========================
        # CONFIDENCE
        # ==========================

        confidence = round(

            min(

                100,

                abs(score) * 0.7

                +

                adx * 0.2

                +

                volume_ratio * 10 * 0.1

            ),

            2

        )


        # ==========================
        # TREND POWER
        # ==========================

        trend_power = {

            "bullish": score if score > 0 else 0,

            "bearish": abs(score) if score < 0 else 0,

            "quality": market_quality

        }


        # ==========================
        # RETURN
        # ==========================

        return {

            "symbol": symbol,

            "market": market,

            "interval": interval,

            "price": last_price,

            "trend": trend,

            "score": score,

            "confidence": confidence,

            "market_quality": market_quality,

            "trend_power": trend_power,

            "ema20": ema20,

            "ema50": ema50,

            "ema100": ema100,

            "ema200": ema200,

            "sma200": sma200,

            "adx": adx,

            "rsi": rsi,

            "macd": macd,

            "momentum": momentum,

            "atr": atr,

            "volatility": volatility,

            "volume_ratio": volume_ratio,

            "trend_strength": trend_strength,

            "reasons": reasons

        }
