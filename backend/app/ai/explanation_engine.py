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
                f"تحليل مضارب: {direction}",

                "message":
                self.trader_message(
                    direction,
                    confidence,
                    reasons
                ),

                "risk":
                risk

            }


        if user_type == "investor":

            return {

                "title":
                f"تحليل مستثمر: {direction}",

                "message":
                self.investor_message(
                    direction,
                    confidence,
                    reasons
                ),

                "risk":
                risk

            }


        if user_type == "company":

            return {

                "title":
                "تقرير تحليل السوق",

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
            "Unknown user type"

        }



    def trader_message(
        self,
        direction,
        confidence,
        reasons
    ):

        return (
            f"الاتجاه الحالي: {direction}\n"
            f"قوة التحليل: {confidence}%\n"
            f"العوامل المؤثرة: "
            + ", ".join(reasons)
        )



    def investor_message(
        self,
        direction,
        confidence,
        reasons
    ):

        return (
            f"الاتجاه المتوقع على المدى الأوسع: {direction}\n"
            f"درجة الثقة: {confidence}%\n"
            f"يعتمد القرار على: "
            + ", ".join(reasons)
        )



    def company_message(
        self,
        analysis
    ):

        return (
            f"اتجاه السوق: "
            f"{analysis.get('direction')}\n"
            f"الثقة: "
            f"{analysis.get('confidence')}%\n"
            f"حالة السوق: "
            f"{analysis.get('market',{}).get('market_state','UNKNOWN')}"
        )
