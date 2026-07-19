class SupportResistanceEngine:

    def __init__(
        self,
        window=5,
        tolerance=0.005,
        touch_threshold=2
    ):
        self.window = window
        self.tolerance = tolerance
        self.touch_threshold = touch_threshold

    def analyze(
        self,
        highs,
        lows,
        closes,
        volumes=None
    ):

        if len(highs) < self.window * 4:

            return {
                "supports": [],
                "resistances": [],
                "nearest_support": None,
                "nearest_resistance": None,
                "broken_support": False,
                "broken_resistance": False,
                "support_strength": 0,
                "resistance_strength": 0,
                "reasons": []
            }

        supports = []
        resistances = []
        reasons = []

        current_price = closes[-1]

        # ==========================
        # استخراج الدعوم
        # ==========================

        for i in range(
            self.window,
            len(lows) - self.window
        ):

            level = lows[i]

            area = lows[
                i-self.window:
                i+self.window+1
            ]

            if level == min(area):

                supports.append({
                    "price": level,
                    "index": i
                })

        # ==========================
        # استخراج المقاومات
        # ==========================

        for i in range(
            self.window,
            len(highs) - self.window
        ):

            level = highs[i]

            area = highs[
                i-self.window:
                i+self.window+1
            ]

            if level == max(area):

                resistances.append({
                    "price": level,
                    "index": i
                })



        supports = self.merge_levels(
            supports
        )

        resistances = self.merge_levels(
            resistances
        )

        # ==========================
        # حساب القوة
        # ==========================

        for level in supports:

            touches = sum(
                1 for p in lows
                if abs(
                    p - level["price"]
                ) <= level["price"] * self.tolerance
            )

            level["touches"] = touches

            level["strength"] = min(
                touches * 15,
                100
            )

        for level in resistances:

            touches = sum(
                1 for p in highs
                if abs(
                    p - level["price"]
                ) <= level["price"] * self.tolerance
            )

            level["touches"] = touches

            level["strength"] = min(
                touches * 15,
                100
            )

        supports.sort(
            key=lambda x: x["strength"],
            reverse=True
        )

        resistances.sort(
            key=lambda x: x["strength"],
            reverse=True
        )

        nearest_support = None
        nearest_resistance = None

        support_strength = 0
        resistance_strength = 0

        broken_support = False
        broken_resistance = False



                # ==========================
        # أقرب دعم
        # ==========================

        below = [
            s for s in supports
            if s["price"] <= current_price
        ]

        if below:

            nearest_support = max(
                below,
                key=lambda x: x["price"]
            )

            support_strength = nearest_support["strength"]

            distance = (
                (
                    current_price -
                    nearest_support["price"]
                )
                /
                current_price
            ) * 100

            reasons.append(
                f"أقرب دعم يبعد {distance:.2f}%"
            )

            if current_price < nearest_support["price"]:

                broken_support = True

                reasons.append(
                    "تم كسر أقرب دعم"
                )

        # ==========================
        # أقرب مقاومة
        # ==========================

        above = [
            r for r in resistances
            if r["price"] >= current_price
        ]

        if above:

            nearest_resistance = min(
                above,
                key=lambda x: x["price"]
            )

            resistance_strength = nearest_resistance["strength"]

            distance = (
                (
                    nearest_resistance["price"] -
                    current_price
                )
                /
                current_price
            ) * 100

            reasons.append(
                f"أقرب مقاومة تبعد {distance:.2f}%"
            )

            if current_price > nearest_resistance["price"]:

                broken_resistance = True

                reasons.append(
                    "تم اختراق أقرب مقاومة"
                )

        if nearest_support and nearest_support["strength"] >= 60:

            reasons.append(
                "منطقة دعم قوية"
            )

        if nearest_resistance and nearest_resistance["strength"] >= 60:

            reasons.append(
                "منطقة مقاومة قوية"
            )

        return {
            "supports": supports,
            "resistances": resistances,
            "nearest_support": nearest_support,
            "nearest_resistance": nearest_resistance,
            "broken_support": broken_support,
            "broken_resistance": broken_resistance,
            "support_strength": support_strength,
            "resistance_strength": resistance_strength,
            "reasons": reasons
        } 


    
    # ==========================
    # دمج المستويات المتقاربة
    # ==========================

    def merge_levels(
        self,
        levels
    ):

        if not levels:
            return []

        merged = []

        for level in sorted(
            levels,
            key=lambda x: x["price"]
        ):

            if not merged:

                merged.append(level)

                continue

            previous = merged[-1]

            difference = abs(
                level["price"] -
                previous["price"]
            )

            if difference <= previous["price"] * self.tolerance:

                previous["price"] = (
                    previous["price"] +
                    level["price"]
                ) / 2

            else:

                merged.append(level)

        return merged
