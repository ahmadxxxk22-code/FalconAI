import requests

from app.services.base_market_service import BaseMarketService


class CoinbaseService(BaseMarketService):

    BASE_URL = "https://api.exchange.coinbase.com"


    @property
    def provider_name(self):

        return "Coinbase"


    def request(self, endpoint, params=None):

        try:

            response = requests.get(
                f"{self.BASE_URL}/{endpoint}",
                params=params,
                timeout=10
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:

            raise Exception(
                f"Coinbase API Error: {e}"
            )


    def get_price(
        self,
        symbol="BTC-USD",
        market="crypto"
    ):

        data = self.request(
            f"products/{symbol}/ticker"
        )

        return {

            "symbol": symbol,

            "price": float(data["price"])

        }


    def get_24h(
        self,
        symbol="BTC-USD",
        market="crypto"
    ):

        data = self.request(
            f"products/{symbol}/stats"
        )

        return {

            "symbol": symbol,

            "price": float(data["last"]),

            "high": float(data["high"]),

            "low": float(data["low"]),

            "volume": float(data["volume"])

        }


    def get_candles(

        self,

        symbol="BTC-USD",

        interval=3600,

        limit=200,

        market="crypto"

    ):

        data = self.request(

            f"products/{symbol}/candles",

            {

                "granularity": interval

            }

        )

        candles = []

        for candle in reversed(data[:limit]):

            candles.append({

                "open_time": candle[0],

                "low": float(candle[1]),

                "high": float(candle[2]),

                "open": float(candle[3]),

                "close": float(candle[4]),

                "volume": float(candle[5]),

                "close_time": candle[0]

            })

        return candles
