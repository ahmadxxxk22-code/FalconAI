class SymbolMapper:

    BINANCE = {

        "BTC": "BTCUSDT",

        "ETH": "ETHUSDT",

        "SOL": "SOLUSDT"

    }

    OKX = {

        "BTC": "BTC-USDT",

        "ETH": "ETH-USDT",

        "SOL": "SOL-USDT"

    }

    COINBASE = {

        "BTC": "BTC-USD",

        "ETH": "ETH-USD",

        "SOL": "SOL-USD"

    }

    @staticmethod
    def to_binance(symbol):

        return SymbolMapper.BINANCE.get(

            symbol,

            symbol

        )

    @staticmethod
    def to_okx(symbol):

        return SymbolMapper.OKX.get(

            symbol,

            symbol

        )

    @staticmethod
    def to_coinbase(symbol):

        return SymbolMapper.COINBASE.get(

            symbol,

            symbol

        )
