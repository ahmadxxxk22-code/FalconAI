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



        # ==========================
        # Indicators
        # ==========================


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


        trend_strength = self.indicators.trend_strength(
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



        # ==========================
        # Volume Analysis
        # ==========================


        volume_average = self.indicators.volume_average(
            volumes
        )


        volume_ratio = self.indicators.volume_ratio(
            volumes
        )



        # ==========================
        # Price Movement
        # ==========================


        price_change = self.indicators.price_change(
            prices
        )



        # ==========================
        # Support Resistance
        # ==========================


        support_resistance = self.indicators.support_resistance_detection(
            prices
        )


        support = support_resistance.get(
            "support"
        )


        resistance = support_resistance.get(
            "resistance"
        )



        # ==========================
        # Market State
        # ==========================


        market_state = self.market_condition(
            trend_strength,
            volatility,
            rsi
        )



        bullish_score = 0

        bearish_score = 0


        reasons = []



        # ==========================
        # EMA Analysis
        # ==========================


        if price > ema:

            bullish_score += 1

            reasons.append(
                "السعر فوق EMA"
            )


        else:

            bearish_score += 1

            reasons.append(
                "السعر تحت EMA"
            )



        # ==========================
        # Trend Analysis
        # ==========================


        if trend_strength > 0:

            bullish_score += 1

            reasons.append(
                "الاتجاه العام صاعد"
            )


        elif trend_strength < 0:

            bearish_score += 1

            reasons.append(
                "الاتجاه العام هابط"
            )



        # ==========================
        # MACD Analysis
        # ==========================


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



        # ==========================
        # Volume Analysis
        # ==========================


        if volume_ratio > 1:

            bullish_score += 1

            reasons.append(
                "حجم التداول أعلى من المتوسط"
            )


        elif volume_ratio < 0.8:

            bearish_score += 1

            reasons.append(
                "حجم التداول ضعيف"
            )



        # ==========================
        # Price Change Analysis
        # ==========================


        if price_change > 0:

            bullish_score += 1

            reasons.append(
                "تغير السعر إيجابي"
            )


        elif price_change < 0:

            bearish_score += 1

            reasons.append(
                "تغير السعر سلبي"
            )



        # ==========================
        # Momentum Analysis
        # ==========================


        if momentum > 0:

            bullish_score += 1

            reasons.append(
                "الزخم يدعم الصعود"
            )


        elif momentum < 0:

            bearish_score += 1

            reasons.append(
                "الزخم يدعم الهبوط"
            )



        # ==========================
        # RSI Analysis
        # ==========================


        if rsi < 35:

            reasons.append(
                "تشبع بيعي محتمل"
            )


        elif rsi > 65:

            reasons.append(
                "تشبع شرائي محتمل"
            )



        # ==========================
        # Support Resistance
        # ==========================


        if support and price <= support:

            bullish_score += 1

            reasons.append(
                "السعر قريب من منطقة دعم"
            )



        if resistance and price >= resistance:

            bearish_score += 1

            reasons.append(
                "السعر قريب من منطقة مقاومة"
            )



        # ==========================
        # ATR Volatility
        # ==========================


        if atr > 0:

            if volatility > atr:

                reasons.append(
                    "حركة السوق قوية"
                )

            else:

                reasons.append(
                    "حركة السوق هادئة"
                )



        # ==========================
        # Final Signal
        # ==========================


        if bullish_score > bearish_score:

            signal = "BUY"


        elif bearish_score > bullish_score:

            signal = "SELL"


        else:

            signal = "WAIT"



        total_score = (

            bullish_score +

            bearish_score

        )


        if total_score > 0:

            confidence = round(

                (

                    max(
                        bullish_score,
                        bearish_score
                    )

                    /

                    total_score

                ) * 100,

                2

            )


        else:

            confidence = 0



        return {

            "symbol": symbol,

            "market": market,

            "interval": interval,

            "price": price,


            # Indicators

            "ema": ema,

            "sma": sma,

            "rsi": rsi,

            "macd": macd,

            "trend_strength": trend_strength,

            "volatility": volatility,

            "atr": atr,

            "momentum": momentum,


            # Volume

            "volume_average": volume_average,

            "volume_ratio": volume_ratio,


            # Price

            "price_change": price_change,


            # Levels

            "support": support,

            "resistance": resistance,


            # Market

            "market_state": market_state,


            # Decision

            "signal": signal,

            "confidence": confidence,


            "bullish": (

                bullish_score >

                bearish_score

            ),


            "bearish": (

                bearish_score >

                bullish_score

            ),


            "bullish_score": bullish_score,

            "bearish_score": bearish_score,


            "analysis_reasons": reasons,


            "candles": candles

        }




    # ==========================
    # Market Condition
    # ==========================

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
