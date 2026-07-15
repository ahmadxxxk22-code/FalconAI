class ExplanationEngine:


    def explain(
        self,
        analysis,
        user_type="trader"
    ):

        direction = analysis.get(
            "direction",
            "WAIT"
        )

        confidence = analysis.get(
            "confidence",
            0
        )

        reasons = analysis.get(
            "decision_reasons",
            []
        )

        risk = analysis.get(
            "risk",
            {}
        )


        if user_type == "trader":

            return {

                "title":
                f"إشارة قصيرة المدى: {direction}",

                "message":
                self.trader_message(
                    direction,
                    confidence,
                    reasons
                ),

                "risk":
                risk

            }


        elif user_type == "investor":

            return {

                "title":
                f"تحليل استثماري: {direction}",

                "message":
                self.investor_message(
                    direction,
                    confidence,
                    reasons
                ),

                "risk":
                risk

            }


        elif user_type == "company":

            return {

                "title":
                "تقرير السوق",

                "message":
                self.company_message(
                    analysis
                ),

                "risk":
                risk

            }


        return {

            "title":
            "Market Analysis",

            "message":
            "No explanation available"

        }



    def trader_message(
        self,
        direction,
        confidence,
        reasons
    ):

        return (
            f"القرار الحالي {direction} "
            f"بثقة {confidence}%."
            f" الأسباب: "
            + ", ".join(reasons)
        )



    def investor_message(
        self,
        direction,
        confidence,
        reasons
    ):

        return (
            f"الاتجاه العام المتوقع "
            f"{direction} "
            f"مع قوة {confidence}%."
            f" يعتمد التحليل على: "
            + ", ".join(reasons)
        )



    def company_message(
        self,
        analysis
    ):

        return {

            "market_direction":
            analysis.get(
                "direction"
            ),

            "confidence":
            analysis.get(
                "confidence"
            ),

            "risk_level":
            analysis.get(
                "risk"
            )

        }
