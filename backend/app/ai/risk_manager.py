from math import fabs


class RiskManager:

    def __init__(self):

        self.max_position_percent = 10

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



    # ==========================================
    # Dynamic Position Size
    # ==========================================

    def calculate_position_size(
        self,
        balance,
        risk_amount,
        stop_distance
    ):

        if stop_distance <= 0:
            return 0

        position = risk_amount / stop_distance

        max_position = balance * (
            self.max_position_percent / 100
        )

        return round(
            min(position, max_position),
            6
        )



    # ==========================================
    # Risk Reward
    # ==========================================

    def calculate_rr(
        self,
        entry,
        stop,
        target
    ):

        risk = fabs(
            entry - stop
        )

        reward = fabs(
            target - entry
        )

        if risk <= 0:
            return 0

        return round(
            reward / risk,
            2
        )


    # ==========================================
    # Trade Grade
    # ==========================================

    def trade_grade(
        self,
        confidence,
        rr,
        trend_strength
    ):

        score = 0

        score += confidence * 0.6
        score += rr * 15
        score += abs(trend_strength) * 8

        if score >= 95:
            return "A+"

        if score >= 85:
            return "A"

        if score >= 75:
            return "B"

        if score >= 65:
            return "C"

        return "D"


    # ==========================================
    # Breakeven
    # ==========================================

    def breakeven_price(
        self,
        entry,
        stop
    ):

        risk = fabs(
            entry - stop
        )

        return round(
            entry + risk,
            4
        )


    # ==========================================
    # Trailing Stop
    # ==========================================

    def trailing_stop(
        self,
        direction,
        current_price,
        atr
    ):

        if direction == "BUY":

            return round(
                current_price - atr,
                4
            )

        if direction == "SELL":

            return round(
                current_price + atr,
                4
            )

        return None



    # ==========================================
    # MAIN RISK CALCULATION
    # ==========================================

    def calculate(
        self,
        direction,
        price,
        confidence,
        atr,
        volatility,
        trend_strength,
        market_state,
        smart_money=None,
        fibonacci=None,
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

        smart_money = smart_money or {}

        fibonacci = fibonacci or {}

        if confidence < 60:

            trade_allowed = False

            reasons.append(
                "Low confidence"
            )

        if market_state == "SIDEWAYS":

            trade_allowed = False

            reasons.append(
                "Sideways market"
            )

        if abs(trend_strength) < 0.5:

            trade_allowed = False

            reasons.append(
                "Weak trend"
            )

        if direction == "WAIT":

            trade_allowed = False

            reasons.append(
                "No entry signal"
            )



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

            position_size = self.calculate_position_size(
                balance,
                risk_amount,
                stop_distance
            )

            risk_reward = self.calculate_rr(
                entry,
                stop_loss,
                take_profit_2
            )



        grade = self.trade_grade(
            confidence,
            risk_reward,
            trend_strength
        )

        breakeven = None

        trailing = None

        if entry is not None:

            breakeven = self.breakeven_price(
                entry,
                stop_loss
            )

            trailing = self.trailing_stop(
                direction,
                entry,
                atr
            )

        if risk_reward < 1.5:

            trade_allowed = False

            reasons.append(
                "Poor risk reward"
            )

        if smart_money.get(
            "bullish",
            False
        ):

            reasons.append(
                "Smart Money Bullish"
            )

        if smart_money.get(
            "bearish",
            False
        ):

            reasons.append(
                "Smart Money Bearish"
            )

        if fibonacci.get(
            "signal"
        ):

            reasons.append(
                f"Fibonacci: {fibonacci['signal']}"
            )

        if volatility > atr * 2:

            reasons.append(
                "High volatility"
            )

        elif volatility < atr * 0.5:

            reasons.append(
                "Low volatility"
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

            "breakeven": (
                round(breakeven, 4)
                if breakeven is not None
                else None
            ),

            "trailing_stop": (
                round(trailing, 4)
                if trailing is not None
                else None
            ),

            "atr": round(
                atr,
                4
            ),

            "volatility": round(
                volatility,
                4
            ),

            "position_size": round(
                position_size,
                6
            ),

            "risk_percent": risk_percent,

            "risk_amount": round(
                risk_amount,
                2
            ),

            "risk_reward": risk_reward,

            "grade": grade,

            "confidence": confidence,

            "market_state": market_state,

            "trade_allowed": trade_allowed,

            "reasons": reasons
        }
