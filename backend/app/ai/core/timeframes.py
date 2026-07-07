from dataclasses import dataclass


@dataclass(frozen=True)
class TimeFrame:

    name: str

    minutes: int

    binance: str

    bybit: str

    okx: str

    kraken: str

    yahoo: str

    twelvedata: str


TIMEFRAMES = {

    "1m": TimeFrame(
        "1m", 1, "1m", "1", "1m", "1", "1m", "1min"
    ),

    "3m": TimeFrame(
        "3m", 3, "3m", "3", "3m", "3", "5m", "3min"
    ),

    "5m": TimeFrame(
        "5m", 5, "5m", "5", "5m", "5", "5m", "5min"
    ),

    "15m": TimeFrame(
        "15m", 15, "15m", "15", "15m", "15", "15m", "15min"
    ),

    "30m": TimeFrame(
        "30m", 30, "30m", "30", "30m", "30", "30m", "30min"
    ),

    "1h": TimeFrame(
        "1h", 60, "1h", "60", "1H", "60", "60m", "1h"
    ),

    "2h": TimeFrame(
        "2h", 120, "2h", "120", "2H", "120", "60m", "2h"
    ),

    "4h": TimeFrame(
        "4h", 240, "4h", "240", "4H", "240", "60m", "4h"
    ),

    "6h": TimeFrame(
        "6h", 360, "6h", "360", "6H", "360", "60m", "6h"
    ),

    "8h": TimeFrame(
        "8h", 480, "8h", "480", "8H", "480", "60m", "8h"
    ),

    "12h": TimeFrame(
        "12h", 720, "12h", "720", "12H", "720", "60m", "12h"
    ),

    "1d": TimeFrame(
        "1d", 1440, "1d", "D", "1D", "1440", "1d", "1day"
    ),

    "3d": TimeFrame(
        "3d", 4320, "3d", "3D", "3D", "4320", "1d", "3day"
    ),

    "1w": TimeFrame(
        "1w", 10080, "1w", "W", "1W", "10080", "1wk", "1week"
    ),

    "1M": TimeFrame(
        "1M", 43200, "1M", "M", "1M", "21600", "1mo", "1month"
    )

}


def get_timeframe(name: str):

    if name not in TIMEFRAMES:

        raise ValueError(f"Unsupported timeframe: {name}")

    return TIMEFRAMES[name]
