from typing import Dict, Any

from app.services.market_data import MarketData
from app.services.indicator_engine import IndicatorEngine


class MarketAnalyzer:

    def __init__(self):

        self.market = MarketData()

        self.indicators = IndicatorEngine()


        # ==========================
        # Dynamic AI Weights
        # ==========================

        self.weights = {

            "trend": 25,

            "ema": 20,

            "macd": 15,

            "rsi": 10,

            "volume": 10,

            "momentum": 10,

            "support": 5,

            "resistance": 5,

            "breakout": 10,

            "reversal": 10

        }


        # ==========================
        # Supported Markets
        # ==========================

        self.supported_markets = [

            "crypto",

            "forex",

            "stocks",

            "gold",

            "oil",

            "indices"

        ]


    # ==================================================
    # MAIN MARKET ANALYSIS
    # ==================================================

    def analyze(

        self,

        symbol="BTCUSDT",

        interval="1h",

        market="crypto"

    ) -> Dict[str, Any]:


        if market not in self.supported_markets:

            market = "crypto"


        candles = self.market.get_candles(

            symbol=symbol,

            interval=interval,

            limit=500,

            market=market

        )


        if not candles:

            raise Exception(

                "No market candles received"

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


        price = prices[-1]


        # ==========================
        # Basic Indicators
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
        # Volume Intelligence
        # ==========================


        volume_average = self.indicators.volume_average(

            volumes

        )


        volume_ratio = self.indicators.volume_ratio(

            volumes

        )



        # ==========================
        # Price Behavior
        # ==========================


        price_change = self.indicators.price_change(

            prices

        )



        # ==========================
        # Support Resistance
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
        # FalconAI Intelligence
        # ==========================


        trend_quality = self.calculate_trend_quality(

            trend_strength,

            adx,

            volume_ratio

        )


        reversal = self.detect_reversal(

            prices,

            rsi,

            momentum,

            volume_ratio

        )


        surprise_move = self.detect_surprise_move(

            prices,

            volumes,

            volatility

        )


        market_regime = self.detect_market_regime(

            trend_strength,

            volatility,

            adx

        )


        # ==========================
        # Internal Scores
        # ==========================


        bullish_score = 0

        bearish_score = 0


        reasons = []



        # ==========================
        # EMA Intelligence
        # ==========================


        if price > ema20:

            bullish_score += self.weights["ema"]

            reasons.append(
                "السعر فوق EMA20"
            )

        else:

            bearish_score += self.weights["ema"]

            reasons.append(
                "السعر تحت EMA20"
            )



        if ema20 > ema50 > ema100 > ema200:

            bullish_score += 15

            reasons.append(
                "ترتيب المتوسطات صاعد"
            )


        elif ema20 < ema50 < ema100 < ema200:

            bearish_score += 15

            reasons.append(
                "ترتيب المتوسطات هابط"
            )



        # ==========================
        # Trend Quality
        # ==========================


        if trend_quality >= 80:

            if trend_strength > 0:

                bullish_score += 20

                reasons.append(
                    "اتجاه صاعد قوي بجودة عالية"
                )

            else:

                bearish_score += 20

                reasons.append(
                    "اتجاه هابط قوي بجودة عالية"
                )


        elif trend_quality >= 50:

            reasons.append(
                "اتجاه متوسط"
            )


        else:

            reasons.append(
                "اتجاه ضعيف"
            )



        # ==========================
        # RSI Intelligence
        # ==========================


        if rsi <= 30:

            bullish_score += 10

            reasons.append(
                "تشبع بيع - احتمال ارتداد"
            )


        elif rsi >= 70:

            bearish_score += 10

            reasons.append(
                "تشبع شراء - خطر هبوط"
            )



        elif 45 <= rsi <= 55:

            reasons.append(
                "RSI محايد"
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
                "الزخم صاعد"
            )


        elif momentum < 0:

            bearish_score += self.weights["momentum"]

            reasons.append(
                "الزخم هابط"
            )



        # ==========================
        # Volume Intelligence
        # ==========================


        if volume_ratio >= 1.5:

            bullish_score += 10

            reasons.append(
                "حجم تداول غير طبيعي داعم"
            )


        elif volume_ratio < 0.7:

            warnings = [
                "ضعف حجم التداول"
            ]

        else:

            warnings = []



        # ==========================
        # Reversal Intelligence
        # ==========================


        if reversal.get("signal") == "BULLISH_REVERSAL":

            bullish_score += self.weights["reversal"]

            reasons.append(
                "اكتشاف انعكاس صاعد مبكر"
            )


        elif reversal.get("signal") == "BEARISH_REVERSAL":

            bearish_score += self.weights["reversal"]

            reasons.append(
                "اكتشاف انعكاس هابط مبكر"
            )



        # ==========================
        # Surprise Move Detection
        # ==========================


        if surprise_move.get("active"):

            if surprise_move.get("direction") == "UP":

                bullish_score += self.weights["breakout"]

                reasons.append(
                    "حركة صعود مفاجئة محتملة"
                )


            elif surprise_move.get("direction") == "DOWN":

                bearish_score += self.weights["breakout"]

                reasons.append(
                    "حركة هبوط مفاجئة محتملة"
                )



        # ==========================
        # Support Resistance
        # ==========================


        if support and price <= support:

            bullish_score += self.weights["support"]

            reasons.append(
                "السعر قريب من منطقة دعم"
            )


        if resistance and price >= resistance:

            bearish_score += self.weights["resistance"]

            reasons.append(
                "السعر قريب من منطقة مقاومة"
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

            abs(trend_strength)

            +

            abs(momentum)

            +

            volume_ratio,

            2

        )



        return {


            "symbol": symbol,

            "market": market,

            "interval": interval,


            "price": price,


            "signal": signal,

            "confidence": confidence,


            "bullish_score": bullish_score,

            "bearish_score": bearish_score,


            "trend_quality": trend_quality,


            "market_regime": market_regime,


            "early_reversal": reversal,


            "surprise_move": surprise_move,


            "market_power": market_power,


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


            "market_state": market_regime,


            "analysis_reasons": reasons,


            "warnings": warnings,


            "candles": candles

        }



    # ==================================================
    # TREND QUALITY ENGINE
    # ==================================================

    def calculate_trend_quality(

        self,

        trend_strength,

        adx,

        volume_ratio

    ):

        score = 0


        score += min(
            abs(trend_strength) * 20,
            40
        )


        if adx >= 25:

            score += 30


        if volume_ratio >= 1:

            score += 20


        if volume_ratio >= 1.5:

            score += 10


        return round(
            min(score, 100),
            2
        )



    # ==================================================
    # EARLY REVERSAL DETECTOR
    # ==================================================

    def detect_reversal(

        self,

        prices,

        rsi,

        momentum,

        volume_ratio

    ):


        if len(prices) < 20:

            return {

                "signal": "NONE",

                "confidence": 0

            }


        recent = prices[-10:]

        previous = prices[-20:-10]


        recent_change = (

            recent[-1] - recent[0]

        )


        previous_change = (

            previous[-1] - previous[0]

        )



        # Bullish reversal

        if (

            previous_change < 0

            and

            recent_change > 0

            and

            rsi < 40

            and

            volume_ratio > 1

        ):

            return {

                "signal": "BULLISH_REVERSAL",

                "confidence": 80

            }



        # Bearish reversal

        if (

            previous_change > 0

            and

            recent_change < 0

            and

            rsi > 60

            and

            volume_ratio > 1

        ):

            return {

                "signal": "BEARISH_REVERSAL",

                "confidence": 80

            }



        return {

            "signal": "NONE",

            "confidence": 0

        }



    # ==================================================
    # SURPRISE MOVE DETECTOR
    # ==================================================

    def detect_surprise_move(

        self,

        prices,

        volumes,

        volatility

    ):


        if len(prices) < 30:

            return {

                "active": False

            }



        price_change = (

            (

                prices[-1]

                -

                prices[-10]

            )

            /

            prices[-10]

        ) * 100



        avg_volume = sum(

            volumes[-30:]

        ) / 30



        current_volume = volumes[-1]



        volume_spike = (

            current_volume

            /

            avg_volume

            if avg_volume

            else 0

        )



        strength = abs(price_change) * 10



        if (

            abs(price_change) >= 2

            and

            volume_spike >= 1.8

        ):


            return {

                "active": True,

                "direction":

                    "UP"

                    if price_change > 0

                    else "DOWN",


                "strength":

                    round(

                        min(strength,100),

                        2

                    )

            }



        return {

            "active": False,

            "direction": "NONE",

            "strength": 0

        }



    # ==================================================
    # MARKET REGIME DETECTOR
    # ==================================================

    def detect_market_regime(

        self,

        trend_strength,

        volatility,

        adx

    ):


        if adx >= 25 and abs(trend_strength) > 1:

            return "TRENDING"



        if volatility > 3:

            return "VOLATILE"



        if adx < 20:

            return "RANGING"



        return "NORMAL"



    # ==================================================
    # CONFIDENCE ENGINE
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

            (max(bullish,bearish) / total)

            * 60

            +

            min(abs(trend) * 5,15)

            +

            min(adx,15)

            +

            min(volume_ratio * 5,5)

            +

            min(volatility,5)

        )


        return round(

            min(confidence,100),

            2

        )
