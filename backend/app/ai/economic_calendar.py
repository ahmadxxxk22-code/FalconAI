import datetime


class EconomicCalendar:

    def __init__(self):

        self.high_impact_keywords = [

            "interest rate",
            "federal reserve",
            "fed",
            "ecb",
            "bank of england",
            "boj",
            "cpi",
            "inflation",
            "ppi",
            "nfp",
            "nonfarm",
            "unemployment",
            "gdp",
            "pmi",
            "fomc",
            "powell",
            "lagarde"

        ]

    def analyze(self, news):

        if not news:

            return self.empty()

        headline = str(
            news.get(
                "headline",
                ""
            )
        ).lower()

        impact = "LOW"

        trade_allowed = True

        confidence = 50

        reasons = []

        for keyword in self.high_impact_keywords:

            if keyword in headline:

                impact = "HIGH"

                trade_allowed = False

                confidence = 90

                reasons.append(

                    f"High Impact Event: {keyword}"

                )

        if news.get(
            "bullish",
            False
        ):

            reasons.append(
                "Positive News"
            )

        if news.get(
            "bearish",
            False
        ):

            reasons.append(
                "Negative News"
            )

        return {

            "impact": impact,

            "confidence": confidence,

            "trade_allowed": trade_allowed,

            "reasons": reasons,

            "checked_at": datetime.datetime.utcnow().isoformat()

        }

    def empty(self):

        return {

            "impact": "UNKNOWN",

            "confidence": 0,

            "trade_allowed": True,

            "reasons": [

                "No economic events"

            ],

            "checked_at": datetime.datetime.utcnow().isoformat()

        }
