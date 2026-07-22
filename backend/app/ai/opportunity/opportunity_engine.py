# ==========================================================
# FalconAI Opportunity Engine
# Production Version
# Part 1
# Core Architecture
# ==========================================================


from typing import Dict, Any, List


from app.ai.opportunity.trend_engine import TrendEngine
from app.ai.opportunity.volume_engine import VolumeEngine
from app.ai.opportunity.liquidity_engine import LiquidityEngine
from app.ai.opportunity.order_blocks import OrderBlocksEngine
from app.ai.opportunity.support_resistance import SupportResistanceEngine
from app.ai.opportunity.candles_ai import CandlesAI
from app.ai.opportunity.historical_learning import HistoricalLearning


from app.ai.smart_money import SmartMoneyAnalyzer



# Multi timeframe engine
try:

    from app.ai.multi_timeframe_engine import MultiTimeframeEngine

except Exception:

    MultiTimeframeEngine = None



# News protection
try:

    from app.ai.news_ai import NewsAnalyzer

except Exception:

    NewsAnalyzer = None




class OpportunityEngine:



    def __init__(self):


        # ==================================================
        # Engine Registry
        # ==================================================


        self.trend_engine = TrendEngine()

        self.volume_engine = VolumeEngine()

        self.liquidity_engine = LiquidityEngine()

        self.order_block_engine = OrderBlocksEngine()

        self.support_engine = SupportResistanceEngine()

        self.candle_engine = CandlesAI()

        self.history_engine = HistoricalLearning()

        self.smart_money_engine = SmartMoneyAnalyzer()



        # ==================================================
        # Optional Engines
        # ==================================================


        self.multi_timeframe_engine = (

            MultiTimeframeEngine()

            if MultiTimeframeEngine

            else None

        )



        self.news_engine = (

            NewsAnalyzer()

            if NewsAnalyzer

            else None

        )



        # ==================================================
        # Supported Timeframes
        # ==================================================


        self.timeframes = [

            "1m",

            "3m",

            "5m",

            "10m",

            "15m",

            "30m",

            "45m",

            "1h",

            "4h",

            "1D",

            "1W",

            "1M"

        ]



        # ==================================================
        # Signal Weights
        # ==================================================


        self.weights = {


            "smart_money": 25,


            "trend": 18,


            "volume": 10,


            "liquidity": 12,


            "order_blocks": 12,


            "candles": 8,


            "history": 10,


            "support_resistance": 5,


            "multi_timeframe": 15,


            "news_filter": 5


        }



        # ==================================================
        # Decision Parameters
        # ==================================================


        self.minimum_score = 50


        self.maximum_score = 100



        self.minimum_confidence = 65



        self.minimum_confirmations = 5



        self.reject_conflicting_signals = True



        # ==================================================
        # Smart Money Bonuses
        # ==================================================


        self.bos_bonus = 6


        self.choch_bonus = 8


        self.displacement_bonus = 5


        self.orderblock_bonus = 6


        self.breaker_bonus = 4


        self.mitigation_bonus = 3



        # ==================================================
        # Risk Settings
        # ==================================================


        self.minimum_risk_reward = 2.0


        self.default_take_profit_ratio = 3.0



        # ==================================================
        # Version
        # ==================================================


        self.version = (

            "FalconAI Opportunity Engine "

            "Production V2"

        )



    # ==================================================
    # Supported timeframe check
    # ==================================================


    def is_supported_timeframe(

        self,

        interval: str

    ) -> bool:


        return interval in self.timeframes



    # ==================================================
    # Empty Result
    # ==================================================


    def empty_result(

        self

    ) -> Dict[str, Any]:


        return {


            "signal": "WAIT",


            "confidence": 0,


            "quality": "D",


            "score": 0,


            "confirmations": 0,


            "reasons": [

                "Not enough market data"

            ],


            "engine": self.version,


            "status": "empty"


        }



    # ==========================================================
    # PART 2
    # Multi Timeframe Data Preparation
    # ==========================================================


    def prepare_timeframes(

        self,

        candles: List[dict],

        current_interval: str = "1h"

    ) -> Dict[str, Any]:


        """
        تجهيز بيانات السوق لكل الفريمات
        بدون إعادة جلب البيانات
        """


        result = {}


        if not candles:

            return result



        # عدد الشموع المطلوبة لكل فريم

        requirements = {


            "1m": 300,

            "3m": 300,

            "5m": 300,

            "10m": 300,

            "15m": 300,

            "30m": 250,

            "45m": 250,

            "1h": 200,

            "4h": 150,

            "1D": 100,

            "1W": 50,

            "1M": 24

        }



        for timeframe, minimum in requirements.items():


            if len(candles) >= minimum:


                result[timeframe] = {


                    "available": True,


                    "candles":

                    candles[-minimum:],


                    "count":

                    minimum


                }


            else:


                result[timeframe] = {


                    "available": False,


                    "candles": [],


                    "count": 0


                }



        return result




    # ==========================================================
    # Calculate Market Direction From Timeframes
    # ==========================================================


    def analyze_timeframe_alignment(

        self,

        timeframe_data: Dict[str, Any]

    ) -> Dict[str, Any]:



        bullish = 0

        bearish = 0

        active = 0


        details = {}



        for tf, data in timeframe_data.items():


            if not data.get(
                "available",
                False
            ):

                continue



            candles = data["candles"]



            if len(candles) < 50:

                continue



            closes = [

                c["close"]

                for c in candles

            ]



            first = closes[0]

            last = closes[-1]



            change = (

                (last - first)

                /

                first

            ) * 100



            direction = "SIDEWAYS"



            if change > 1:

                direction = "BULLISH"

                bullish += 1



            elif change < -1:

                direction = "BEARISH"

                bearish += 1



            active += 1



            details[tf] = {


                "direction":

                direction,


                "change":

                round(

                    change,

                    3

                )

            }



        if active == 0:


            return {


                "direction":

                "UNKNOWN",


                "bullish":

                0,


                "bearish":

                0,


                "details":

                details

            }




        if bullish > bearish:


            final_direction = "BULLISH"



        elif bearish > bullish:


            final_direction = "BEARISH"



        else:


            final_direction = "SIDEWAYS"




        confidence = (

            max(

                bullish,

                bearish

            )

            /

            active

        ) * 100




        return {


            "direction":

            final_direction,


            "bullish":

            bullish,


            "bearish":

            bearish,


            "confidence":

            round(

                confidence,

                2

            ),


            "details":

            details

        }



