from app.services.providers.binance_service import BinanceService
from app.services.providers.bybit_service import BybitService
from app.services.providers.okx_service import OKXService
from app.services.providers.coinbase_service import CoinbaseService
from app.services.providers.kraken_service import KrakenService
from app.services.providers.yahoo_service import YahooService
from app.services.providers.finnhub_service import FinnhubService
from app.services.providers.twelvedata_service import TwelveDataService


class MarketRouter:


    def __init__(self):

        self.crypto = [

            BinanceService(),

            BybitService(),

            OKXService(),

            CoinbaseService(),

            KrakenService()

        ]


        self.stocks = [

            YahooService(),

            FinnhubService()

        ]


        self.forex = [

            TwelveDataService()

        ]



    # =====================================
    # اختيار مزودي البيانات
    # =====================================

    def get_providers(
        self,
        market="crypto"
    ):


        if market == "crypto":

            return self.crypto


        if market == "stocks":

            return self.stocks


        if market == "forex":

            return self.forex


        return self.crypto



    # =====================================
    # توحيد الرموز
    # =====================================

    def map_symbol(
        self,
        provider,
        symbol
    ):


        name = provider.provider_name



        if name == "OKX":

            return symbol.replace(
                "USDT",
                "-USDT"
            )



        if name == "Coinbase":

            return symbol.replace(
                "USDT",
                "-USD"
            )



        if name == "Kraken":


            if symbol == "BTCUSDT":

                return "XBTUSDT"



        return symbol




    # =====================================
    # توحيد الفريمات الزمنية
    # =====================================

    def map_interval(
        self,
        provider,
        interval
    ):


        name = provider.provider_name


        mappings = {


            "Bybit": {

                "1m": "1",

                "5m": "5",

                "15m": "15",

                "30m": "30",

                "1h": "60",

                "4h": "240",

                "1d": "D"

            },



            "OKX": {

                "1m": "1m",

                "5m": "5m",

                "15m": "15m",

                "30m": "30m",

                "1h": "1H",

                "4h": "4H",

                "1d": "1D"

            },



            "Coinbase": {

                "1m": 60,

                "5m": 300,

                "15m": 900,

                "30m": 1800,

                "1h": 3600,

                "4h": 14400,

                "1d": 86400

            },



            "Kraken": {

                "1m": "1",

                "5m": "5",

                "15m": "15",

                "30m": "30",

                "1h": "60",

                "4h": "240",

                "1d": "1440"

            }

        }



        if name in mappings:

            return mappings[name].get(

                interval,

                interval

            )


        return interval





    # =====================================
    # السعر الحالي
    # =====================================

    def get_price(
        self,
        symbol,
        market="crypto"
    ):


        last_error = None



        for provider in self.get_providers(market):


            try:


                provider_symbol = self.map_symbol(

                    provider,

                    symbol

                )


                return provider.get_price(

                    provider_symbol,

                    market

                )


            except Exception as e:


                last_error = e



        raise Exception(

            f"No Provider Available: {last_error}"

        )





    # =====================================
    # بيانات 24 ساعة
    # =====================================

    def get_24h(
        self,
        symbol,
        market="crypto"
    ):


        last_error = None



        for provider in self.get_providers(market):


            try:


                provider_symbol = self.map_symbol(

                    provider,

                    symbol

                )


                return provider.get_24h(

                    provider_symbol,

                    market

                )



            except Exception as e:


                last_error = e




        raise Exception(

            f"No Provider Available: {last_error}"

        )





    # =====================================
    # الشموع
    # =====================================

    def get_candles(
        self,
        symbol,
        interval="1h",
        limit=200,
        market="crypto"
    ):


        last_error = None



        for provider in self.get_providers(market):


            try:


                provider_symbol = self.map_symbol(

                    provider,

                    symbol

                )



                provider_interval = self.map_interval(

                    provider,

                    interval

                )



                return provider.get_candles(

                    provider_symbol,

                    provider_interval,

                    limit,

                    market

                )



            except Exception as e:


                last_error = e




        raise Exception(

            f"No Provider Available: {last_error}"

    )
