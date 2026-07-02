class RiskManager:

    def calculate(
        self,
        symbol="BTCUSDT",
        timeframe="1h",
        balance=1000,
        risk_percent=2,
        entry=100,
        stop_loss=98
    ):

        risk_amount = balance * (risk_percent / 100)

        stop_distance = abs(entry - stop_loss)

        if stop_distance == 0:
            stop_distance = 0.0001

        position_size = risk_amount / stop_distance

        tp1 = entry + (entry - stop_loss) * 1.5

        tp2 = entry + (entry - stop_loss) * 2

        tp3 = entry + (entry - stop_loss) * 3

        risk_reward = round(
            abs(tp2 - entry) / stop_distance,
            2
        )

        trade_allowed = risk_reward >= 2

        return {

            "symbol": symbol,

            "timeframe": timeframe,

            "entry": round(entry, 4),

            "stop_loss": round(stop_loss, 4),

            "take_profit_1": round(tp1, 4),

            "take_profit_2": round(tp2, 4),

            "take_profit_3": round(tp3, 4),

            "position_size": round(position_size, 4),

            "risk_percent": risk_percent,

            "risk_reward": risk_reward,

            "trade_allowed": trade_allowed

        }
