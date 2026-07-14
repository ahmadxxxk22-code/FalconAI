from math import fabs


class RiskManager:

    def __init__(self):

        self.market_settings = {

            "crypto": {
                "atr_multiplier": 2.0,
                "tp1": 2.0,
                "tp2": 3.5,
                "tp3": 5.0,
                "max_risk": 2.0
            },

            "forex": {
                "atr_multiplier": 1.8,
                "tp1": 1.8,
                "tp2": 3.0,
                "tp3": 4.5,
                "max_risk": 1.5
            },

            "gold": {
                "atr_multiplier": 2.2,
                "tp1": 2.5,
                "tp2": 4.0,
                "tp3": 6.0,
                "max_risk": 1.5
            },

            "oil": {
                "atr_multiplier": 2.4,
                "tp1": 2.5,
                "tp2": 4.5,
                "tp3": 6.5,
                "max_risk": 1.5
            },

            "stocks": {
                "atr_multiplier": 2.0,
                "tp1": 2.5,
                "tp2": 4.0,
                "tp3": 6.0,
                "max_risk": 2.0
            },

            "indices": {
                "atr_multiplier": 2.0,
                "tp1": 2.2,
                "tp2": 3.8,
                "tp3": 5.5,
                "max_risk": 1.5
            }

        }

    def calculate(
        self,
        direction,
        price,
        confidence,
        atr,
        volatility,
        trend_strength,
        market_state,
        smart_money,
        fibonacci,
        market="crypto",
        balance=10000,
        risk_percent=2
    ):

        settings = self.market_settings.get(
            market,
            self.market_settings["crypto"]
        )

        risk_percent = min(
            risk_percent,
            settings["max_risk"]
        )

        risk_amount = balance * (
            risk_percent / 100
        )

        atr = max(
            atr,
            price * 0.003
        )

        multiplier = settings["atr_multiplier"]

        trade_allowed = True
        reasons = []

        if confidence < 60:
            trade_allowed = False
            reasons.append("الثقة أقل من الحد الأدنى")

        if market_state == "SIDEWAYS":
            trade_allowed = False
            reasons.append("السوق عرضي")

        if abs(trend_strength) < 0.5:
            trade_allowed = False
            reasons.append("الاتجاه ضعيف")

        if direction == "WAIT":
            trade_allowed = False
            reasons.append("لا توجد إشارة
                    if direction == "BUY":

            entry = price

            stop_loss = price - (
                atr * multiplier
            )

            take_profit_1 = price + (
                atr * settings["tp1"]
            )

            take_profit_2 = price + (
                atr * settings["tp2"]
            )

            take_profit_3 = price + (
                atr * settings["tp3"]
            )

        elif direction == "SELL":

            entry = price

            stop_loss = price + (
                atr * multiplier
            )

            take_profit_1 = price - (
                atr * settings["tp1"]
            )

            take_profit_2 = price - (
                atr * settings["tp2"]
            )

            take_profit_3 = price - (
                atr * settings["tp3"]
            )

        else:

            entry = None
            stop_loss = None
            take_profit_1 = None
            take_profit_2 = None
            take_profit_3 = None

        if entry is None:

            position_size = 0
            risk_reward = 0

        else:

            stop_distance = fabs(
                entry - stop_loss
            )

            if stop_distance < 0.00000001:
                stop_distance = 0.00000001

            position_size = (
                risk_amount /
                stop_distance
            )

            reward = fabs(
                take_profit_2 -
                entry
            )

            risk_reward = round(
                reward /
                stop_distance,
                2
            )

            if risk_reward < 1.5:

                trade_allowed = False

                reasons.append(
                    "العائد أقل من المخاطرة"
                )
                               if smart_money.get(
            "bullish",
            False
        ):
            reasons.append(
                "Smart Money إيجابي"
            )

        if smart_money.get(
            "bearish",
            False
        ):
            reasons.append(
                "Smart Money سلبي"
            )

        if fibonacci.get(
            "signal"
        ):
            reasons.append(
                f"فيبوناتشي: {fibonacci['signal']}"
            )

        return {

            "direction": direction,

            "entry": (
                round(entry, 4)
                if entry is not None
                else None
            ),

            "stop_loss": (
                round(stop_loss, 4)
                if stop_loss is not None
                else None
            ),

            "take_profit_1": (
                round(take_profit_1, 4)
                if take_profit_1 is not None
                else None
            ),

            "take_profit_2": (
                round(take_profit_2, 4)
                if take_profit_2 is not None
                else None
            ),

            "take_profit_3": (
                round(take_profit_3, 4)
                if take_profit_3 is not None
                else None
            ),

            "atr": round(
                atr,
                4
            ),

            "position_size": round(
                position_size,
                4
            ),

            "risk_percent": risk_percent,

            "risk_amount": round(
                risk_amount,
                2
            ),

            "risk_reward": risk_reward,

            "confidence": confidence,

            "market_state": market_state,

            "trade_allowed": trade_allowed,

            "reasons": reasons

        }    
                           دخول")
