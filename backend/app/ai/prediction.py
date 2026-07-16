from app.ai.market_analyzer import MarketAnalyzer
from app.ai.trend_engine import TrendEngine
from app.ai.opportunity.opportunity_engine import OpportunityEngine


class PredictionEngine:

    def __init__(self):

        self.market = MarketAnalyzer()

        self.trend = TrendEngine()

        self.opportunity = OpportunityEngine()



    # ==========================
    # Main Prediction
    # ==========================

    def predict(
        self,
        symbol="BTCUSDT",
        interval="1h",
        market="crypto"
    ):


        market_data = self.market.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )


        trend_data = self.trend.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )


        candles = market_data.get(

            "candles",

            []

        )


        opportunity_data = self.opportunity.analyze(

            symbol=symbol,

            candles=candles

        )


        price = market_data.get(

            "price",

            0

        )


        rsi = market_data.get(

            "rsi",

            0

        )


        macd = market_data.get(

            "macd",

            0

        )


        volume_ratio = market_data.get(

            "volume_ratio",

            0

        )


        momentum = market_data.get(

            "momentum",

            0

        )


        trend_score = trend_data.get(

            "score",

            0

        )


        trend = trend_data.get(

            "trend",

            "SIDEWAYS"

        )



        # ==========================
        # Opportunity Signal
        # ==========================

        opportunity_signal = opportunity_data.get(

            "signal",

            "WAIT"

        )


        opportunity_confidence = opportunity_data.get(

            "confidence",

            0

        )



        # ==========================
        # Internal Scoring
        # ==========================

        bullish_score = 0

        bearish_score = 0


        reasons = []



        # ==========================
        # Trend Analysis
        # ==========================

        if trend in [

            "STRONG_BULL",

            "BULL"

        ]:

            bullish_score += 30

            reasons.append(

                "الاتجاه العام يدعم الصعود"

            )


        elif trend in [

            "STRONG_BEAR",

            "BEAR"

        ]:

            bearish_score += 30

            reasons.append(

                "الاتجاه العام يدعم الهبوط"

            )



        # ==========================
        # Trend Score
        # ==========================

        if trend_score > 50:

            bullish_score += 20

            reasons.append(

                "قوة الاتجاه إيجابية"

            )


        elif trend_score < -50:

            bearish_score += 20

            reasons.append(

                "قوة الاتجاه سلبية"

            )



        # ==========================
        # RSI Confirmation
        # ==========================

        if rsi < 35:

            bullish_score += 10

            reasons.append(

                "RSI يشير إلى تشبع بيعي"

            )


        elif rsi > 65:

            bearish_score += 10

            reasons.append(

                "RSI يشير إلى تشبع شرائي"

            )



        # ==========================
        # MACD Confirmation
        # ==========================

        if macd > 0:

            bullish_score += 15

            reasons.append(

                "MACD إيجابي"

            )


        elif macd < 0:

            bearish_score += 15

            reasons.append(

                "MACD سلبي"

            )



        # ==========================
        # Momentum Confirmation
        # ==========================

        if momentum > 0:

            bullish_score += 10

            reasons.append(

                "الزخم الحالي إيجابي"

            )


        elif momentum < 0:

            bearish_score += 10

            reasons.append(

                "الزخم الحالي سلبي"

            )



        # ==========================
        # Volume Confirmation
        # ==========================

        if volume_ratio > 1:

            bullish_score += 10

            reasons.append(

                "حجم التداول أعلى من المتوسط"

            )


        elif volume_ratio < 1:

            bearish_score += 5

            reasons.append(

                "حجم التداول ضعيف"

            )



        # ==========================
        # Opportunity Engine Fusion
        # ==========================

        if opportunity_signal == "BUY":

            bullish_score += 20

            reasons.append(

                "محرك الفرص يعطي إشارة شراء"

            )


        elif opportunity_signal == "SELL":

            bearish_score += 20

            reasons.append(

                "محرك الفرص يعطي إشارة بيع"

            )



        # ==========================
        # Final Score
        # ==========================

        total_score = (

            bullish_score -

            bearish_score

        )



        if total_score > 0:

            direction = "BULLISH"


        elif total_score < 0:

            direction = "BEARISH"


        else:

            direction = "NEUTRAL"



        # ==========================
        # Signal Decision
        # ==========================

        signal = "WAIT"


        if bullish_score > bearish_score:

            if bullish_score >= 60:

                signal = "BUY"


        elif bearish_score > bullish_score:

            if bearish_score >= 60:

                signal = "SELL"



        # ==========================
        # Confidence Calculation
        # ==========================

        confidence = self.calculate_confidence(

            bullish_score,

            bearish_score,

            opportunity_confidence

        )



        # ==========================
        # Risk Status
        # ==========================

        risk_status = self.risk_evaluation(

            confidence,

            trend,

            volume_ratio

        )



        # ==========================
        # Market Strength
        # ==========================

        market_strength = {

            "bullish_score": bullish_score,

            "bearish_score": bearish_score,

            "difference": total_score

        }



        # ==========================
        # Final Result
        # ==========================

        return {

            "symbol": symbol,

            "market": market,

            "interval": interval,

            "signal": signal,

            "direction": direction,

            "confidence": confidence,

            "risk": risk_status,

            "price": price,

            "trend": trend,

            "trend_score": trend_score,

            "rsi": rsi,

            "macd": macd,

            "momentum": momentum,

            "volume_ratio": volume_ratio,

            "scores": market_strength,

            "reasons": reasons,

            "opportunity": opportunity_data,

            "market_analysis": market_data,

            "trend_analysis": trend_data

    }



    # ==========================
    # Confidence Calculation
    # ==========================

    def calculate_confidence(
        self,
        bullish_score,
        bearish_score,
        opportunity_confidence
    ):


        total = (

            bullish_score +

            bearish_score

        )


        if total == 0:

            return 0



        difference = abs(

            bullish_score -

            bearish_score

        )


        score_confidence = (

            difference /

            total

        ) * 100



        final_confidence = (

            score_confidence * 0.7

            +

            opportunity_confidence * 0.3

        )



        if final_confidence > 100:

            final_confidence = 100



        if final_confidence < 0:

            final_confidence = 0



        return round(

            final_confidence,

            2

        )



    # ==========================
    # Risk Evaluation
    # ==========================

    def risk_evaluation(
        self,
        confidence,
        trend,
        volume_ratio
    ):


        risk = "MEDIUM"



        if confidence >= 80:

            risk = "LOW"



        elif confidence < 50:

            risk = "HIGH"



        if trend in [

            "SIDEWAYS"

        ]:

            risk = "HIGH"



        if volume_ratio < 0.7:

            risk = "HIGH"



        return risk



    # ==========================
    # Trend Evaluation
    # ==========================

    def evaluate_trend(
        self,
        trend_data
    ):

        score = 0

        reasons = []


        trend = trend_data.get(
            "trend",
            "SIDEWAYS"
        )


        trend_strength = trend_data.get(
            "trend_strength",
            0
        )



        if trend in [

            "STRONG_BULL",
            "BULLISH_TREND"

        ]:

            score += 30

            reasons.append(

                "الاتجاه العام صاعد"

            )



        elif trend in [

            "STRONG_BEAR",
            "BEARISH_TREND"

        ]:

            score -= 30

            reasons.append(

                "الاتجاه العام هابط"

            )



        if trend_strength > 2:

            score += 15

            reasons.append(

                "قوة الاتجاه إيجابية"

            )


        elif trend_strength < -2:

            score -= 15

            reasons.append(

                "ضعف الاتجاه أو هبوط"

            )



        return {

            "score": score,

            "reasons": reasons

        }



    # ==========================
    # Early Reversal Detection
    # ==========================

    def detect_reversal(
        self,
        market_data
    ):

        signals = []

        score = 0


        rsi = market_data.get(
            "rsi",
            50
        )


        momentum = market_data.get(
            "momentum",
            0
        )


        volume = market_data.get(
            "volume_power",
            0
        )



        # Oversold Reversal

        if rsi < 30:

            score += 20

            signals.append(

                "RSI oversold reversal possibility"

            )



        # Overbought Reversal

        elif rsi > 70:

            score -= 20

            signals.append(

                "RSI overbought reversal possibility"

            )



        # Momentum Change

        if momentum > 0:

            score += 10

            signals.append(

                "Momentum turning positive"

            )


        elif momentum < 0:

            score -= 10

            signals.append(

                "Momentum turning negative"

            )



        # Volume Confirmation

        if volume > 1.5:

            score += 15

            signals.append(

                "Strong volume entering"

            )



        return {

            "score": score,

            "signals": signals

        }



    # ==========================
    # Breakout Detection
    # ==========================

    def detect_breakout(
        self,
        market_data
    ):

        candles = market_data.get(
            "candles",
            []
        )


        if len(candles) < 20:

            return {

                "breakout": False,

                "type": None

            }



        closes = [

            c["close"]

            for c in candles

        ]


        recent_high = max(

            closes[-20:]

        )


        recent_low = min(

            closes[-20:]

        )


        price = closes[-1]



        if price > recent_high:

            return {

                "breakout": True,

                "type": "BULLISH_BREAKOUT"

            }



        if price < recent_low:

            return {

                "breakout": True,

                "type": "BEARISH_BREAKOUT"

            }



        return {

            "breakout": False,

            "type": None

        }



    # ==========================
    # Smart Money Evaluation
    # ==========================

    def evaluate_smart_money(
        self,
        smart_money=None
    ):

        if not smart_money:

            return {

                "score": 0,

                "reasons": []

            }


        score = 0

        reasons = []


        direction = smart_money.get(
            "direction",
            None
        )


        if direction == "BUY":

            score += 20

            reasons.append(
                "Smart Money buying pressure"
            )


        elif direction == "SELL":

            score -= 20

            reasons.append(
                "Smart Money selling pressure"
            )


        return {

            "score": score,

            "reasons": reasons

        }



    # ==========================
    # Liquidity Evaluation
    # ==========================

    def evaluate_liquidity(
        self,
        liquidity=None
    ):

        if not liquidity:

            return {

                "score": 0,

                "reasons": []

            }



        score = 0

        reasons = []



        liquidity_state = liquidity.get(
            "state",
            None
        )



        if liquidity_state == "HIGH":

            score += 10

            reasons.append(

                "High liquidity detected"

            )


        elif liquidity_state == "LOW":

            score -= 10

            reasons.append(

                "Low liquidity risk"

            )



        return {

            "score": score,

            "reasons": reasons

        }



    # ==========================
    # Order Block Evaluation
    # ==========================

    def evaluate_order_blocks(
        self,
        order_blocks=None
    ):

        if not order_blocks:

            return {

                "score": 0,

                "reasons": []

            }



        score = 0

        reasons = []



        block_type = order_blocks.get(
            "type",
            None
        )



        if block_type == "BULLISH":

            score += 15

            reasons.append(

                "Bullish order block detected"

            )


        elif block_type == "BEARISH":

            score -= 15

            reasons.append(

                "Bearish order block detected"

            )



        return {

            "score": score,

            "reasons": reasons

        }



    # ==========================
    # Advanced Fusion Engine
    # ==========================

    def advanced_fusion(
        self,
        market_data,
        trend_data,
        smart_money=None,
        liquidity=None,
        order_blocks=None
    ):


        total_score = 0

        reasons = []



        # Trend

        trend_result = self.evaluate_trend(

            trend_data

        )


        total_score += trend_result["score"]

        reasons.extend(

            trend_result["reasons"]

        )



        # Reversal

        reversal = self.detect_reversal(

            market_data

        )


        total_score += reversal["score"]

        reasons.extend(

            reversal["signals"]

        )



        # Breakout

        breakout = self.detect_breakout(

            market_data

        )


        if breakout["breakout"]:

            if breakout["type"] == "BULLISH_BREAKOUT":

                total_score += 20

                reasons.append(

                    "Bullish breakout detected"

                )


            elif breakout["type"] == "BEARISH_BREAKOUT":

                total_score -= 20

                reasons.append(

                    "Bearish breakout detected"

                )



        # Smart Money

        smart_result = self.evaluate_smart_money(

            smart_money

        )


        total_score += smart_result["score"]

        reasons.extend(

            smart_result["reasons"]

        )



        # Liquidity

        liquidity_result = self.evaluate_liquidity(

            liquidity

        )


        total_score += liquidity_result["score"]

        reasons.extend(

            liquidity_result["reasons"]

        )



        # Order Blocks

        order_result = self.evaluate_order_blocks(

            order_blocks

        )


        total_score += order_result["score"]

        reasons.extend(

            order_result["reasons"]

        )



        # Final Direction

        if total_score >= 40:

            direction = "BULLISH"


        elif total_score <= -40:

            direction = "BEARISH"


        else:

            direction = "NEUTRAL"



        confidence = min(

            abs(total_score),

            100

        )



        return {

            "direction": direction,

            "score": total_score,

            "confidence": confidence,

            "reasons": reasons

        }



    # ==========================
    # Final Prediction Pipeline
    # ==========================

    def final_prediction(
        self,
        symbol="BTCUSDT",
        interval="1h",
        market="crypto",
        smart_money=None,
        liquidity=None,
        order_blocks=None
    ):

        market_data = self.market.analyze(
            symbol=symbol,
            interval=interval,
            market=market
        )


        trend_data = self.trend.analyze(
            symbol=symbol,
            interval=interval,
            market=market
        )


        candles = market_data.get(
            "candles",
            []
        )


        opportunity = self.opportunity.analyze(
            symbol=symbol,
            candles=candles
        )


        fusion = self.advanced_fusion(
            market_data,
            trend_data,
            smart_money,
            liquidity,
            order_blocks
        )


        score = fusion.get(
            "score",
            0
        )


        confidence = fusion.get(
            "confidence",
            0
        )


        signal = "WAIT"


        if score >= 40:
            signal = "BUY"


        elif score <= -40:
            signal = "SELL"



        opportunity_signal = opportunity.get(
            "signal",
            "WAIT"
        )


        if signal == "WAIT":

            if opportunity_signal == "BUY":
                signal = "BUY"

            elif opportunity_signal == "SELL":
                signal = "SELL"



        return {

            "symbol": symbol,

            "market": market,

            "interval": interval,

            "signal": signal,

            "confidence": confidence,

            "fusion_score": score,

            "direction": fusion.get(
                "direction"
            ),

            "reasons": fusion.get(
                "reasons",
                []
            ),

            "price": market_data.get(
                "price",
                0
            ),

            "rsi": market_data.get(
                "rsi",
                0
            ),

            "macd": market_data.get(
                "macd",
                0
            ),

            "momentum": market_data.get(
                "momentum",
                0
            ),

            "volume": market_data.get(
                "volume_power",
                0
            ),

            "market_analysis": market_data,

            "trend_analysis": trend_data,

            "opportunity": opportunity

            }
