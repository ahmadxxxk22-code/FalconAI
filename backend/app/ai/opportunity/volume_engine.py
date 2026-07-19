class VolumeEngine:


    def __init__(self):

        self.spike_multiplier = 2.0

        self.high_volume_multiplier = 1.5

        self.low_volume_multiplier = 0.7



    # ==================================================
    # Helpers
    # ==================================================


    def average(
        self,
        values,
        length
    ):

        if len(values) < length:

            return 0


        return sum(
            values[-length:]
        ) / length



    def price_direction(
        self,
        closes,
        length=5
    ):


        if len(closes) < length + 1:

            return 0


        return (

            closes[-1]
            -
            closes[-length]

        )



    def detect_divergence(
        self,
        closes,
        volumes
    ):


        if len(closes) < 10:

            return {

                "bullish":False,

                "bearish":False

            }



        price_move = (

            closes[-1]
            -
            closes[-10]

        )


        volume_move = (

            volumes[-1]
            -
            volumes[-10]

        )



        bullish = (

            price_move < 0

            and

            volume_move > 0

        )



        bearish = (

            price_move > 0

            and

            volume_move < 0

        )



        return {

            "bullish":bullish,

            "bearish":bearish

        }



    # ==================================================
    # MAIN ANALYSIS
    # ==================================================


    def analyze(
        self,
        candles
    ):


        if len(candles) < 30:

            return {

                "volume_state":"UNKNOWN",

                "score":0,

                "confidence":0,

                "bullish":False,

                "bearish":False,

                "high_volume":False,

                "low_volume":False,

                "volume_spike":False,

                "climax":False,

                "accumulation":False,

                "distribution":False,

                "divergence":False,

                "reasons":[]

            }



        volumes = [

            c.get(
                "volume",
                0
            )

            for c in candles

        ]


        closes = [

            c.get(
                "close",
                0
            )

            for c in candles

        ]



        current_volume = volumes[-1]



        avg_20 = self.average(

            volumes[:-1],

            20

        )


        avg_50 = self.average(

            volumes[:-1],

            50

        )



        ratio_20 = (

            current_volume /
            avg_20

            if avg_20 > 0

            else 0

        )



        ratio_50 = (

            current_volume /
            avg_50

            if avg_50 > 0

            else 0

        )



        score = 0

        reasons = []



        bullish = False

        bearish = False


        volume_spike = False

        climax = False

        accumulation = False

        distribution = False



        # ==========================
        # Volume Spike
        # ==========================


        if ratio_20 >= self.spike_multiplier:


            score += 30

            volume_spike = True


            reasons.append(
                "انفجار في حجم التداول"
            )


        elif ratio_20 >= self.high_volume_multiplier:


            score += 20


            reasons.append(
                "حجم التداول فوق المتوسط"
            )



        elif ratio_20 <= self.low_volume_multiplier:


            score -= 10


            reasons.append(
                "حجم التداول ضعيف"
            )



        # ==========================
        # Accumulation / Distribution
        # ==========================


        direction = self.price_direction(

            closes

        )



        if current_volume > avg_20:


            if direction > 0:


                score += 15

                accumulation = True

                bullish = True


                reasons.append(
                    "تجميع مع ارتفاع السعر"
                )



            elif direction < 0:


                score -= 15

                distribution = True

                bearish = True


                reasons.append(
                    "تصريف مع هبوط السعر"
            )



        # ==========================
        # Volume Climax
        # ==========================


        last_candle = candles[-1]


        candle_range = (

            last_candle.get(
                "high",
                0
            )

            -

            last_candle.get(
                "low",
                0
            )

        )



        average_range = sum(

            [

                (
                    c.get("high",0)
                    -
                    c.get("low",0)

                )

                for c in candles[-20:]

            ]

        ) / 20



        if (

            ratio_20 >= 2.5

            and

            candle_range > average_range * 1.5

        ):


            climax = True

            score += 20


            reasons.append(
                "Volume Climax: حركة قوية مع حجم استثنائي"
            )



            if last_candle["close"] > last_candle["open"]:

                bullish = True


            else:

                bearish = True



        # ==========================
        # Volume Divergence
        # ==========================


        divergence = self.detect_divergence(

            closes,

            volumes

        )



        if divergence["bullish"]:


            score += 15

            bullish = True


            reasons.append(
                "انحراف حجمي صاعد"
            )



        if divergence["bearish"]:


            score -= 15

            bearish = True


            reasons.append(
                "انحراف حجمي هابط"
            )



        # ==========================
        # Final State
        # ==========================


        if score >= 50:


            state = "EXTREME_BULLISH"

            bullish = True



        elif score >= 25:


            state = "BULLISH_VOLUME"



        elif score <= -25:


            state = "BEARISH_VOLUME"

            bearish = True



        elif score < 0:


            state = "WEAK_VOLUME"



        else:


            state = "NORMAL"



        confidence = min(

            abs(score) * 2,

            100

        )



        return {


            "volume_state":

            state,


            "score":

            score,


            "confidence":

            round(

                confidence,

                2

            ),


            "bullish":

            bullish,


            "bearish":

            bearish,


            "high_volume":

            ratio_20 >= self.high_volume_multiplier,


            "low_volume":

            ratio_20 <= self.low_volume_multiplier,


            "volume_spike":

            volume_spike,


            "climax":

            climax,


            "accumulation":

            accumulation,


            "distribution":

            distribution,


            "divergence":

            divergence["bullish"]
            or
            divergence["bearish"],


            "average_volume_20":

            round(
                avg_20,
                2
            ),


            "average_volume_50":

            round(
                avg_50,
                2
            ),


            "current_volume":

            round(
                current_volume,
                2
            ),


            "ratio_20":

            round(
                ratio_20,
                2
            ),


            "ratio_50":

            round(
                ratio_50,
                2
            ),


            "reasons":

            reasons

        }
