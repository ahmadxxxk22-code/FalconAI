import math


class IndicatorEngine:


    # ==========================
    # EMA
    # ==========================
    def ema(
        self,
        prices,
        period=20
    ):

        if not prices:
            return 0

        if len(prices) < period:
            return round(
                prices[-1],
                2
            )

        multiplier = 2 / (period + 1)

        ema = sum(
            prices[:period]
        ) / period

        for price in prices[period:]:

            ema = (
                (price - ema)
                * multiplier
                + ema
            )

        return round(
            ema,
            2
        )



    # ==========================
    # SMA
    # ==========================
    def sma(
        self,
        prices,
        period=20
    ):

        if not prices:
            return 0

        if len(prices) < period:
            return round(
                prices[-1],
                2
            )

        return round(
            sum(
                prices[-period:]
            ) / period,
            2
        )



    # ==========================
    # RSI
    # ==========================
    def rsi(
        self,
        prices,
        period=14
    ):

        if len(prices) <= period:
            return 50


        gains = []
        losses = []


        for i in range(
            1,
            len(prices)
        ):

            diff = (
                prices[i]
                -
                prices[i - 1]
            )

            if diff >= 0:

                gains.append(
                    diff
                )

                losses.append(
                    0
                )

            else:

                gains.append(
                    0
                )

                losses.append(
                    abs(diff)
                )


        avg_gain = (
            sum(
                gains[-period:]
            )
            /
            period
        )


        avg_loss = (
            sum(
                losses[-period:]
            )
            /
            period
        )


        if avg_loss == 0:
            return 100


        rs = (
            avg_gain
            /
            avg_loss
        )


        value = (
            100
            -
            (
                100
                /
                (
                    1 + rs
                )
            )
        )


        return round(
            value,
            2
        )



    # ==========================
    # MACD
    # ==========================
    def macd(
        self,
        prices
    ):

        ema12 = self.ema(
            prices,
            12
        )

        ema26 = self.ema(
            prices,
            26
        )


        return round(
            ema12 - ema26,
            4
        )



    # ==========================
    # Trend Strength
    # ==========================
    def trend_strength(
        self,
        prices,
        period=20
    ):

        if len(prices) < period:
            return 0


        first = prices[-period]

        last = prices[-1]


        if first == 0:
            return 0


        trend = (
            (
                last - first
            )
            /
            first
        ) * 100


        return round(
            trend,
            2
        )



    # ==========================
    # Volatility
    # ==========================
    def volatility(
        self,
        prices
    ):

        if not prices:
            return 0


        avg = (
            sum(prices)
            /
            len(prices)
        )


        variance = (
            sum(
                (
                    x - avg
                ) ** 2
                for x in prices
            )
            /
            len(prices)
        )


        return round(
            math.sqrt(
                variance
            ),
            4
        )



    # ==========================
    # ATR
    # ==========================
    def atr(
        self,
        candles,
        period=14
    ):

        if len(candles) < period + 1:
            return 0


        trs = []


        for i in range(
            1,
            len(candles)
        ):

            high = candles[i]["high"]

            low = candles[i]["low"]

            prev_close = candles[i - 1]["close"]


            tr = max(
                high - low,
                abs(
                    high - prev_close
                ),
                abs(
                    low - prev_close
                )
            )


            trs.append(
                tr
            )


        return round(
            sum(
                trs[-period:]
            )
            /
            period,
            4
        )



    # ==========================
    # Momentum
    # ==========================
    def momentum(
        self,
        prices,
        period=10
    ):

        if len(prices) <= period:
            return 0


        return round(
            prices[-1]
            -
            prices[-period],
            4
        )



    # ==========================
    # ADX
    # ==========================
    def adx(
        self,
        candles,
        period=14
    ):

        if len(candles) < period + 1:
            return 0


        plus_dm = []
        minus_dm = []
        tr_list = []


        for i in range(
            1,
            len(candles)
        ):

            high = candles[i]["high"]
            low = candles[i]["low"]

            prev_high = candles[i-1]["high"]
            prev_low = candles[i-1]["low"]

            prev_close = candles[i-1]["close"]


            up_move = (
                high - prev_high
            )

            down_move = (
                prev_low - low
            )


            plus_dm.append(
                up_move
                if up_move > down_move and up_move > 0
                else 0
            )

            minus_dm.append(
                down_move
                if down_move > up_move and down_move > 0
                else 0
            )


            tr_list.append(
                max(
                    high - low,
                    abs(high - prev_close),
                    abs(low - prev_close)
                )
            )


        atr = (
            sum(
                tr_list[-period:]
            )
            /
            period
        )


        if atr == 0:
            return 0


        plus_di = (
            sum(
                plus_dm[-period:]
            )
            /
            atr
        )


        minus_di = (
            sum(
                minus_dm[-period:]
            )
            /
            atr
        )


        if plus_di + minus_di == 0:
            return 0


        dx = (
            abs(
                plus_di - minus_di
            )
            /
            (
                plus_di
                +
                minus_di
            )
        ) * 100


        return round(
            dx,
            2
        )



    # ==========================
    # Bollinger Bands
    # ==========================
    def bollinger_bands(
        self,
        prices,
        period=20,
        deviation=2
    ):

        if len(prices) < period:
            price = prices[-1]

            return {
                "upper": price,
                "middle": price,
                "lower": price
            }


        middle = (
            sum(
                prices[-period:]
            )
            /
            period
        )


        variance = (
            sum(
                (
                    x - middle
                ) ** 2
                for x in prices[-period:]
            )
            /
            period
        )


        std = math.sqrt(
            variance
        )


        return {

            "upper": round(
                middle + deviation * std,
                4
            ),

            "middle": round(
                middle,
                4
            ),

            "lower": round(
                middle - deviation * std,
                4
            )

        }


    # ==========================
    # SuperTrend
    # ==========================
    def supertrend(
        self,
        candles,
        period=10,
        multiplier=3
    ):

        if len(candles) < period + 1:
            return {
                "trend": "UNKNOWN",
                "value": 0
            }


        atr = self.atr(
            candles,
            period
        )


        close = candles[-1]["close"]

        high = candles[-1]["high"]

        low = candles[-1]["low"]


        hl2 = (
            high + low
        ) / 2


        upper = (
            hl2
            +
            multiplier * atr
        )


        lower = (
            hl2
            -
            multiplier * atr
        )


        if close > upper:

            trend = "BULLISH"

            value = lower


        elif close < lower:

            trend = "BEARISH"

            value = upper


        else:

            trend = "NEUTRAL"

            value = hl2


        return {

            "trend": trend,

            "value": round(
                value,
                4
            ),

            "atr": atr

        }



    # ==========================
    # VWAP
    # ==========================
    def vwap(
        self,
        candles
    ):

        if not candles:
            return 0


        total_volume = 0

        total_value = 0


        for candle in candles:

            price = (
                candle["high"]
                +
                candle["low"]
                +
                candle["close"]
            ) / 3


            volume = candle["volume"]


            total_value += (
                price * volume
            )


            total_volume += volume


        if total_volume == 0:
            return 0


        return round(
            total_value /
            total_volume,
            4
        )



    # ==========================
    # Ichimoku Cloud
    # ==========================
    def ichimoku(
        self,
        candles
    ):

        if len(candles) < 52:

            return {

                "conversion": 0,

                "base": 0,

                "span_a": 0,

                "span_b": 0

            }


        highs = [
            c["high"]
            for c in candles
        ]

        lows = [
            c["low"]
            for c in candles
        ]


        conversion = (

            max(
                highs[-9:]
            )
            +
            min(
                lows[-9:]
            )

        ) / 2


        base = (

            max(
                highs[-26:]
            )
            +
            min(
                lows[-26:]
            )

        ) / 2


        span_a = (

            conversion
            +
            base

        ) / 2


        span_b = (

            max(
                highs[-52:]
            )
            +
            min(
                lows[-52:]
            )

        ) / 2


        return {

            "conversion": round(
                conversion,
                4
            ),

            "base": round(
                base,
                4
            ),

            "span_a": round(
                span_a,
                4
            ),

            "span_b": round(
                span_b,
                4
            )

        }



    # ==========================
    # Stochastic RSI
    # ==========================
    def stochastic_rsi(
        self,
        prices,
        period=14
    ):

        if len(prices) < period:

            return 50


        rsi_values = []


        for i in range(
            period,
            len(prices)
        ):

            rsi_values.append(

                self.rsi(
                    prices[:i+1],
                    period
                )

            )


        if len(rsi_values) < period:

            return 50


        current = rsi_values[-1]

        highest = max(
            rsi_values[-period:]
        )

        lowest = min(
            rsi_values[-period:]
        )


        if highest == lowest:
            return 50


        value = (

            (
                current - lowest
            )
            /
            (
                highest - lowest
            )

        ) * 100


        return round(
            value,
            2
        )



    # ==========================
    # CCI
    # ==========================
    def cci(
        self,
        candles,
        period=20
    ):

        if len(candles) < period:
            return 0


        typical = [

            (
                c["high"]
                +
                c["low"]
                +
                c["close"]

            ) / 3

            for c in candles[-period:]

        ]


        average = (
            sum(typical)
            /
            period
        )


        mean_deviation = (

            sum(
                abs(
                    x - average
                )
                for x in typical
            )

            /
            period

        )


        if mean_deviation == 0:
            return 0


        return round(

            (
                typical[-1]
                -
                average
            )
            /
            (
                0.015
                *
                mean_deviation
            ),

            2

        )



    # ==========================
    # Money Flow Index MFI
    # ==========================
    def mfi(
        self,
        candles,
        period=14
    ):

        if len(candles) < period + 1:
            return 50


        positive = 0

        negative = 0


        for i in range(
            -period,
            0
        ):

            current = candles[i]

            previous = candles[i-1]


            current_price = (

                current["high"]
                +
                current["low"]
                +
                current["close"]

            ) / 3


            previous_price = (

                previous["high"]
                +
                previous["low"]
                +
                previous["close"]

            ) / 3


            flow = (
                current_price
                *
                current["volume"]
            )


            if current_price > previous_price:

                positive += flow

            else:

                negative += flow


        if negative == 0:
            return 100


        ratio = positive / negative


        return round(
            100 -
            (
                100 /
                (1 + ratio)
            ),
            2
        )



    # ==========================
    # OBV
    # ==========================
    def obv(
        self,
        candles
    ):

        if len(candles) < 2:
            return 0


        value = 0


        for i in range(
            1,
            len(candles)
        ):

            current = candles[i]

            previous = candles[i-1]


            if current["close"] > previous["close"]:

                value += current["volume"]


            elif current["close"] < previous["close"]:

                value -= current["volume"]


        return round(
            value,
            2
        )



    # ==========================
    # Chaikin Money Flow CMF
    # ==========================
    def cmf(
        self,
        candles,
        period=20
    ):

        if len(candles) < period:
            return 0


        money_flow = 0

        volume = 0


        for candle in candles[-period:]:

            high = candle["high"]

            low = candle["low"]

            close = candle["close"]

            vol = candle["volume"]


            if high == low:
                multiplier = 0

            else:

                multiplier = (

                    (
                        (close - low)
                        -
                        (high - close)
                    )
                    /
                    (high - low)

                )


            money_flow += (
                multiplier * vol
            )

            volume += vol


        if volume == 0:
            return 0


        return round(
            money_flow / volume,
            4
        )



    # ==========================
    # Donchian Channel
    # ==========================
    def donchian_channel(
        self,
        candles,
        period=20
    ):

        if len(candles) < period:
            return {

                "upper": 0,

                "lower": 0,

                "middle": 0

            }


        highs = [
            c["high"]
            for c in candles[-period:]
        ]


        lows = [
            c["low"]
            for c in candles[-period:]
        ]


        upper = max(highs)

        lower = min(lows)


        return {

            "upper": round(
                upper,
                4
            ),

            "lower": round(
                lower,
                4
            ),

            "middle": round(
                (
                    upper + lower
                ) / 2,
                4
            )

        }



    # ==========================
    # Keltner Channel
    # ==========================
    def keltner_channel(
        self,
        prices,
        candles,
        period=20,
        multiplier=2
    ):

        if len(prices) < period:
            price = prices[-1]

            return {

                "upper": price,

                "middle": price,

                "lower": price

            }


        middle = self.ema(
            prices,
            period
        )


        atr = self.atr(
            candles,
            period
        )


        return {

            "upper": round(
                middle + multiplier * atr,
                4
            ),

            "middle": round(
                middle,
                4
            ),

            "lower": round(
                middle - multiplier * atr,
                4
            )

        }



    # ==========================
    # Parabolic SAR
    # ==========================
    def parabolic_sar(
        self,
        candles,
        step=0.02,
        max_step=0.2
    ):

        if len(candles) < 2:
            return 0


        sar = candles[0]["low"]

        ep = candles[0]["high"]

        af = step


        bullish = True


        for candle in candles[1:]:

            if bullish:

                sar = sar + af * (
                    ep - sar
                )

                if candle["low"] < sar:

                    bullish = False

                    sar = ep

                    ep = candle["low"]

                    af = step

                elif candle["high"] > ep:

                    ep = candle["high"]

                    af = min(
                        af + step,
                        max_step
                    )


            else:

                sar = sar + af * (
                    ep - sar
                )

                if candle["high"] > sar:

                    bullish = True

                    sar = ep

                    ep = candle["high"]

                    af = step

                elif candle["low"] < ep:

                    ep = candle["low"]

                    af = min(
                        af + step,
                        max_step
                    )


        return round(
            sar,
            4
        )



    # ==========================
    # Aroon
    # ==========================
    def aroon(
        self,
        candles,
        period=25
    ):

        if len(candles) < period:
            return {

                "up": 0,

                "down": 0

            }


        section = candles[-period:]


        highs = [
            c["high"]
            for c in section
        ]

        lows = [
            c["low"]
            for c in section
        ]


        high_index = (
            len(highs)
            -
            1
            -
            highs.index(
                max(highs)
            )
        )


        low_index = (
            len(lows)
            -
            1
            -
            lows.index(
                min(lows)
            )
        )


        return {

            "up": round(
                (
                    (
                        period - high_index
                    )
                    /
                    period
                )
                * 100,
                2
            ),

            "down": round(
                (
                    (
                        period - low_index
                    )
                    /
                    period
                )
                * 100,
                2
            )

        }



    # ==========================
    # Williams %R
    # ==========================
    def williams_r(
        self,
        candles,
        period=14
    ):

        if len(candles) < period:
            return -50


        section = candles[-period:]


        high = max(
            c["high"]
            for c in section
        )


        low = min(
            c["low"]
            for c in section
        )


        close = candles[-1]["close"]


        if high == low:
            return -50


        return round(

            (
                (
                    high - close
                )
                /
                (
                    high - low
                )

            )
            * -100,

            2

        )



    # ==========================
    # ROC
    # ==========================
    def roc(
        self,
        prices,
        period=12
    ):

        if len(prices) <= period:
            return 0


        previous = prices[-period]

        current = prices[-1]


        if previous == 0:
            return 0


        return round(

            (
                (
                    current - previous
                )
                /
                previous

            )
            * 100,

            2

        )



    # ==========================
    # Linear Regression Trend
    # ==========================
    def linear_regression_trend(
        self,
        prices,
        period=50
    ):

        if len(prices) < period:
            return 0


        values = prices[-period:]


        x = list(
            range(period)
        )


        x_mean = sum(x) / period

        y_mean = sum(values) / period


        numerator = sum(

            (
                x[i] - x_mean
            )
            *
            (
                values[i] - y_mean
            )

            for i in range(period)

        )


        denominator = sum(

            (
                x[i] - x_mean
            ) ** 2

            for i in range(period)

        )


        if denominator == 0:
            return 0


        slope = (
            numerator
            /
            denominator
        )


        return round(
            slope,
            6
        )



