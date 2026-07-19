from typing import List, Dict, Any
from statistics import mean

from app.services.market_data import MarketData


class SmartMoneyAnalyzer:

    def __init__(self):

        self.market = MarketData()

        # عدد الشموع المستخدمة لاكتشاف Swing
        self.swing_window = 7

        # هامش مساواة القمم والقيعان
        self.equal_tolerance = 0.0015

        # أقل قوة مطلوبة للإزاحة
        self.displacement_multiplier = 1.8

        # عدد الشموع المستخدمة لحساب متوسط الجسم
        self.average_body_period = 50

    # =====================================================
    # MAIN
    # =====================================================

    def analyze(

        self,

        symbol="BTCUSDT",

        interval="1h",

        market="crypto"

    ):

        candles = self.market.get_candles(

            symbol=symbol,

            interval=interval,

            limit=400,

            market=market

        )

        if not candles or len(candles) < 100:

            return self.empty_result()

        highs = [c["high"] for c in candles]

        lows = [c["low"] for c in candles]

        opens = [c["open"] for c in candles]

        closes = [c["close"] for c in candles]

        volumes = [c["volume"] for c in candles]

        current_price = closes[-1]

        bullish = False
        bearish = False

        confidence = 0
        score = 0

        reasons = []

        # ==========================================
        # استخراج Swing High / Swing Low
        # ==========================================

        swing_highs = self.detect_swing_highs(

            highs

        )

        swing_lows = self.detect_swing_lows(

            lows

        )

        last_swing_high = (

            swing_highs[-1]

            if swing_highs

            else None

        )

        last_swing_low = (

            swing_lows[-1]

            if swing_lows

            else None

        )

        # ==========================================
        # Liquidity
        # ==========================================

        liquidity = self.detect_liquidity(

            candles,

            swing_highs,

            swing_lows

        )



    # ==========================================
    # Liquidity Sweep
    # ==========================================

    liquidity_sweep = False

    liquidity_side = "NONE"

    if last_swing_high:

        if (

            candles[-1]["high"] >

            last_swing_high["price"]

            and

            candles[-1]["close"] <

            last_swing_high["price"]

        ):

            liquidity_sweep = True

            liquidity_side = "BUY_SIDE"

            bearish = True

            score += 15

            reasons.append(

                "Buy Side Liquidity Sweep"

            )

    if last_swing_low:

        if (

            candles[-1]["low"] <

            last_swing_low["price"]

            and

            candles[-1]["close"] >

            last_swing_low["price"]

        ):

            liquidity_sweep = True

            liquidity_side = "SELL_SIDE"

            bullish = True

            score += 15

            reasons.append(

                "Sell Side Liquidity Sweep"

            )

    # ==========================================
    # Equal Highs
    # ==========================================

    equal_highs = []

    for i in range(1, len(swing_highs)):

        p1 = swing_highs[i - 1]["price"]

        p2 = swing_highs[i]["price"]

        diff = abs(p1 - p2) / p1

        if diff <= self.equal_tolerance:

            equal_highs.append(

                swing_highs[i]

            )

    # ==========================================
    # Equal Lows
    # ==========================================

    equal_lows = []

    for i in range(1, len(swing_lows)):

        p1 = swing_lows[i - 1]["price"]

        p2 = swing_lows[i]["price"]

        diff = abs(p1 - p2) / p1

        if diff <= self.equal_tolerance:

            equal_lows.append(

                swing_lows[i]

            )

    if equal_highs:

        reasons.append(

            "Equal Highs Detected"

        )

        score += 5

    if equal_lows:

        reasons.append(

            "Equal Lows Detected"

        )

        score += 5

    # ==========================================
    # Displacement
    # ==========================================

    displacement = False

    average_body = mean(

        [

            abs(

                c["close"] -

                c["open"]

            )

            for c in candles[
                -self.average_body_period:
            ]

        ]

    )

    current_body = abs(

        candles[-1]["close"]

        -

        candles[-1]["open"]

    )

    if current_body >= (

        average_body *

        self.displacement_multiplier

    ):

        displacement = True

        score += 15

        reasons.append(

            "Displacement Candle"

        )



    # ==========================================
    # Break Of Structure (BOS)
    # ==========================================

    bos = False
    bos_direction = "NONE"

    if last_swing_high:

        if current_price > last_swing_high["price"]:

            bos = True
            bos_direction = "BULLISH"

            bullish = True

            score += 20

            reasons.append(
                "Bullish Break Of Structure"
            )

    if last_swing_low:

        if current_price < last_swing_low["price"]:

            bos = True
            bos_direction = "BEARISH"

            bearish = True

            score += 20

            reasons.append(
                "Bearish Break Of Structure"
            )

    # ==========================================
    # Change Of Character (CHOCH)
    # ==========================================

    choch = False
    choch_direction = "NONE"

    if len(swing_highs) >= 2 and len(swing_lows) >= 2:

        last_high = swing_highs[-1]["price"]
        previous_high = swing_highs[-2]["price"]

        last_low = swing_lows[-1]["price"]
        previous_low = swing_lows[-2]["price"]

        # Bullish CHOCH
        if (

            last_low > previous_low

            and

            current_price > last_high

        ):

            choch = True

            choch_direction = "BULLISH"

            bullish = True

            score += 20

            reasons.append(
                "Bullish CHOCH"
            )

        # Bearish CHOCH
        elif (

            last_high < previous_high

            and

            current_price < last_low

        ):

            choch = True

            choch_direction = "BEARISH"

            bearish = True

            score += 20

            reasons.append(
                "Bearish CHOCH"
            )

    # ==========================================
    # Internal BOS
    # ==========================================

    internal_bos = False

    if len(closes) >= 6:

        if closes[-1] > max(closes[-6:-1]):

            internal_bos = True

            bullish = True

            score += 8

            reasons.append(
                "Internal Bullish BOS"
            )

        elif closes[-1] < min(closes[-6:-1]):

            internal_bos = True

            bearish = True

            score += 8

            reasons.append(
                "Internal Bearish BOS"
            )



    # ==========================================
    # Premium / Discount Zone
    # ==========================================

    premium_discount = "NEUTRAL"

    if last_swing_high and last_swing_low:

        dealing_range = (

            last_swing_high["price"]

            -

            last_swing_low["price"]

        )

        midpoint = (

            last_swing_low["price"]

            +

            dealing_range / 2

        )

        if current_price > midpoint:

            premium_discount = "PREMIUM"

            reasons.append(
                "Premium Zone"
            )

        else:

            premium_discount = "DISCOUNT"

            reasons.append(
                "Discount Zone"
            )

    # ==========================================
    # Order Block
    # ==========================================

    order_block = None

    if bullish:

        order_block = {

            "type": "BULLISH",

            "low": candles[-2]["low"],

            "high": candles[-2]["high"]

        }

    elif bearish:

        order_block = {

            "type": "BEARISH",

            "low": candles[-2]["low"],

            "high": candles[-2]["high"]

        }

    # ==========================================
    # Mitigation Block
    # ==========================================

    mitigation_block = None

    if order_block:

        mitigation_block = {

            "active": True,

            "zone": order_block

        }

    # ==========================================
    # Breaker Block
    # ==========================================

    breaker_block = None

    if bos and liquidity_sweep:

        breaker_block = {

            "active": True,

            "direction": bos_direction

        }

    # ==========================================
    # Smart Money Score
    # ==========================================

    score = min(score, 100)

    confidence = score

    signal = "WAIT"

    if bullish and score >= 60:

        signal = "BUY"

        elif bearish and score >= 60:

            signal = "SELL"

        return {

            "signal": signal,

            "confidence": confidence,

            "smart_money_score": score,

            "bullish": bullish,

            "bearish": bearish,

            "bos": bos,

            "bos_direction": bos_direction,

            "choch": choch,

            "choch_direction": choch_direction,

            "internal_bos": internal_bos,

            "liquidity_sweep": liquidity_sweep,

            "liquidity_side": liquidity_side,

            "equal_highs": equal_highs,

            "equal_lows": equal_lows,

            "displacement": displacement,

            "premium_discount": premium_discount,

            "order_block": order_block,

            "mitigation_block": mitigation_block,

            "breaker_block": breaker_block,

            "reasons": reasons

        }

    # =====================================================
    # EMPTY RESULT
    # =====================================================

    def empty_result(self):

        return {

            "signal": "WAIT",

            "confidence": 0,

            "smart_money_score": 0,

            "bullish": False,

            "bearish": False,

            "bos": False,

            "choch": False,

            "internal_bos": False,

            "liquidity_sweep": False,

            "liquidity_side": "NONE",

            "equal_highs": [],

            "equal_lows": [],

            "displacement": False,

            "premium_discount": "NEUTRAL",

            "order_block": None,

            "mitigation_block": None,

            "breaker_block": None,

            "reasons": []

        }