# ==========================================================
# PART 3
# Core Opportunity Scoring Engines
# ==========================================================


    def calculate_engine_scores(

        self,

        trend,

        volume,

        liquidity,

        order_blocks,

        history,

        smart_money,

        candle_patterns,

        support

    ):


        bullish = 0

        bearish = 0

        confirmations = 0

        reasons = []



        # ==================================================
        # SMART MONEY
        # ==================================================


        smart_score = smart_money.get(

            "smart_money_score",

            0

        )



        if smart_money.get(

            "bullish",

            False

        ):


            bullish += min(

                smart_score,

                self.weights["smart_money"]

            )


            confirmations += 1

            reasons.append(

                "Smart Money Bullish"

            )



        elif smart_money.get(

            "bearish",

            False

        ):


            bearish += min(

                smart_score,

                self.weights["smart_money"]

            )


            confirmations += 1

            reasons.append(

                "Smart Money Bearish"

            )



        # ==================================================
        # BOS / CHOCH
        # ==================================================


        if smart_money.get(

            "bos",

            False

        ):


            confirmations += 1


            if smart_money.get(

                "bos_direction"

            ) == "BULLISH":


                bullish += self.bos_bonus

                reasons.append(

                    "Bullish BOS"

                )


            elif smart_money.get(

                "bos_direction"

            ) == "BEARISH":


                bearish += self.bos_bonus

                reasons.append(

                    "Bearish BOS"

                )




        if smart_money.get(

            "choch",

            False

        ):


            confirmations += 1


            if smart_money.get(

                "choch_direction"

            ) == "BULLISH":


                bullish += self.choch_bonus

                reasons.append(

                    "Bullish CHOCH"

                )


            elif smart_money.get(

                "choch_direction"

            ) == "BEARISH":


                bearish += self.choch_bonus

                reasons.append(

                    "Bearish CHOCH"

                )



        # ==================================================
        # TREND
        # ==================================================


        trend_signal = trend.get(

            "signal",

            "WAIT"

        )



        if trend_signal == "BUY":


            bullish += self.weights["trend"]

            confirmations += 1

            reasons.append(

                "Trend Bullish"

            )


        elif trend_signal == "SELL":


            bearish += self.weights["trend"]

            confirmations += 1

            reasons.append(

                "Trend Bearish"

            )



        # ==================================================
        # VOLUME
        # ==================================================


        volume_score = volume.get(

            "score",

            0

        )



        if volume_score > 0:


            bullish += min(

                volume_score,

                self.weights["volume"]

            )


            confirmations += 1

            reasons.append(

                "Volume Support Buyers"

            )



        elif volume_score < 0:


            bearish += min(

                abs(volume_score),

                self.weights["volume"]

            )


            confirmations += 1

            reasons.append(

                "Volume Support Sellers"

            )



        # ==================================================
        # LIQUIDITY
        # ==================================================


        liquidity_score = liquidity.get(

            "score",

            0

        )



        if liquidity_score > 0:


            bullish += min(

                liquidity_score,

                self.weights["liquidity"]

            )


            confirmations += 1

            reasons.append(

                "Liquidity Bullish"

            )



        elif liquidity_score < 0:


            bearish += min(

                abs(liquidity_score),

                self.weights["liquidity"]

            )


            confirmations += 1

            reasons.append(

                "Liquidity Bearish"

            )



        return {


            "bullish_score":

                bullish,


            "bearish_score":

                bearish,


            "confirmations":

                confirmations,


            "reasons":

                reasons

                }



