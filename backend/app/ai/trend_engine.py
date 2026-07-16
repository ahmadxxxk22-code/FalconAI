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


    def analyze(
        self,
        symbol="BTCUSDT",
        interval="1h",
        market="crypto"
    ):

        prices = self.market.get_close_prices(
            symbol=symbol,
            interval=interval,
            limit=400,
            market=market
        )

        candles = self.market.get_candles(
            symbol=symbol,
            interval=interval,
            limit=400,
            market=market
        )


        if len(prices) < EMA_LONG:
            raise Exception(
                "Not enough candles."
            )


        last_price = prices[-1]


        ema20 = self.indicators.ema(
            prices,
            EMA_FAST
        )

        ema50 = self.indicators.ema(
            prices,
            EMA_MEDIUM
        )

        ema100 = self.indicators.ema(
            prices,
            EMA_SLOW
        )

        ema200 = self.indicators.ema(
            prices,
            EMA_LONG
        )


        sma200 = self.indicators.sma(
            prices,
            SMA_LONG
        )


        rsi = self.indicators.rsi(
            prices
        )

        macd = self.indicators.macd(
            prices
        )

        momentum = self.indicators.momentum(
            prices
        )

        atr = self.indicators.atr(
            candles
        )

        trend_strength = self.indicators.trend_strength(
            prices
        )


        score = 0
        reasons = []


        # ==========================
        # EMA Score
        # ==========================

        if last_price > ema20:
            score += 5
            reasons.append(
                "Price above EMA20"
            )
        else:
            score -= 5


        if last_price > ema50:
            score += 10
            reasons.append(
                "Price above EMA50"
            )
        else:
            score -= 10


        if last_price > ema100:
            score += 15
            reasons.append(
                "Price above EMA100"
            )
        else:
            score -= 15


        if last_price > ema200:
            score += 20
            reasons.append(
                "Price above EMA200"
            )
        else:
            score -= 20



        # ==========================
        # EMA Alignment
        # ==========================

        if ema20 > ema50 > ema100 > ema200:

            score += 15

            reasons.append(
                "EMA Alignment Bullish"
            )

        elif ema20 < ema50 < ema100 < ema200:

            score -= 15

            reasons.append(
                "EMA Alignment Bearish"
            )


        # ==========================
        # EMA200 Slope
        # ==========================

        previous_ema200 = self.indicators.ema(
            prices[:-1],
            EMA_LONG
        ) if len(prices[:-1]) >= EMA_LONG else ema200

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
        # RSI
        # ==========================

        if rsi < RSI_OVERSOLD:

            score += 15

            reasons.append(
                "RSI Oversold"
            )


        elif rsi > RSI_OVERBOUGHT:

            score -= 15

            reasons.append(
                "RSI Overbought"
            )


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

            reasons.append(
                "MACD Bullish"
            )

        else:

            score -= 15



        # ==========================
        # Momentum
        # ==========================

        if momentum > 0:

            score += 10

            reasons.append(
                "Positive Momentum"
            )

        else:

            score -= 10



        # ==========================
        # ATR Confirmation
        # ==========================

        average_atr = self.indicators.atr(
            candles[:-20]
        )

        if average_atr > 0:

            if atr > average_atr:

                score += 5

                reasons.append(
                    "ATR confirms movement"
                )

            else:

                score -= 5



        # ==========================
        # Trend Result
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



        return {

            "symbol": symbol,

            "market": market,
            
            "interval": interval,

            "price": last_price,

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

            "trend_strength": trend_strength,

            "reasons": reasons

        }
