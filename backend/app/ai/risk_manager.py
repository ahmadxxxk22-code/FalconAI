class RiskManager:

    def calculate(
        self,
        direction="BUY",
        price=100,
        confidence=80,
        balance=1000,
        risk_percent=2
    ):

        risk_amount = balance * (risk_percent / 100)

        if direction == "BUY":

            stop_loss = price * 0.98

            take_profit_1 = price * 1.02

            take_profit_2 = price * 1.04

            take_profit_3 = price * 1.06

        elif direction == "SELL":

            stop_loss = price * 1.02

            take_profit_1 = price * 0.98

            take_profit_2 = price * 0.96

            take_profit_3 = price * 0.94

        else:

            stop_loss = price

            take_profit_1 = price

            take_profit_2 = price

            take_profit_3 = price

        stop_distance = abs(price - stop_loss)

        if stop_distance == 0:
            stop_distance = 0.0001

        position_size = risk_amount / stop_distance

        risk_reward = round(
            abs(take_profit_2 - price) / stop_distance,
            2
        )

        return {

            "direction": direction,

            "entry": round(price, 4),

            "stop_loss": round(stop_loss, 4),

            "take_profit_1": round(take_profit_1, 4),

            "take_profit_2": round(take_profit_2, 4),

            "take_profit_3": round(take_profit_3, 4),

            "position_size": round(position_size, 4),

            "risk_reward": risk_reward,

            "confidence": confidence,

            "trade_allowed": (
                confidence >= 60
                and risk_reward >= 2
            )

        }