# ==========================================================
# PART 4
# Advanced Confirmation Layer
# ==========================================================


    def calculate_advanced_confirmation(

        self,

        order_blocks,

        candle_patterns,

        history,

        support,

        timeframe_alignment

    ):


        bullish = 0

        bearish = 0

        confirmations = 0

        reasons = []



        # ==================================================
        # ORDER BLOCK ENGINE
        # ==================================================


        if order_blocks.get(

            "bullish_blocks",

            False

        ):


            bullish += self.weights["order_blocks"]

            confirmations += 1

            reasons.append(

                "Bullish Order Block"

            )



        if order_blocks.get(

            "bearish_blocks",

            False

        ):


            bearish += self.weights["order_blocks"]

            confirmations += 1

            reasons.append(

                "Bearish Order Block"

            )



        # ==================================================
        # CANDLE AI
        # ==================================================


        candle_confidence = candle_patterns.get(

            "confidence",

            0

        )



        if candle_patterns.get(

            "bullish",

            False

        ):


            bullish += min(

                candle_confidence,

                self.weights["candles"]

            )


            confirmations += 1

            reasons.append(

                "Bullish Candle Pattern"

            )



        elif candle_patterns.get(

            "bearish",

            False

        ):


            bearish += min(

                candle_confidence,

                self.weights["candles"]

            )


            confirmations += 1

            reasons.append(

                "Bearish Candle Pattern"

            )



        # ==================================================
        # HISTORICAL LEARNING
        # ==================================================


        history_confidence = history.get(

            "confidence",

            0

        )



        if history.get(

            "bullish",

            False

        ):


            bullish += min(

                history_confidence,

                self.weights["history"]

            )


            confirmations += 1

            reasons.append(

                "Historical Bullish Pattern"

            )



        elif history.get(

            "bearish",

            False

        ):


            bearish += min(

                history_confidence,

                self.weights["history"]

            )


            confirmations += 1

            reasons.append(

                "Historical Bearish Pattern"

            )



        # ==================================================
        # SUPPORT RESISTANCE
        # ==================================================


        support_strength = support.get(

            "support_strength",

            0

        )


        resistance_strength = support.get(

            "resistance_strength",

            0

        )



        if support_strength >= 70:


            bullish += self.weights["support_resistance"]

            reasons.append(

                "Strong Support Zone"

            )



        if resistance_strength >= 70:


            bearish += self.weights["support_resistance"]

            reasons.append(

                "Strong Resistance Zone"

            )



        # ==================================================
        # MULTI TIMEFRAME
        # ==================================================


        direction = timeframe_alignment.get(

            "direction",

            "SIDEWAYS"

        )



        mtf_confidence = timeframe_alignment.get(

            "confidence",

            0

        )



        if direction == "BULLISH":


            bullish += (

                self.weights["multi_timeframe"]

                *

                mtf_confidence

                /

                100

            )


            reasons.append(

                "Multi Timeframe Bullish"

            )



        elif direction == "BEARISH":


            bearish += (

                self.weights["multi_timeframe"]

                *

                mtf_confidence

                /

                100

            )


            reasons.append(

                "Multi Timeframe Bearish"

            )



        return {


            "bullish_score":

                bullish,


            "bearish_score":

                bearish,


            "confirmations":

                confirmations,


            "reasons":

                reasons

            }


