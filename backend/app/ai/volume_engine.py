class VolumeEngine:


    def __init__(self):

        pass



    def analyze(
        self,
        candles=[]
    ):

        if not candles or len(candles) < 20:

            return {

                "volume_strength": 0,

                "bullish": False,

                "bearish": False,

                "confidence": 0,

                "status": "NO_DATA",

                "reasons": []

            }



        volumes = []

        for candle in candles:

            volumes.append(
                candle.get(
                    "volume",
                    0
                )
            )



        current_volume = volumes[-1]



        average_volume = sum(
            volumes[:-1]
        ) / len(
            volumes[:-1]
        )



        if average_volume == 0:

            return {

                "volume_strength": 0,

                "bullish": False,

                "bearish": False,

                "confidence": 0,

                "status": "INVALID",

                "reasons": []

            }



        volume_ratio = round(

            (
                current_volume /
                average_volume
            ) * 100,

            2

        )



        strength = min(

            volume_ratio,

            200

        )



        bullish = False

        bearish = False

        reasons = []



        last_candle = candles[-1]



        open_price = last_candle.get(
            "open",
            0
        )


        close_price = last_candle.get(
            "close",
            0
        )



        if volume_ratio >= 120:


            if close_price > open_price:

                bullish = True

                reasons.append(
                    "حجم شراء قوي مع شمعة صاعدة"
                )


            elif close_price < open_price:

                bearish = True

                reasons.append(
                    "حجم بيع قوي مع شمعة هابطة"
                )


        else:

            reasons.append(
                "الحجم غير قوي حالياً"
            )



        confidence = min(

            int(
                abs(volume_ratio - 100)
            ),

            100

        )



        return {


            "current_volume":

            current_volume,


            "average_volume":

            round(
                average_volume,
                2
            ),


            "volume_ratio":

            volume_ratio,


            "volume_strength":

            strength,


            "bullish":

            bullish,


            "bearish":

            bearish,


            "confidence":

            confidence,


            "status":

            "ACTIVE",


            "reasons":

            reasons

  }
