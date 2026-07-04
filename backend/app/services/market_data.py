from app.services.market_router import MarketRouter


class MarketData:

    def __init__(self):

        self.router = MarketRouter()

    def get_price(

        self,

        symbol="BTCUSDT",

        market="crypto"

    ):

        return self.router.get_price(

            symbol,

            market

        )

    def get_24h(

        self,

        symbol="BTCUSDT",

        market="crypto"

    ):

        return self.router.get_24h(

            symbol,

            market

        )

    def get_candles(

        self,

        symbol="BTCUSDT",

        interval="1h",

        limit=200,

        market="crypto"

    ):

        return self.router.get_candles(

            symbol=symbol,

            interval=interval,

            limit=limit,

            market=market

        )

    def get_close_prices(

        self,

        symbol="BTCUSDT",

        interval="1h",

        limit=200,

        market="crypto"

    ):

        candles = self.get_candles(

            symbol,

            interval,

            limit,

            market

        )

        return [

            candle["close"]

            for candle in candles

        ]

    def get_volumes(

        self,

        symbol="BTCUSDT",

        interval="1h",

        limit=200,

        market="crypto"

    ):

        candles = self.get_candles(

            symbol,

            interval,

            limit,

            market

        )

        return [

            candle["volume"]

            for candle in candles

        ]
