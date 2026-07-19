class LiquidityEngine:


    def __init__(self):

        self.equal_level_threshold = 0.3

        self.sweep_window = 5

        self.volume_multiplier = 1.5



    # ==================================================
    # MAIN ANALYSIS
    # ==================================================

    def analyze(
        self,
        candles=[]
    ):


        if not candles or len(candles) < 30:

            return {

                "liquidity_strength": 0,

                "bullish": False,

                "bearish": False,

                "confidence": 0,

                "liquidity_zone": "UNKNOWN",

                "sweep": False,

                "fake_breakout": False,

                "buy_liquidity": 0,

                "sell_liquidity": 0,

                "reversal_probability": 0,

                "reasons": []

            }



        highs = [
            c.get("high",0)
            for c in candles
        ]


        lows = [
            c.get("low",0)
            for c in candles
        ]


        closes = [
            c.get("close",0)
            for c in candles
        ]


        volumes = [
            c.get("volume",0)
            for c in candles
        ]



        current_price = closes[-1]

        reasons = []



        bullish = False

        bearish = False

        sweep = False

        fake_breakout = False



        liquidity_strength = 0


        buy_liquidity = 0

        sell_liquidity = 0



        # ==========================
        # Liquidity Pools
        # ==========================


        recent_highs = highs[-20:-1]

        recent_lows = lows[-20:-1]



        high_pool = max(
            recent_highs
        )


        low_pool = min(
            recent_lows
        )



        high_distance = (

            abs(
                high_pool - current_price
            )
            /
            current_price

        ) * 100



        low_distance = (

            abs(
                current_price - low_pool
            )
            /
            current_price

        ) * 100



        if low_distance < 1:

            buy_liquidity += 40

            liquidity_strength += 20

            reasons.append(
                "السعر قريب من Buy Liquidity Pool"
            )



        if high_distance < 1:

            sell_liquidity += 40

            liquidity_strength += 20

            reasons.append(
                "السعر قريب من Sell Liquidity Pool"
            )



        # ==========================
        # Equal Highs / Equal Lows
        # ==========================


        if self.detect_equal_lows(lows):

            buy_liquidity += 20

            liquidity_strength += 10

            reasons.append(
                "وجود Equal Lows تجمع سيولة شراء"
            )



        if self.detect_equal_highs(highs):

            sell_liquidity += 20

            liquidity_strength += 10

            reasons.append(
                "وجود Equal Highs تجمع سيولة بيع"
            )



        # ==========================
        # Liquidity Sweep Detection
        # ==========================


        last = candles[-1]


        previous_lows = lows[
            -self.sweep_window-1:-1
        ]


        previous_highs = highs[
            -self.sweep_window-1:-1
        ]



        if last.get(
            "low",
            0
        ) < min(previous_lows):


            sweep = True

            bullish = True

            buy_liquidity += 30

            liquidity_strength += 30

            reasons.append(
                "Liquidity Sweep أسفل القيعان مع احتمال انعكاس صاعد"
            )



        if last.get(
            "high",
            0
        ) > max(previous_highs):


            sweep = True

            bearish = True

            sell_liquidity += 30

            liquidity_strength += 30

            reasons.append(
                "Liquidity Sweep فوق القمم مع احتمال انعكاس هابط"
            )



        # ==========================
        # Fake Breakout Detection
        # ==========================


        if sweep:


            if bullish and current_price < high_pool:

                fake_breakout = True

                reasons.append(
                    "احتمال Fake Breakdown"
                )


            elif bearish and current_price > low_pool:

                fake_breakout = True

                reasons.append(
                    "احتمال Fake Breakout"
                )



        # ==========================
        # Volume Confirmation
        # ==========================


        average_volume = sum(
            volumes[:-1]
        ) / len(
            volumes[:-1]
        )


        if volumes[-1] > (
            average_volume *
            self.volume_multiplier
        ):

            liquidity_strength += 20

            reasons.append(
                "حجم قوي يؤكد حركة السيولة"
            )



        # ==========================
        # Reversal Probability
        # ==========================


        reversal_probability = 0


        if sweep:

            reversal_probability += 40


        if liquidity_strength >= 60:

            reversal_probability += 30


        if volumes[-1] > average_volume:

            reversal_probability += 20


        if fake_breakout:

            reversal_probability += 10



        reversal_probability = min(
            reversal_probability,
            100
        )



        # ==========================
        # Final Confidence
        # ==========================


        confidence = min(
            liquidity_strength,
            100
        )



        if confidence >= 70:

            zone = "STRONG"


        elif confidence >= 40:

            zone = "MEDIUM"


        else:

            zone = "WEAK"



        # ==========================
        # Final Return
        # ==========================


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


            "fake_breakout":
            fake_breakout,


            "buy_liquidity":
            buy_liquidity,


            "sell_liquidity":
            sell_liquidity,


            "reversal_probability":
            reversal_probability,


            "confidence":
            confidence,


            "reasons":
            reasons

        }



    # ==================================================
    # Equal Lows Detection
    # ==================================================

    def detect_equal_lows(
        self,
        lows
    ):


        if len(lows) < 5:

            return False


        recent = lows[-10:]


        for i in range(len(recent)-1):

            diff = abs(
                recent[i]
                -
                recent[i+1]
            )


            avg = (
                recent[i]
                +
                recent[i+1]
            ) / 2


            if avg > 0 and (

                diff / avg * 100

            ) < self.equal_level_threshold:

                return True


        return False



    # ==================================================
    # Equal Highs Detection
    # ==================================================

    def detect_equal_highs(
        self,
        highs
    ):


        if len(highs) < 5:

            return False


        recent = highs[-10:]


        for i in range(len(recent)-1):

            diff = abs(
                recent[i]
                -
                recent[i+1]
            )


            avg = (
                recent[i]
                +
                recent[i+1]
            ) / 2


            if avg > 0 and (

                diff / avg * 100

            ) < self.equal_level_threshold:

                return True


        return False