# ==========================================================
# PART 5
# Final Decision Engine
# ==========================================================


    def finalize_decision(

        self,

        base_result,

        advanced_result

    ):


        bullish_score = (

            base_result.get(

                "bullish_score",

                0

            )

            +

            advanced_result.get(

                "bullish_score",

                0

            )

        )



        bearish_score = (

            base_result.get(

                "bearish_score",

                0

            )

            +

            advanced_result.get(

                "bearish_score",

                0

            )

        )



        confirmations = (

            base_result.get(

                "confirmations",

                0

            )

            +

            advanced_result.get(

                "confirmations",

                0

            )

        )



        reasons = (

            base_result.get(

                "reasons",

                []

            )

            +

            advanced_result.get(

                "reasons",

                []

            )

        )



        score = (

            bullish_score

            -

            bearish_score

        )



        # ==================================================
        # Conflict Protection
        # ==================================================


        if self.reject_conflicting_signals:


            difference = abs(

                bullish_score

                -

                bearish_score

            )



            if (

                bullish_score > 0

                and

                bearish_score > 0

                and

                difference <= self.conflict_penalty

            ):


                return {


                    "signal":

                        "WAIT",


                    "confidence":

                        0,


                    "score":

                        score,


                    "bullish_score":

                        bullish_score,


                    "bearish_score":

                        bearish_score,


                    "confirmations":

                        confirmations,


                    "reasons":

                        reasons + [

                            "Conflicting market signals"

                        ]


                }




        # ==================================================
        # Confirmation Check
        # ==================================================


        if confirmations < self.minimum_confirmations:


            return {


                "signal":

                    "WAIT",


                "confidence":

                    0,


                "score":

                    score,


                "bullish_score":

                    bullish_score,


                "bearish_score":

                    bearish_score,


                "confirmations":

                    confirmations,


                "reasons":

                    reasons + [

                        "Insufficient confirmations"

                    ]

            }




        # ==================================================
        # Signal Direction
        # ==================================================


        signal = "WAIT"



        if (

            bullish_score >= self.minimum_score

            and

            bullish_score > bearish_score

        ):


            signal = "BUY"



        elif (

            bearish_score >= self.minimum_score

            and

            bearish_score > bullish_score

        ):


            signal = "SELL"




        # ==================================================
        # Confidence Calculation
        # ==================================================


        total_score = (

            bullish_score

            +

            bearish_score

        )



        confidence = 0



        if total_score > 0:


            confidence = int(

                (

                    max(

                        bullish_score,

                        bearish_score

                    )

                    /

                    total_score

                )

                *

                100

            )



        confidence = min(

            confidence,

            self.maximum_score

        )




        if confidence < self.minimum_confidence:


            signal = "WAIT"



            reasons.append(

                "Confidence below threshold"

            )



        return {


            "signal":

                signal,


            "confidence":

                confidence,


            "score":

                score,


            "bullish_score":

                bullish_score,


            "bearish_score":

                bearish_score,


            "confirmations":

                confirmations,


            "reasons":

                reasons

        }



# ==========================================================
# PART 6
# Quality + Risk Management Layer
# ==========================================================


    def calculate_quality(

        self,

        decision,

        smart_money,

        trend,

        volume,

        history,

        candle_patterns,

        support

    ):


        quality_score = 0



        # Smart Money Quality

        if smart_money.get("bos"):

            quality_score += 2


        if smart_money.get("choch"):

            quality_score += 2


        if smart_money.get("liquidity_sweep"):

            quality_score += 2


        if smart_money.get("order_block"):

            quality_score += 2


        if smart_money.get("displacement"):

            quality_score += 1



        # Trend confirmation

        if trend.get("signal") == decision:

            quality_score += 2



        # Volume confirmation

        volume_score = volume.get(

            "score",

            0

        )


        if decision == "BUY" and volume_score > 0:

            quality_score += 1


        if decision == "SELL" and volume_score < 0:

            quality_score += 1



        # Candle quality

        if candle_patterns.get(

            "confidence",

            0

        ) >= 70:

            quality_score += 1



        # Historical quality

        if history.get(

            "confidence",

            0

        ) >= 70:

            quality_score += 1



        # Support resistance

        if decision == "BUY":


            if support.get(

                "support_strength",

                0

            ) >= 70:

                quality_score += 1



        elif decision == "SELL":


            if support.get(

                "resistance_strength",

                0

            ) >= 70:

                quality_score += 1




        if quality_score >= 12:

            quality = "A+"

        elif quality_score >= 10:

            quality = "A"

        elif quality_score >= 8:

            quality = "B"

        elif quality_score >= 6:

            quality = "C"

        else:

            quality = "D"



        return {


            "quality":

                quality,


            "quality_score":

                quality_score

        }





    # ==========================================================
    # Risk Reward Calculator
    # ==========================================================


    def calculate_risk_reward(

        self,

        signal,

        current_price,

        support

    ):


        stop_loss = None

        take_profit = None

        risk_reward = 0



        if signal == "BUY":


            nearest_support = support.get(

                "nearest_support"

            )


            if nearest_support:


                stop_loss = nearest_support.get(

                    "price"

                )


                if stop_loss:


                    risk = (

                        current_price

                        -

                        stop_loss

                    )


                    if risk > 0:


                        take_profit = (

                            current_price

                            +

                            (

                                risk

                                *

                                self.default_take_profit_ratio

                            )

                        )


                        reward = (

                            take_profit

                            -

                            current_price

                        )


                        risk_reward = (

                            reward

                            /

                            risk

                        )



        elif signal == "SELL":


            nearest_resistance = support.get(

                "nearest_resistance"

            )


            if nearest_resistance:


                stop_loss = nearest_resistance.get(

                    "price"

                )


                if stop_loss:


                    risk = (

                        stop_loss

                        -

                        current_price

                    )


                    if risk > 0:


                        take_profit = (

                            current_price

                            -

                            (

                                risk

                                *

                                self.default_take_profit_ratio

                            )

                        )


                        reward = (

                            current_price

                            -

                            take_profit

                        )


                        risk_reward = (

                            reward

                            /

                            risk

                        )



        return {


            "stop_loss":

                stop_loss,


            "take_profit":

                take_profit,


            "risk_reward":

                round(

                    risk_reward,

                    2

                )

            }



