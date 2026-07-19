class OrderBlocksEngine:


    def __init__(self):

        self.minimum_candles = 30

        self.max_blocks_return = 5

        self.volume_multiplier = 1.5



    # ==================================================
    # MAIN ANALYSIS
    # ==================================================

    def analyze(
        self,
        candles
    ):


        if not candles or len(candles) < self.minimum_candles:

            return {

                "bullish_blocks": [],

                "bearish_blocks": [],

                "nearest_block": None,

                "active_block": None,

                "bos": False,

                "confidence": 0,

                "bullish": False,

                "bearish": False,

                "reasons": []

            }



        bullish_blocks = []

        bearish_blocks = []

        reasons = []



        current_price = candles[-1].get(
            "close",
            0
        )



        volumes = [

            c.get(
                "volume",
                0
            )

            for c in candles

        ]



        average_volume = sum(
            volumes
        ) / len(
            volumes
        )



        # ==================================================
        # Detect Blocks
        # ==================================================


        for i in range(
            2,
            len(candles)-2
        ):


            previous = candles[i-1]

            current = candles[i]

            next_candle = candles[i+1]



            body = abs(
                current["close"]
                -
                current["open"]
            )


            candle_range = (

                current["high"]
                -
                current["low"]

            )



            if candle_range == 0:

                continue



            body_strength = (

                body /
                candle_range

            ) * 100



            volume_power = (

                current.get(
                    "volume",
                    0
                )

                /

                average_volume

            )



            # ==========================
            # Bullish Order Block
            # ==========================


            if (

                current["close"] < current["open"]

                and

                next_candle["close"] > current["high"]

            ):


                strength = (

                    abs(
                        next_candle["close"]
                        -
                        current["open"]
                    )

                    /

                    current["open"]

                ) * 100



                if volume_power >= self.volume_multiplier:

                    strength += 10

                    reasons.append(
                        "Bullish Order Block مع حجم قوي"
                    )



                if body_strength > 50:

                    strength += 5



                bullish_blocks.append({

                    "type":
                    "BULLISH",


                    "low":
                    current["low"],


                    "high":
                    current["high"],


                    "index":
                    i,


                    "strength":
                    round(
                        min(strength,100),
                        2
                    ),


                    "mitigated":
                    self.check_mitigation(
                        candles,
                        i,
                        current_price
                    )

                })



            # ==========================
            # Bearish Order Block
            # ==========================


            if (

                current["close"] > current["open"]

                and

                next_candle["close"] < current["low"]

            ):


                strength = (

                    abs(
                        current["open"]
                        -
                        next_candle["close"]
                    )

                    /

                    current["open"]

                ) * 100



                if volume_power >= self.volume_multiplier:

                    strength += 10

                    reasons.append(
                        "Bearish Order Block مع حجم قوي"
                    )



                if body_strength > 50:

                    strength += 5



                bearish_blocks.append({

                    "type":
                    "BEARISH",


                    "low":
                    current["low"],


                    "high":
                    current["high"],


                    "index":
                    i,


                    "strength":
                    round(
                        min(strength,100),
                        2
                    ),


                    "mitigated":
                    self.check_mitigation(
                        candles,
                        i,
                        current_price
                    )

                })



        # ==================================================
        # Sort Blocks
        # ==================================================


        bullish_blocks.sort(

            key=lambda x: x["strength"],

            reverse=True

        )


        bearish_blocks.sort(

            key=lambda x: x["strength"],

            reverse=True

        )



        # ==================================================
        # Nearest Active Block
        # ==================================================


        nearest_block = None


        all_blocks = (
            bullish_blocks
            +
            bearish_blocks
        )



        if all_blocks:


            nearest_block = min(

                all_blocks,

                key=lambda block:

                abs(

                    current_price -

                    (
                        block["high"]
                        +
                        block["low"]

                    ) / 2

                )

            )



        # ==================================================
        # Structure Break Detection
        # ==================================================


        bos = False


        recent_high = max(

            [
                c["high"]

                for c in candles[-10:-1]

            ]

        )


        recent_low = min(

            [
                c["low"]

                for c in candles[-10:-1]

            ]

        )



        if current_price > recent_high:

            bos = True

            reasons.append(
                "Break Of Structure صاعد"
            )



        elif current_price < recent_low:

            bos = True

            reasons.append(
                "Break Of Structure هابط"
            )



        # ==================================================
        # Direction
        # ==================================================


        bullish = False

        bearish = False



        if nearest_block:


            if nearest_block["type"] == "BULLISH":

                bullish = True

                reasons.append(
                    "أقرب Order Block صاعد"
                )



            elif nearest_block["type"] == "BEARISH":

                bearish = True

                reasons.append(
                    "أقرب Order Block هابط"
                )



        # ==================================================
        # Confidence
        # ==================================================


        confidence = 0


        if nearest_block:


            confidence = nearest_block["strength"]



            if nearest_block.get(
                "mitigated",
                False
            ):

                confidence -= 20

                reasons.append(
                    "Order Block تم اختباره سابقاً"
                )



        confidence = max(

            min(
                confidence,
                100
            ),

            0

        )



        active_block = None


        for block in all_blocks:


            if (

                block["low"]
                <=
                current_price
                <=
                block["high"]

            ):

                active_block = block

                break



        return {


            "bullish_blocks":

            bullish_blocks[:self.max_blocks_return],



            "bearish_blocks":

            bearish_blocks[:self.max_blocks_return],



            "nearest_block":

            nearest_block,



            "active_block":

            active_block,



            "bos":

            bos,



            "bullish":

            bullish,



            "bearish":

            bearish,



            "confidence":

            round(
                confidence,
                2
            ),



            "reasons":

            reasons

        }



    # ==================================================
    # Mitigation Check
    # ==================================================


    def check_mitigation(

        self,

        candles,

        index,

        current_price

    ):


        block = candles[index]


        for candle in candles[index+1:]:


            if (

                block["low"]
                <=
                candle["close"]
                <=
                block["high"]

            ):

                return True



        return False
