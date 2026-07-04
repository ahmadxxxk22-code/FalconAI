from datetime import datetime


class LearningEngine:

    def __init__(self):

        self.history = []

    def save_trade(self, trade):

        trade["saved_at"] = datetime.utcnow().isoformat()

        self.history.append(trade)

        return True

    def success_rate(self):

        if not self.history:
            return 0

        wins = sum(
            1 for trade in self.history
            if trade.get("result") == "WIN"
        )

        return round(
            wins / len(self.history) * 100,
            2
        )

    def total_trades(self):

        return len(self.history)

    def last_trades(self, limit=20):

        return self.history[-limit:]

    def analyze_mistakes(self):

        losses = [

            trade

            for trade in self.history

            if trade.get("result") == "LOSS"

        ]

        reasons = {}

        for trade in losses:

            reason = trade.get(
                "reason",
                "UNKNOWN"
            )

            reasons[reason] = reasons.get(
                reason,
                0
            ) + 1

        return reasons

    def best_patterns(self):

        stats = {}

        for trade in self.history:

            pattern = trade.get(
                "pattern",
                "UNKNOWN"
            )

            if pattern not in stats:

                stats[pattern] = {

                    "wins": 0,

                    "losses": 0

                }

            if trade.get("result") == "WIN":

                stats[pattern]["wins"] += 1

            else:

                stats[pattern]["losses"] += 1

        return stats

    def statistics(self):

        return {

            "total_trades": self.total_trades(),

            "success_rate": self.success_rate(),

            "mistakes": self.analyze_mistakes(),

            "best_patterns": self.best_patterns(),

            "last_update": datetime.utcnow().isoformat()

        }
