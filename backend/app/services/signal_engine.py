from datetime import datetime
import random


class SignalEngine:

    def analyze_market(self, symbol: str, timeframe: str = "1m"):
        """
        تحليل السوق (نسخة أولية - لاحقاً نربط AI + Indicators)
        """

        # محاكاة بيانات (لاحقاً نستبدلها ببيانات حقيقية)
        rsi = random.randint(10, 90)
        trend_strength = random.randint(1, 100)

        # قرار بسيط مبدئي
        if rsi < 30 and trend_strength > 60:
            direction = "BUY"
            confidence = random.randint(70, 95)
            reason = "السوق في حالة تشبع بيع + قوة صعود واضحة"

        elif rsi > 70 and trend_strength > 60:
            direction = "SELL"
            confidence = random.randint(70, 95)
            reason = "السوق في حالة تشبع شراء + ضعف محتمل في الصعود"

        else:
            direction = "WAIT"
            confidence = random.randint(40, 60)
            reason = "السوق غير واضح، يفضل الانتظار"

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "direction": direction,
            "confidence": confidence,
            "rsi": rsi,
            "trend_strength": trend_strength,
            "reason": reason,
            "created_at": datetime.utcnow().isoformat()
        }
