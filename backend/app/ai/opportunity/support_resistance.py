class SupportResistanceEngine:


    def __init__(
        self,
        window=5,
        tolerance=0.005
    ):

        self.window = window
        self.tolerance = tolerance



    def analyze(
        self,
        highs,
        lows,
        closes
    ):


        if len(highs) < self.window * 3:

            return {

                "supports": [],

                "resistances": [],

                "nearest_support": None,

                "nearest_resistance": None,

                "reasons": []

            }



        supports = []

        resistances = []

        reasons = []



        # ==========================
        # استخراج الدعوم
        # ==========================

        for i in range(
            self.window,
            len(lows)-self.window
        ):


            low = lows[i]


            zone = lows[
                i-self.window:
                i+self.window+1
            ]


            if low == min(zone):

                supports.append(low)



        # ==========================
        # استخراج المقاومات
        # ==========================


        for i in range(
            self.window,
            len(highs)-self.window
        ):


            high = highs[i]


            zone = highs[
                i-self.window:
                i+self.window+1
            ]


            if high == max(zone):

                resistances.append(high)




        supports = self.merge_levels(
            supports
        )


        resistances = self.merge_levels(
            resistances
        )



        current_price
