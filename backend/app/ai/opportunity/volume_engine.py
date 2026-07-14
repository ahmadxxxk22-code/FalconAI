class VolumeEngine:

    def analyze(self, candles):

        if len(candles) < 30:

            return {

                "volume_state": "UNKNOWN",

                "score": 0,

                "high_volume": False,

                "low_volume": False,

                "average_volume": 0,

                "current_volume": 0

            }

        volumes = [

            candle["volume"]

            for candle in candles

        ]

        average_volume = (

            sum(volumes[:-1]) /

            (len(volumes) - 1)

        )

        current_volume = volumes[-1]

        ratio = (

            current_volume /

            average_volume

            if average_volume > 0

            else 0

        )

        score = 0

        high_volume = False

        low_volume = False

        state = "NORMAL"

        if ratio >= 2:

            state = "VERY_HIGH"

            score = 30

            high_volume = True

        elif ratio >= 1.5:

            state = "HIGH"

            score = 20

            high_volume = True

        elif ratio <= 0.7:

            state = "LOW"

            score = -10

            low_volume = True

        return {

            "volume_state": state,

            "score": score,

            "high_volume": high_volume,

            "low_volume": low_volume,

            "average_volume": round(

                average_volume,

                2

            ),

            "current_volume": round(

                current_volume,

                2

            ),

            "ratio": round(

                ratio,

                2

            )

        }
