from app.services.market_data import MarketData
from app.services.indicator_engine import IndicatorEngine


class MarketAnalyzer:

    def __init__(self):

        self.market = MarketData()

        self.indicators = IndicatorEngine()

    def analyze(
        self,
        symbol="BTCUSDT",
        interval="1h"
    ):

        prices = self.market.get_close_prices(
            symbol=symbol,
            interval=interval,
            limit=300
        )

        volumes = self.market.get_volumes(
            symbol=symbol,
            interval=interval,
            limit=300
        )

        if not prices or not volumes:

            raise Exception(
                "No market data received."
            )

        rsi = self.indicators.rsi(prices)

        ema = self.indicators.ema(prices)

        trend = self.indicators.trend_strength(prices)

        last_price = prices[-1]

        avg_volume = sum(volumes) / len(volumes)

        current_volume = volumes[-1]

        volume_power = (
            current_volume / avg_volume
            if avg_volume > 0
            else 0
        )

        bullish = (

            trend > 0

            and

            last_price > ema

            and

            rsi < 35

            and

            volume_power > 1

        )

        bearish = (

            trend < 0

            and

            last_price < ema

            and

            rsi > 65

            and

            volume_power > 1

        )

        return {

            "symbol": symbol,

            "price": last_price,

            "trend_strength": trend,

            "ema": ema,

            "rsi": rsi,

            "volume_power": round(
                volume_power,
                2
            ),

            "bullish": bullish,

            "bearish": bearish

        }
