import feedparser
from datetime import datetime

from app.ai.economic_calendar import EconomicCalendar


class NewsAnalyzer:

    def __init__(self):

        self.calendar = EconomicCalendar()

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

            bullish = any(
                word in title
                for word in self.bullish_words
            )

            bearish = any(
                word in title
                for word in self.bearish_words
            )

            sentiment = "NEUTRAL"
            confidence = 50

            if bullish and not bearish:
                sentiment = "BULLISH"
                confidence = 75

            elif bearish and not bullish:
                sentiment = "BEARISH"
                confidence = 75

            news = {

                "symbol": symbol,

                "market": self.detect_market(symbol),

                "headline": article.title,

                "sentiment": sentiment,

                "confidence": confidence,

                "bullish": bullish,

                "bearish": bearish,

                "source": "CoinDesk",

                "published_at": getattr(
                    article,
                    "published",
                    datetime.utcnow().isoformat()
                )

            }

            news["economic"] = self.calendar.analyze(news)

            news["trade_allowed"] = news["economic"]["trade_allowed"]

            return news

        except Exception:

            return self.empty(symbol)

    def detect_market(self, symbol):

        symbol = symbol.upper()

        if "XAU" in symbol or "GOLD" in symbol:
            return "GOLD"

        if "BTC" in symbol or "ETH" in symbol:
            return "CRYPTO"

        if any(x in symbol for x in [
            "EUR", "USD", "JPY",
            "GBP", "CHF",
            "AUD", "CAD",
            "NZD"
        ]):
            return "FOREX"

        if "OIL" in symbol:
            return "OIL"

        return "STOCK"

    def empty(self, symbol):

        news = {

            "symbol": symbol,

            "market": self.detect_market(symbol),

            "headline": "No News",

            "sentiment": "NEUTRAL",

            "confidence": 50,

            "bullish": False,

            "bearish": False,

            "source": None,

            "published_at": datetime.utcnow().isoformat()

        }

        news["economic"] = self.calendar.empty()

        news["trade_allowed"] = True

        return news
