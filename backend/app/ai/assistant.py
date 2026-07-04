class FalconAssistant:

    def explain(self, analysis):

        direction = analysis.get("direction", "WAIT")

        confidence = analysis.get("confidence", 0)

        risk = analysis.get("risk", {})

        market = analysis.get("market", {})

        pattern = analysis.get("patterns", {})

        smart = analysis.get("smart_money", {})

        news = analysis.get("news", {})

        fibonacci = analysis.get("fibonacci", {})

        if direction == "BUY":

            title = "إشارة شراء"

        elif direction == "SELL":

            title = "إشارة بيع"

        else:

            title = "انتظار"

        return {

            "title": title,

            "signal": direction,

            "confidence": confidence,

            "summary": self.summary(

                direction,

                confidence

            ),

            "market": market,

            "pattern": pattern,

            "smart_money": smart,

            "news": news,

            "fibonacci": fibonacci,

            "risk": risk,

            "advice": self.advice(

                direction,

                confidence

            )

        }

    def summary(

        self,

        direction,

        confidence

    ):

        return (

            f"FalconAI يرى أن الاتجاه {direction} "

            f"بثقة {confidence}%."

        )

    def advice(

        self,

        direction,

        confidence

    ):

        if direction == "BUY" and confidence >= 80:

            return (

                "الاتجاه صاعد بقوة. "

                "يفضل الدخول مع الالتزام "

                "بوقف الخسارة."

            )

        if direction == "SELL" and confidence >= 80:

            return (

                "الاتجاه هابط بقوة. "

                "يفضل البيع أو تجنب "

                "الشراء حالياً."

            )

        return (

            "يفضل الانتظار حتى "

            "ظهور تأكيدات إضافية."

        )