import math


class IndicatorEngine:


    # ==========================
    # EMA
    # ==========================
    def ema(self, prices, period=20):

        if not prices:
            return 0

        if len(prices) < period:
            return round(prices[-1], 2)

        multiplier = 2 / (period + 1)

        ema = sum(prices[:period]) / period

        for price in prices[period:]:

            ema = (price - ema) * multiplier + ema

        return round(ema, 2)



    # ==========================
    # SMA
    # ==========================
    def sma(self, prices, period=20):

        if not prices:
            return 0

        if len(prices) < period:
            return round(prices[-1], 2)

        return round(
            sum(prices[-period:]) / period,
            2
        )



    # ==========================
    # RSI
    # ==========================
    def rsi(self, prices, period=14):

        if len(prices) <= period:
            return 50

        gains = []
        losses = []

        for i in range(1, len(prices)):

            diff = prices[i] - prices[i - 1]

            if diff >= 0:

                gains.append(diff)
                losses.append(0)

            else:

                gains.append(0)
                losses.append(abs(diff))


        avg_gain = sum(gains[-period:]) / period

        avg_loss = sum(losses[-period:]) / period


        if avg_loss == 0:
            return 100


        rs = avg_gain / avg_loss

        value = 100 - (100 / (1 + rs))

        return round(value, 2)



    # ==========================
    # MACD
    # ==========================
    def macd(self, prices):

        ema12 = self.ema(
            prices,
            12
        )

        ema26 = self.ema(
            prices,
            26
        )

        return round(
            ema12 - ema26,
            2
        )



    # ==========================
    # Trend Strength
    # ==========================
    def trend_strength(self, prices):

        if len(prices) < 20:
            return 0


        first = prices[-20]

        last = prices[-1]


        if first == 0:
            return 0


        value = ((last - first) / first) * 100


        return round(
            value,
            2
        )



    # ==========================
    # Volatility
    # ==========================
    def volatility(self, prices):

        if not prices:
            return 0


        avg = sum(prices) / len(prices)


        variance = sum(

            (x - avg) ** 2

            for x in prices

        ) / len(prices)


        return round(
            math.sqrt(variance),
            2
        )



    # ==========================
    # ATR
    # ==========================
    def atr(self, candles, period=14):

        if len(candles) < period + 1:
            return 0


        trs = []


        for i in range(1, len(candles)):

            high = candles[i]["high"]

            low = candles[i]["low"]

            prev_close = candles[i-1]["close"]


            tr = max(

                high - low,

                abs(high - prev_close),

                abs(low - prev_close)

            )


            trs.append(tr)


        return round(

            sum(trs[-period:]) / period,

            4

        )



    # ==========================
    # Momentum
    # ==========================
    def momentum(self, prices, period=10):

        if len(prices) <= period:
            return 0


        return round(

            prices[-1] - prices[-period],

            4

        )



    # ==========================
    # Volume Average
    # ==========================
    def volume_average(self, volumes, period=20):

        if not volumes:
            return 0

        if len(volumes) < period:

            return round(
                sum(volumes) / len(volumes),
                2
            )


        return round(

            sum(volumes[-period:]) / period,

            2

        )



    # ==========================
    # Volume Ratio
    # ==========================
    def volume_ratio(self, volumes, period=20):

        if not volumes:
            return 0


        average = self.volume_average(
            volumes,
            period
        )


        if average == 0:
            return 0


        return round(

            volumes[-1] / average,

            2

        )



    # ==========================
    # Price Change %
    # ==========================
    def price_change(self, prices, period=1):

        if len(prices) <= period:
            return 0


        old = prices[-period-1]

        current = prices[-1]


        if old == 0:
            return 0


        change = (

            (current - old)

            / old

        ) * 100


        return round(
            change,
            2
        )



    # ==========================
    # Support Resistance Detection
    # ==========================
    def support_resistance_detection(
        self,
        prices,
        window=20
    ):

        if len(prices) < window:

            return {

                "support": None,

                "resistance": None

            }


        recent = prices[-window:]


        support = min(recent)

        resistance = max(recent)


        return {

            "support": round(
                support,
                2
            ),

            "resistance": round(
                resistance,
                2
            )

        }
