from app.services.market_router import MarketRouter


class DataManager:

    def __init__(self):

        self.router = MarketRouter()

    def get_price(self, symbol):

        return self.router.get_price(symbol)

    def get_market_summary(self, symbol):

        return self.router.get_24h(symbol)

    def get_candles(

        self,

        symbol,

        interval,

        limit=200

    ):

        return self.router.get_candles(

            symbol,

            interval,

            limit

        )

    def get_close_prices(

        self,

        symbol,

        interval,

        limit=200

    ):

        candles = self.get_candles(

            symbol,

            interval,

            limit

        )

        return [

            candle["close"]

            for candle in candles

        ]

    def get_highs(

        self,

        symbol,

        interval,

        limit=200

    ):

        candles = self.get_candles(

            symbol,

            interval,

            limit

        )

        return [

            candle["high"]

            for candle in candles

        ]

    def get_lows(

        self,

        symbol,

        interval,

        limit=200

    ):

        candles = self.get_candles(

            symbol,

            interval,

            limit

        )

        return [

            candle["low"]

            for candle in candles

        ]

    def get_volumes(

        self,

        symbol,

        interval,

        limit=200

    ):

        candles = self.get_candles(

            symbol,

            interval,

            limit

        )

        return [

            candle["volume"]

            for candle in candles

        ]