# ==========================================================
# PART 7
# Main Analyze Pipeline + Production Status
# ==========================================================


    def analyze(

        self,

        symbol: str,

        candles: list,

        interval: str = "1h",

        market: str = "crypto"

    ) -> Dict[str, Any]:



        if not candles or len(candles) < 120:

            return self.empty_result()



        if not self.is_supported_timeframe(

            interval

        ):


            return {


                "signal":

                    "WAIT",


                "confidence":

                    0,


                "reason":

                    "Unsupported timeframe",


                "engine":

                    self.version

            }



        closes = [

            c["close"]

            for c in candles

        ]


        highs = [

            c["high"]

            for c in candles

        ]


        lows = [

            c["low"]

            for c in candles

        ]



        current_price = closes[-1]



        # ==================================================
        # Prepare Timeframes
        # ==================================================


        timeframe_data = self.prepare_timeframes(

            candles,

            interval

        )



        timeframe_alignment = self.analyze_timeframe_alignment(

            timeframe_data

        )



        # ==================================================
        # Run AI Engines
        # ==================================================


        trend = self.trend_engine.analyze(

            symbol

        )


        volume = self.volume_engine.analyze(

            candles

        )


        liquidity = self.liquidity_engine.analyze(

            candles

        )


        order_blocks = self.order_block_engine.analyze(

            candles

        )


        candle_patterns = self.candle_engine.analyze(

            candles

        )


        history = self.history_engine.analyze(

            candles

        )


        support = self.support_engine.analyze(

            highs,

            lows,

            closes

        )


        smart_money = self.smart_money_engine.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )



        # ==================================================
        # Calculate Scores
        # ==================================================


        base_result = self.calculate_engine_scores(

            trend,

            volume,

            liquidity,

            order_blocks,

            history,

            smart_money,

            candle_patterns,

            support

        )



        advanced_result = self.calculate_advanced_confirmation(

            order_blocks,

            candle_patterns,

            history,

            support,

            timeframe_alignment

        )



        decision = self.finalize_decision(

            base_result,

            advanced_result

        )



        signal = decision.get(

            "signal",

            "WAIT"

        )



        # ==================================================
        # Quality
        # ==================================================


        quality = self.calculate_quality(

            signal,

            smart_money,

            trend,

            volume,

            history,

            candle_patterns,

            support

        )



        decision.update(

            quality

        )



        # ==================================================
        # Risk
        # ==================================================


        risk = self.calculate_risk_reward(

            signal,

            current_price,

            support

        )



        decision.update(

            risk

        )



        if (

            signal != "WAIT"

            and

            decision["risk_reward"]

            <

            self.minimum_risk_reward

        ):


            decision["signal"] = "WAIT"


            decision["reasons"].append(

                "Risk reward below minimum"

            )



        # ==================================================
        # Final Output
        # ==================================================


        return {


            **decision,


            "symbol":

                symbol,


            "interval":

                interval,


            "price":

                current_price,


            "trend":

                trend,


            "volume":

                volume,


            "liquidity":

                liquidity,


            "order_blocks":

                order_blocks,


            "candles":

                candle_patterns,


            "history":

                history,


            "support":

                support,


            "smart_money":

                smart_money,


            "timeframe_alignment":

                timeframe_alignment,


            "engine":

                self.version,


            "status":

                "completed"

        }



    # ==========================================================
    # Production Status
    # ==========================================================


    def production_status(

        self

    ):


        return {


            "engine":

                self.version,


            "status":

                "ACTIVE",


            "supported_timeframes":

                self.timeframes,


            "engines":

            {


                "trend":

                    True,


                "volume":

                    True,


                "liquidity":

                    True,


                "order_blocks":

                    True,


                "candles":

                    True,


                "history":

                    True,


                "smart_money":

                    True,


                "multi_timeframe":

                    self.multi_timeframe_engine is not None


            }


        }



    # ==========================================================
    # Health Check
    # ==========================================================


    def health_check(

        self

    ):


        return {


            "engine":

                self.version,


            "status":

                "healthy",


            "timeframes":

                len(

                    self.timeframes

                ),


            "engines_loaded":

                8,


            "ready":

                True

        }



