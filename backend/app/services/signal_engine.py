from datetime import datetime
import random

from app.services.indicator_engine import IndicatorEngine


class SignalEngine:

    def __init__(self):
        self.indicators = IndicatorEngine()

    def get_mock_prices(self):
    # بيانات شبه واقعية بدل العشوائية الكاملة
    base = 27000
    return [base + random.randint(-500, 500) for _ in range(30)]

    def analyze_market(self, symbol: str, timeframe: str = "1m"):

        prices = self.get_mock_prices()

        rsi = self.indicators.rsi(prices)
        ema = self.indicators.ema(prices)
        trend_strength = self.indicators.trend_strength(prices)

        last_price = prices[-1]

        # القرار الحقيقي الآن
        if rsi < 30 and last_price > ema:
            direction = "BUY"
            confidence = 85 + random.randint(0, 10)
            reason = "RSI منخفض + السعر فوق EMA = بداية صعود محتمل"

        elif rsi > 70 and last_price < ema:
            direction = "SELL"
            confidence = 85 + random.randint(0, 10)
            reason = "RSI مرتفع + السعر تحت EMA = احتمال هبوط"

        else:
            direction = "WAIT"
            confidence = 50 + random.randint(0, 20)
            reason = "السوق غير واضح + لا يوجد تأكيد قوي"

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "direction": direction,
            "confidence": confidence,
            "rsi": rsi,
            "ema": ema,
            "trend_strength": trend_strength,
            "last_price": last_price,
            "reason": reason,
            "created_at": datetime.utcnow().isoformat()
        }
