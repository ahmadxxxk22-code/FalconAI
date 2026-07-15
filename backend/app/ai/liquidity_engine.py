class LiquidityEngine:


    def __init__(self):

        pass



    def analyze(
        self,
        candles=[]
    ):


        if not candles or len(candles) < 20:

            return {

                "liquidity_strength": 0,

                "bullish": False,

                "bearish": False,

                "confidence": 0,

                "liquidity_zone": "UNKNOWN",

                "sweep": False,

                "reasons": []

            }



        highs = []

        lows = []

        volumes = []



        for candle in candles:

            highs.append(
                candle.get(
                    "high",
                    0
                )
            )

            lows.append(
                candle.get(
                    "low",
                    0
                )
            )

            volumes.append(
                candle.get(
                    "volume",
                    0
                )
            )



        current_price = candles[-1].get(
            "close",
            0
        )



        highest = max(
            highs[:-1]
        )


        lowest = min(
            lows[:-1]
        )



        average_volume = sum(
            volumes[:-1]
        ) / len(
            volumes[:-1]
        )



        current_volume = volumes[-1]



        bullish = False

        bearish = False

        sweep = False

        reasons = []



        distance_high = (

            abs(
                highest - current_price
            )
            /
            current_price

        ) * 100



        distance_low = (

            abs(
                current_price - lowest
            )
            /
            current_price

        ) * 100



        liquidity_strength = 0



        # اقتراب من سيولة الشراء

        if distance_low < 1:

            liquidity_strength += 40

            reasons.append(
                "السعر قريب من منطقة سيولة سفلية"
            )



        # اقتراب من سيولة البيع

        if distance_high < 1:

            liquidity_strength += 40

            reasons.append(
                "السعر قريب من منطقة سيولة علوية"
            )



        # كشف سحب السيولة

        last_candle = candles[-1]

        previous_low = min(
            lows[-5:-1]
        )

        previous_high = max(
            highs[-5:-1]
        )



        if last_candle.get(
            "low",
            0
        ) < previous_low:


            sweep = True

            bullish = True

            liquidity_strength += 30

            reasons.append(
                "تم سحب سيولة أسفل السعر مع احتمال انعكاس"
            )



        if last_candle.get(
            "high",
            0
        ) > previous_high:


            sweep = True

            bearish = True

            liquidity_strength += 30

            reasons.append(
                "تم سحب سيولة أعلى السعر مع احتمال هبوط"
            )



        if current_volume > average_volume * 1.5:

            liquidity_strength += 20

            reasons.append(
                "حجم تداول مرتفع داخل منطقة السيولة"
            )



        confidence = min(
            liquidity_strength,
            100
        )



        if confidence >= 60:

            zone = "STRONG"

        elif confidence >= 30:

            zone = "MEDIUM"

        else:

            zone = "WEAK"



        return {


            "liquidity_strength":

            liquidity_strength,


            "liquidity_zone":

            zone,


            "bullish":

            bullish,


            "bearish":

            bearish,


            "sweep":

            sweep,


            "confidence":

            confidence,


            "reasons":

            reasons

      }
