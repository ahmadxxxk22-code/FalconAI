class OrderBlocksEngine:


    def analyze(
        self,
        candles
    ):


        if len(candles) < 20:

            return {

                "bullish_blocks": [],

                "bearish_blocks": [],

                "nearest_block": None,

                "confidence": 0,

                "reasons": []

            }



        bullish_blocks = []

        bearish_blocks = []

        reasons = []



        for i in range(
            2,
            len(candles) - 2
        ):


            prev = candles[i - 1]

            current = candles[i]

            nxt = candles[i + 1]



            move_up = (
                nxt["close"] -
                current["open"]
            )


            move_down = (
                current["open"] -
                nxt["close"]
            )



            # ==========================
            # Bullish Order Block
            # ==========================


            if (

                current["close"] < current["open"]

                and

                nxt["close"] > current["high"]

                and

                move_up > 0

            ):


                strength = abs(
                    move_up /
                    current["open"]
                ) * 100



                bullish_blocks.append({

                    "low":
                    current["low"],


                    "high":
                    current["high"],


                    "index":
                    i,


                    "strength":
                    round(
                        strength,
                        2
                    )

                })



            # ==========================
            # Bearish Order Block
            # ==========================


            if (

                current["close"] > current["open"]

                and

                nxt["close"] < current["low"]

                and

                move_down > 0

            ):


                strength = abs(
                    move_down /
                    current["open"]
                ) * 100



                bearish_blocks.append({

                    "low":
                    current["low"],


                    "high":
                    current["high"],


                    "index":
                    i,


                    "strength":
                    round(
                        strength,
                        2
                    )

                })




        # ترتيب حسب القوة

        bullish_blocks.sort(
            key=lambda x:x["strength"],
            reverse=True
        )


        bearish_blocks.sort(
            key=lambda x:x["strength"],
            reverse=True
        )



        nearest_block = None



        if bullish_blocks:

            nearest_block = bullish_blocks[0]

            reasons.append(
                "تم اكتشاف Bullish Order Block قوي"
            )



        elif bearish_blocks:

            nearest_block = bearish_blocks[0]

            reasons.append(
                "تم اكتشاف Bearish Order Block قوي"
            )



        confidence = 0



        if nearest_block:

            confidence = min(

                nearest_block["strength"] * 5,

                100

            )



        return {


            "bullish_blocks":
            bullish_blocks[:5],


            "bearish_blocks":
            bearish_blocks[:5],


            "nearest_block":
            nearest_block,


            "confidence":
            round(
                confidence,
                2
            ),


            "reasons":
            reasons

        }