# ==========================================================
# FalconAI Opportunity Engine
# Production Version
# Part 8
# Production Intelligence Layer
# ==========================================================


    # ==================================================
    # Market Regime Detection
    # ==================================================

    def detect_market_regime(
        self,
        candles: list
    ) -> Dict[str, Any]:


        if not candles or len(candles) < 50:

            return {

                "regime": "UNKNOWN",

                "volatility": 0,

                "trend_strength": 0

            }



        closes = [

            c["close"]

            for c in candles

        ]



        moves = []


        for i in range(1, len(closes)):

            if closes[i-1] == 0:

                continue


            moves.append(

                abs(

                    (
                        closes[i]
                        -
                        closes[i-1]

                    )
                    /
                    closes[i-1]

                )

            )



        volatility = (

            sum(moves)
            /
            max(
                len(moves),
                1
            )

        ) * 100



        first = closes[0]

        last = closes[-1]


        trend_strength = abs(

            (
                last
                -
                first

            )
            /
            first

        ) * 100



        if volatility > 3:

            regime = "HIGH_VOLATILITY"


        elif trend_strength > 5:

            regime = "TRENDING"


        elif volatility < 0.5:

            regime = "LOW_VOLATILITY"


        else:

            regime = "RANGING"



        return {


            "regime": regime,


            "volatility": round(

                volatility,

                3

            ),


            "trend_strength": round(

                trend_strength,

                3

            )

        }



    # ==================================================
    # News Risk Protection
    # ==================================================

    def analyze_news_risk(
        self,
        symbol: str
    ) -> Dict[str, Any]:


        if not self.news_engine:

            return {


                "risk": False,


                "score": 0,


                "message": "News engine unavailable"

            }



        try:


            news = self.news_engine.analyze(

                symbol

            )


            impact = news.get(

                "impact",

                0

            )


            if impact >= 70:


                return {


                    "risk": True,


                    "score": impact,


                    "message":

                    "High impact news detected"

                }



            return {


                "risk": False,


                "score": impact,


                "message":

                "News risk normal"

            }



        except Exception:


            return {


                "risk": False,


                "score": 0,


                "message":

                "News analysis failed"

            }



    # ==================================================
    # Falcon Intelligence Score
    # ==================================================

    def calculate_falcon_score(
        self,
        analysis: Dict[str, Any]
    ) -> float:


        score = 0



        confidence = analysis.get(

            "confidence",

            0

        )


        quality_score = analysis.get(

            "quality_score",

            0

        )


        confirmations = analysis.get(

            "confirmations",

            0

        )



        score += confidence * 0.5


        score += quality_score * 3


        score += min(

            confirmations * 5,

            25

        )



        return round(

            min(

                score,

                100

            ),

            2

        )



    # ==================================================
    # Final User Explanation
    # ==================================================

    def explain_signal(
        self,
        result: Dict[str, Any]
    ) -> str:



        signal = result.get(

            "signal",

            "WAIT"

        )



        reasons = result.get(

            "reasons",

            []

        )



        if signal == "BUY":


            return (

                "FalconAI detected a BUY opportunity. "

                "Reasons: "

                +
                ", ".join(reasons)

            )



        if signal == "SELL":


            return (

                "FalconAI detected a SELL opportunity. "

                "Reasons: "

                +
                ", ".join(reasons)

            )



        return (

            "FalconAI recommends WAIT. "

            "Market confirmation is not strong enough. "

            +
            ", ".join(reasons)

        )



    # ==================================================
    # Final Production Validation
    # ==================================================

    def production_validation(
        self,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:


        warnings = []



        if result.get(

            "confidence",

            0

        ) < 60:


            warnings.append(

                "Low confidence"

            )



        if result.get(

            "quality",

            "D"

        ) in [

            "C",

            "D"

        ]:


            warnings.append(

                "Low signal quality"

            )



        if result.get(

            "risk_reward",

            0

        ) < 2:


            warnings.append(

                "Poor risk reward"

            )



        return {


            "approved":

            len(warnings) == 0,


            "warnings":

            warnings

        }



# ==========================================================
# PART 8
# Adaptive AI Learning Layer
# ==========================================================

    def adaptive_learning_update(

        self,

        result,

        candles

    ):


        if not result:

            return


        memory = {

            "signal": result.get("signal"),

            "confidence": result.get("confidence"),

            "quality": result.get("quality"),

            "score": result.get("score"),

            "price": candles[-1]["close"],

            "confirmations": result.get("confirmations"),

            "risk_reward": result.get("risk_reward"),

            "timestamp": candles[-1].get("time")

        }


        self.signal_memory.append(memory)


        if len(self.signal_memory) > self.max_memory:

            self.signal_memory.pop(0)



    def adaptive_signal_threshold(self):


        if len(self.signal_memory) < 200:

            return self.minimum_score


        wins = 0


        for item in self.signal_memory:

            if item["quality"] in ["A+", "A"]:

                wins += 1


        ratio = wins / len(self.signal_memory)


        if ratio >= 0.75:

            return max(

                self.minimum_score - 3,

                40

            )


        if ratio <= 0.45:

            return min(

                self.minimum_score + 5,

                60

            )


        return self.minimum_score



# ==========================================================
# PART 9
# Multi-Timeframe Consensus Layer
# ==========================================================

    def timeframe_consensus(

        self,

        analyses

    ):


        if not analyses:

            return {

                "direction": "WAIT",

                "score": 0,

                "confidence": 0

            }


        bullish = 0

        bearish = 0

        weight_sum = 0


        for tf, result in analyses.items():

            weight = self.get_timeframe_weight(tf)

            weight_sum += weight


            signal = result.get("signal", "WAIT")


            if signal == "BUY":

                bullish += weight


            elif signal == "SELL":

                bearish += weight


        score = bullish - bearish


        confidence = 0


        if weight_sum > 0:

            confidence = int(

                max(

                    bullish,

                    bearish

                )

                /

                weight_sum

                *

                100

            )


        direction = "WAIT"


        if bullish > bearish and confidence >= 60:

            direction = "BUY"


        elif bearish > bullish and confidence >= 60:

            direction = "SELL"


        return {

            "direction": direction,

            "bullish": bullish,

            "bearish": bearish,

            "score": score,

            "confidence": confidence

        }



    def build_timeframe_map(

        self,

        symbol,

        candles,

        market

    ):


        if not self.multi_timeframe_engine:

            return {}


        results = {}


        for tf in self.timeframes:


            try:

                results[tf] = (

                    self.multi_timeframe_engine.analyze(

                        symbol=symbol,

                        timeframe=tf,

                        candles=candles,

                        market=market

                    )

                )


            except Exception:

                continue


        return results



# ==========================================================
# PART 10
# Market Intelligence Fusion Layer
# ==========================================================


    def calculate_market_intelligence(

        self,

        trend,

        smart_money,

        history,

        regime,

        timeframe_result

    ):


        intelligence_score = 50


        reasons = []



        # Trend Influence

        trend_signal = trend.get(

            "signal",

            "WAIT"

        )


        if trend_signal == "BUY":

            intelligence_score += 10

            reasons.append(

                "Trend alignment bullish"

            )


        elif trend_signal == "SELL":

            intelligence_score -= 10

            reasons.append(

                "Trend alignment bearish"

            )



        # Smart Money Influence

        if smart_money.get(

            "bos",

            False

        ):

            intelligence_score += 8

            reasons.append(

                "Break of structure detected"

            )



        if smart_money.get(

            "choch",

            False

        ):

            intelligence_score += 8

            reasons.append(

                "Change of character detected"

            )



        if smart_money.get(

            "liquidity_sweep",

            False

        ):

            intelligence_score += 6

            reasons.append(

                "Liquidity sweep detected"

            )



        # Historical Learning

        history_confidence = history.get(

            "confidence",

            0

        )


        if history_confidence >= 70:

            intelligence_score += 5

            reasons.append(

                "Historical pattern confirmed"

            )



        # Market Regime

        if regime.get(

            "regime"

        ) == "TRENDING":

            intelligence_score += 5

            reasons.append(

                "Trending market"

            )


        elif regime.get(

            "regime"

        ) == "HIGH_VOLATILITY":

            intelligence_score -= 5

            reasons.append(

                "High volatility risk"

            )



        # Multi timeframe

        timeframe_confidence = timeframe_result.get(

            "confidence",

            0

        )


        if timeframe_confidence >= 70:

            intelligence_score += 5

            reasons.append(

                "Multi timeframe agreement"

            )



        intelligence_score = max(

            min(

                intelligence_score,

                100

            ),

            0

        )



        return {


            "intelligence_score":

                intelligence_score,


            "reasons":

                reasons

        }





    # ==================================================
    # Final Signal Explanation Builder
    # ==================================================


    def build_signal_explanation(

        self,

        result

    ):


        signal = result.get(

            "signal",

            "WAIT"

        )


        confidence = result.get(

            "confidence",

            0

        )


        quality = result.get(

            "quality",

            "D"

        )



        reasons = result.get(

            "reasons",

            []

        )



        if signal == "BUY":


            message = (

                "BUY opportunity detected. "

            )


        elif signal == "SELL":


            message = (

                "SELL opportunity detected. "

            )


        else:


            message = (

                "WAIT. Market confirmation is insufficient. "

            )



        message += (

            f"Confidence {confidence}%. "

            f"Quality {quality}. "

        )



        if reasons:


            message += (

                "Factors: "

                +

                ", ".join(reasons)

            )



        return message



# ==========================================================
# PART 11
# Falcon Final Decision Fusion
# ==========================================================


    def apply_intelligence_filter(

        self,

        decision,

        intelligence

    ):


        score = decision.get(

            "score",

            0

        )


        intelligence_score = intelligence.get(

            "intelligence_score",

            50

        )


        final_score = (

            score * 0.6

        ) + (

            (intelligence_score - 50)

            *

            0.8

        )



        decision["falcon_score"] = round(

            max(

                min(

                    final_score,

                    100

                ),

                -100

            ),

            2

        )



        if intelligence_score < 35:


            decision["signal"] = "WAIT"


            decision["reasons"].append(

                "Falcon intelligence rejected signal"

            )



        return decision





    # ==================================================
    # Production Output Formatter
    # ==================================================


    def format_production_result(

        self,

        result,

        symbol,

        interval,

        price

    ):


        explanation = self.build_signal_explanation(

            result

        )



        return {


            "symbol":

                symbol,


            "interval":

                interval,


            "price":

                price,


            "signal":

                result.get(

                    "signal",

                    "WAIT"

                ),


            "confidence":

                result.get(

                    "confidence",

                    0

                ),


            "quality":

                result.get(

                    "quality",

                    "D"

                ),


            "falcon_score":

                result.get(

                    "falcon_score",

                    0

                ),


            "risk_reward":

                result.get(

                    "risk_reward",

                    0

                ),


            "stop_loss":

                result.get(

                    "stop_loss"

                ),


            "take_profit":

                result.get(

                    "take_profit"

                ),


            "confirmations":

                result.get(

                    "confirmations",

                    0

                ),


            "explanation":

                explanation,


            "reasons":

                result.get(

                    "reasons",

                    []

                ),


            "engine":

                self.version,


            "status":

                "completed"

        }



# ==========================================================
# PART 12
# Final Market Decision Pipeline
# ==========================================================


    def final_decision_pipeline(

        self,

        symbol,

        candles,

        interval="1h",

        market="crypto"

    ):


        if not candles or len(candles) < 120:

            return self.empty_result()



        regime = self.detect_market_regime(

            candles

        )



        news_risk = self.analyze_news_risk(

            symbol

        )



        timeframe_results = self.build_timeframe_map(

            symbol,

            candles,

            market

        )



        timeframe_consensus = self.timeframe_consensus(

            timeframe_results

        )



        return {


            "regime":

                regime,


            "news_risk":

                news_risk,


            "timeframe_analysis":

                timeframe_results,


            "timeframe_consensus":

                timeframe_consensus

        }





    # ==================================================
    # Risk Protection Layer
    # ==================================================


    def apply_risk_protection(

        self,

        result,

        news_risk,

        regime

    ):



        if news_risk.get(

            "risk",

            False

        ):


            result["signal"] = "WAIT"


            result.setdefault(

                "reasons",

                []

            ).append(

                "High impact news protection"

            )



        if regime.get(

            "regime"

        ) == "HIGH_VOLATILITY":


            result["confidence"] = max(

                result.get(

                    "confidence",

                    0

                )

                -

                self.news_risk_penalty,

                0

            )


            result.setdefault(

                "reasons",

                []

            ).append(

                "High volatility adjustment"

            )



        return result



# ==========================================================
# PART 13
# Falcon Final Production Integration
# ==========================================================


    def production_finalize(

        self,

        symbol,

        interval,

        market,

        candles,

        decision

    ):


        pipeline = self.final_decision_pipeline(

            symbol=symbol,

            candles=candles,

            interval=interval,

            market=market

        )


        intelligence = self.calculate_market_intelligence(

            trend=decision.get("trend", {}),

            smart_money=decision.get("smart_money", {}),

            history=decision.get("history", {}),

            regime=pipeline["regime"],

            timeframe_result=pipeline["timeframe_consensus"]

        )


        decision = self.apply_intelligence_filter(

            decision,

            intelligence

        )


        decision = self.apply_risk_protection(

            decision,

            pipeline["news_risk"],

            pipeline["regime"]

        )


        validation = self.production_validation(

            decision

        )


        decision["validation"] = validation


        decision["market_regime"] = pipeline["regime"]


        decision["news"] = pipeline["news_risk"]


        decision["timeframes"] = pipeline["timeframe_consensus"]


        self.adaptive_learning_update(

            decision,

            candles

        )


        return self.format_production_result(

            result=decision,

            symbol=symbol,

            interval=interval,

            price=candles[-1]["close"]

        )



# ==================================================
# Falcon AI Score Rank
# ==================================================

    def classify_falcon_score(

        self,

        score

    ):


        if score >= 90:

            return "ELITE"


        if score >= 80:

            return "PREMIUM"


        if score >= 70:

            return "STRONG"


        if score >= 60:

            return "NORMAL"


        if score >= 50:

            return "WEAK"


        return "REJECTED"



    def add_rank(

        self,

        result

    ):


        result["rank"] = self.classify_falcon_score(

            result.get(

                "falcon_score",

                0

            )

        )


        return result
