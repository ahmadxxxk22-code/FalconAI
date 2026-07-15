from app.services.market_data import MarketData
from app.services.indicator_engine import IndicatorEngine


class MarketAnalyzer:

    def __init__(self):

        self.market = MarketData()
        self.indicators = IndicatorEngine()


    def analyze(
        self,
        symbol="BTCUSDT",
        interval="1h",
        market="crypto"
    ):

        candles = self.market.get_candles(
            symbol=symbol,
            interval=interval,
            limit=300,
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


        price = prices[-1]


        ema = self.indicators.ema(
            prices
        )

        sma = self.indicators.sma(
            prices
        )

        rsi = self.indicators.rsi(
            prices
        )

        macd = self.indicators.macd(
            prices
        )

        trend = self.indicators.trend_strength(
            prices
        )

        volatility = self.indicators.volatility(
            prices
        )

        atr = self.indicators.atr(
            candles
        )

        momentum = self.indicators.momentum(
            prices
        )


        average_volume = (
            sum(volumes) / len(volumes)
        )


        current_volume = volumes[-1]


        volume_power = (

            current_volume /
            average_volume

            if average_volume > 0

            else 0

        )


        market_state = self.market_condition(
            trend,
            volatility,
            rsi
        )


        bullish_score = 0
        bearish_score = 0


        reasons = []


        if price > ema:

            bullish_score += 1

            reasons.append(
                "السعر فوق متوسط EMA"
            )

        else:

            bearish_score += 1

            reasons.append(
                "السعر تحت متوسط EMA"
            )


        if trend > 0:

            bullish_score += 1

            reasons.append(
                "الاتجاه العام صاعد"
            )

        elif trend < 0:

            bearish_score += 1

            reasons.append(
                "الاتجاه العام هابط"
            )


        if macd > 0:

            bullish_score += 1

            reasons.append(
                "MACD إيجابي"
            )

        else:

            bearish_score += 1

            reasons.append(
                "MACD سلبي"
            )


        if volume_power > 1:

            reasons.append(
                "حجم التداول أعلى من المتوسط"
            )


        if rsi < 35:

            reasons.append(
                "السوق قريب من التشبع البيعي"
            )


        if rsi > 65:

            reasons.append(
                "السوق قريب من التشبع الشرائي"
            )


        bullish = (
            bullish_score > bearish_score
        )


        bearish = (
            bearish_score > bullish_score
        )


        return {

            "symbol": symbol,

            "market": market,

            "interval": interval,


            "price": price,

            "ema": ema,

            "sma": sma,

            "rsi": rsi,

            "macd": macd,

            "trend_strength": trend,

            "volatility": volatility,

            "atr": atr,

            "momentum": momentum,

            "volume_power": round(
                volume_power,
                2
            ),


            "market_state": market_state,


            "bullish": bullish,

            "bearish": bearish,


            "analysis_reasons": reasons

        }



    def market_condition(
        self,
        trend,
        volatility,
        rsi
    ):


        if abs(trend) < 0.5:

            return "SIDEWAYS"


        if trend > 0:

            if volatility > 0:

                return "BULLISH_TREND"


        if trend < 0:

            return "BEARISH_TREND"


        return "UNKNOWN"

"candles": candles,
