import feedparser


class NewsAnalyzer:

    def analyze(self, symbol="BTCUSDT"):

        try:

            feed = feedparser.parse(
                "https://www.coindesk.com/arc/outboundfeeds/rss/"
            )

            if len(feed.entries) == 0:

                return self.empty(symbol)

            article = feed.entries[0]

            title = article.title.lower()

            bullish_words = [
                "surge",
                "rise",
                "bull",
                "record",
                "adoption",
                "growth",
                "approval"
            ]

            bearish_words = [
                "crash",
                "fall",
                "hack",
                "ban",
                "lawsuit",
                "bear",
                "drop"
            ]

            bullish = any(
                word in title
                for word in bullish_words
            )

            bearish = any(
                word in title
                for word in bearish_words
            )

            sentiment = "NEUTRAL"

            if bullish:
                sentiment = "BULLISH"

            if bearish:
                sentiment = "BEARISH"

            return {

                "symbol": symbol,

                "headline": article.title,

                "sentiment": sentiment,

                "confidence": 70,

                "bullish": bullish,

                "bearish": bearish

            }

        except Exception:

            return self.empty(symbol)

    def empty(self, symbol):

        return {

            "symbol": symbol,

            "headline": "No News",

            "sentiment": "NEUTRAL",

            "confidence": 50,

            "bullish": False,

            "bearish": False

        }
