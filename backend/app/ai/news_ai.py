import feedparser
from datetime import datetime


class NewsAnalyzer:

    def __init__(self):

        self.bullish_words = [
            "surge",
            "rise",
            "bull",
            "record",
            "adoption",
            "growth",
            "approval",
            "breakout",
            "strong",
            "gain",
            "buy"
        ]

        self.bearish_words = [
            "crash",
            "fall",
            "hack",
            "ban",
            "lawsuit",
            "bear",
            "drop",
            "sell",
            "collapse",
            "weak",
            "recession"
        ]

    def analyze(self, symbol="BTCUSDT"):

        try:

            feed = feedparser.parse(
                "https://www.coindesk.com/arc/outboundfeeds/rss/"
            )

            if not feed.entries:
                return self.empty(symbol)

            article = feed.entries[0]

            title = article.title.lower()

            bullish = any(word in title for word in self.bullish_words)
            bearish = any(word in title for word in self.bearish_words)

            sentiment = "NEUTRAL"
            confidence = 50

            if bullish and not bearish:
                sentiment = "BULLISH"
                confidence = 75

            elif bearish and not bullish:
                sentiment = "BEARISH"
                confidence = 75

            impact = self.detect_impact(title)

            return {

                "symbol": symbol,

                "market": self.detect_market(symbol),

                "headline": article.title,

                "sentiment": sentiment,

                "confidence": confidence,

                "impact": impact,

                "bullish": bullish,

                "bearish": bearish,

                "trade_allowed": impact != "EXTREME",

                "source": "CoinDesk",

                "published_at": getattr(
                    article,
                    "published",
                    datetime.utcnow().isoformat()
                )

            }

        except Exception:

            return self.empty(symbol)

    def detect_market(self, symbol):

        symbol = symbol.upper()

        if "XAU" in symbol or "GOLD" in symbol:
            return "GOLD"

        if "BTC" in symbol or "ETH" in symbol:
            return "CRYPTO"

        if any(x in symbol for x in ["EUR", "USD", "JPY", "GBP", "CHF", "AUD", "NZD", "CAD"]):
            return "FOREX"

        if "OIL" in symbol or "WTI" in symbol or "BRENT" in symbol:
            return "OIL"

        return "STOCK"

    def detect_impact(self, title):

        title = title.lower()

        extreme = [
            "federal reserve",
            "interest rate",
            "cpi",
            "nfp",
            "inflation"
        ]

        high = [
            "sec",
            "etf",
            "bank",
            "war",
            "sanction"
        ]

        if any(word in title for word in extreme):
            return "EXTREME"

        if any(word in title for word in high):
            return "HIGH"

        return "MEDIUM"

    def empty(self, symbol):

        return {

            "symbol": symbol,

            "market": self.detect_market(symbol),

            "headline": "No News",

            "sentiment": "NEUTRAL",

            "confidence": 50,

            "impact": "LOW",

            "bullish": False,

            "bearish": False,

            "trade_allowed": True,

            "source": None,

            "published_at": datetime.utcnow().isoformat()

        }
