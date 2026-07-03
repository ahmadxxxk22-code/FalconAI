from datetime import datetime


class LearningEngine:

    def __init__(self):

        self.history = []

    def save_trade(self, signal):

        signal["saved_at"] = datetime.utcnow().isoformat()

        self.history.append(signal)

        return True

    def success_rate(self):

        if len(self.history) == 0:

            return 0

        wins = len(

            [
                x for x in self.history

                if x.get("result") == "WIN"
            ]

        )

        return round(

            wins / len(self.history) * 100,

            2

        )

    def total_trades(self):

        return len(self.history)

    def last_trades(self, limit=20):

        return self.history[-limit:]

    def statistics(self):

        return {

            "total_trades": self.total_trades(),

            "success_rate": self.success_rate(),

            "last_update": datetime.utcnow().isoformat()

        }
