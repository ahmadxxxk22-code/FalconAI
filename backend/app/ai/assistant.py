class FalconAssistant:

    def explain(self, analysis: dict):

        signal = analysis.get("signal", "WAIT")
        confidence = analysis.get("confidence", 0)
        reasons = analysis.get("reasons", [])
        risk = analysis.get("risk", {})

        if signal == "BUY":
            title = "إشارة شراء"

        elif signal == "SELL":
            title = "إشارة بيع"

        else:
            title = "انتظار"

        return {

            "title": title,

            "signal": signal,

            "confidence": confidence,

            "summary": f"درجة الثقة {confidence}%",

            "reasons": reasons,

            "risk": risk,

            "advice": self.build_advice(signal, confidence)

        }

    def build_advice(self, signal, confidence):

        if signal == "BUY" and confidence >= 80:
            return "الاتجاه قوي ويمكن التفكير بالدخول مع إدارة جيدة لرأس المال."

        if signal == "SELL" and confidence >= 80:
            return "الاتجاه هابط بقوة، ويجب الانتباه لإدارة المخاطر."

        return "يفضل انتظار تأكيدات إضافية قبل اتخاذ القرار."
