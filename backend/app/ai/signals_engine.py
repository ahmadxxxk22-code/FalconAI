from datetime import datetime
from typing import Dict, Any, Optional


from app.ai.market_analyzer import MarketAnalyzer
from app.ai.trend_engine import TrendEngine
from app.ai.patterns import PatternAnalyzer
from app.ai.smart_money import SmartMoneyAnalyzer
from app.ai.prediction import PredictionEngine
from app.ai.risk_manager import RiskManager
from app.ai.news_ai import NewsAnalyzer
from app.ai.fibonacci import FibonacciAnalyzer


from app.ai.opportunity.opportunity_engine import OpportunityEngine
from app.ai.multi_timeframe_engine import MultiTimeframeEngine

from app.ai.opportunity.volume_engine import VolumeEngine
from app.ai.opportunity.liquidity_engine import LiquidityEngine
from app.ai.opportunity.order_blocks import OrderBlocksEngine
from app.ai.opportunity.candles_ai import CandlesAI
from app.ai.opportunity.historical_learning import HistoricalLearning


# Economic Intelligence

try:

    from app.ai.economic_calendar import EconomicCalendar

except Exception:

    EconomicCalendar = None





# =====================================================
# FALCONAI SIGNAL ENGINE
# =====================================================


class SignalEngine:


    """
    FalconAI Advanced Signal Intelligence Engine


    مسؤول عن دمج:

    - Technical Analysis
    - Trend Intelligence
    - Smart Money
    - Market Structure
    - Opportunity Detection
    - Multi Timeframe
    - Economic Intelligence
    - News Analysis
    - Risk Management
    - Historical Learning


    لا ينفذ تداولات

    فقط يحلل ويصدر قرار ذكي
    """



    def __init__(
        self
    ):



        # =========================================
        # Core AI Engines
        # =========================================


        self.market = MarketAnalyzer()

        self.trend = TrendEngine()

        self.patterns = PatternAnalyzer()

        self.smart_money = SmartMoneyAnalyzer()

        self.prediction = PredictionEngine()

        self.risk = RiskManager()

        self.news = NewsAnalyzer()

        self.fibonacci = FibonacciAnalyzer()



        # =========================================
        # Opportunity Intelligence
        # =========================================


        self.opportunity = OpportunityEngine()

        self.multi_timeframe = MultiTimeframeEngine()

        self.volume = VolumeEngine()

        self.liquidity = LiquidityEngine()

        self.order_blocks = OrderBlocksEngine()

        self.candles_ai = CandlesAI()

        self.history = HistoricalLearning()



        # =========================================
        # Economic Intelligence
        # =========================================


        self.enable_economic_filter = True


        if self.enable_economic_filter:
    

           self.economic = EconomicCalendar()


        else:


            self.economic = None




        # =========================================
        # Decision Settings
        # =========================================


        self.minimum_confidence = 60


        self.minimum_signal_score = 6


        self.maximum_confidence = 100



        self.allow_counter_trend = False




        # =========================================
        # Filters
        # =========================================


        self.enable_news_filter = True

        self.enable_economic_filter = True

        self.enable_fibonacci_filter = True

        self.enable_smart_money_filter = True

        self.enable_volume_filter = True

        self.enable_liquidity_filter = True

        self.enable_orderblock_filter = True

        self.enable_candle_filter = True

        self.enable_history_filter = True

        self.enable_mtf_filter = True




        # =========================================
        # Intelligence Weights
        # =========================================


        self.weights = {


            "smart_money": 15,


            "prediction": 10,


            "patterns": 5,


            "market": 5,


            "news": 5,


            "economic": 10,


            "fibonacci": 5,


            "volume": 5,


            "liquidity": 5,


            "order_blocks": 5,


            "candles": 5,


            "history": 5

        }




        # =========================================
        # Statistics
        # =========================================


        self.signal_statistics = {


            "buy": 0,


            "sell": 0,


            "wait": 0,


            "success": 0,


            "failed": 0

        }



        self.version = "FalconAI Signal Engine V1.0"



# =====================================================
# MAIN AI SIGNAL ANALYSIS
# =====================================================


    def analyze(
        self,
        symbol: str = "BTCUSDT",
        interval: str = "1h",
        market: str = "crypto",
        economic_event: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:


        signal_id = (

            f"{symbol}_"

            f"{interval}_"

            f"{datetime.utcnow().timestamp()}"

        )



        # =====================================
        # MARKET DATA
        # =====================================


        market_data = self.market.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )



        candles = market_data.get(

            "candles",

            []

        )



        data_quality = self.evaluate_data_quality(

            candles

        )



        # =====================================
        # MARKET INTELLIGENCE MODULES
        # =====================================


        volume_analysis = self.volume.analyze(

            candles

        )


        liquidity_analysis = self.liquidity.analyze(

            candles

        )


        order_blocks_analysis = self.order_blocks.analyze(

            candles

        )


        candle_analysis = self.candles_ai.analyze(

            candles

        )


        historical_analysis = self.history.analyze(

            candles

        )



        # =====================================
        # CORE AI ENGINES
        # =====================================


        trend = self.trend.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )



        multi_timeframe = self.multi_timeframe.analyze(

            symbol=symbol,

            market=market

        )



        opportunity = self.opportunity.analyze(

            symbol=symbol,

            candles=candles

        )



        smart_money = self.smart_money.analyze(

            symbol,

            interval

        )



        prediction = self.prediction.predict(

            symbol=symbol,

            interval=interval,

            market=market

        )



        patterns = self.patterns.analyze(

            symbol,

            interval

        )



        fibonacci = self.fibonacci.analyze(

            symbol,

            interval

        )



        news = self.news.analyze(

            symbol

        )



        # =====================================
        # ECONOMIC INTELLIGENCE
        # =====================================


        economic = {


            "available":

                False,


            "risk":

                "UNKNOWN"

        }



        if (

            self.enable_economic_filter

            and

            self.economic

        ):


            economic = self.economic.analyze(

                economic_event

            )




        # =====================================
        # MARKET REGIME
        # =====================================


        market_regime = self.detect_market_regime(

            market_data,

            trend,

            multi_timeframe

        )




        # =====================================
        # EARLY TREND
        # =====================================


        early_trend = self.detect_early_trend(

            market_data,

            opportunity,

            smart_money,

            multi_timeframe,

            volume_analysis,

            liquidity_analysis,

            order_blocks_analysis,

            candle_analysis,

            historical_analysis

        )




        # =====================================
        # CONFIDENCE FUSION
        # =====================================


        confidence, confidence_details = self.calculate_confidence(

            trend,

            multi_timeframe,

            opportunity,

            smart_money,

            prediction,

            market_data,

            fibonacci,

            news,

            patterns,

            volume_analysis,

            liquidity_analysis,

            order_blocks_analysis,

            candle_analysis,

            historical_analysis,

            economic

        )




        # =====================================
        # FINAL DECISION
        # =====================================


        decision = self.make_decision(

            trend,

            multi_timeframe,

            opportunity,

            smart_money,

            prediction,

            market_data,

            fibonacci,

            news,

            early_trend,

            volume_analysis,

            liquidity_analysis,

            order_blocks_analysis,

            candle_analysis,

            historical_analysis,

            economic,

            market_regime

        )



        direction = decision.get(

            "signal",

            "WAIT"

        )




        # =====================================
        # RISK MANAGEMENT
        # =====================================


        risk = self.risk.calculate(

            direction=direction,

            price=market_data.get(

                "price",

                0

            ),

            confidence=confidence,

            atr=market_data.get(

                "atr",

                0

            ),

            volatility=market_data.get(

                "volatility",

                0

            ),

            trend_strength=market_data.get(

                "trend_strength",

                0

            ),

            market_state=market_regime,

            smart_money=smart_money,

            fibonacci=fibonacci,

            market=market

        )




        # =====================================
        # FINAL RESPONSE
        # =====================================


        report = {


            "signal_id":

                signal_id,


            "engine":

                self.version,


            "symbol":

                symbol,


            "interval":

                interval,


            "market":

                market,


            "market_regime":

                market_regime,


            "data_quality":

                data_quality,



            "signal":

                direction,


            "confidence":

                confidence,


            "confidence_details":

                confidence_details,



            "decision":

                decision,



            "risk":

                risk,



            "economic":

                economic,



            "modules": {


                "market":

                    market_data,


                "trend":

                    trend,


                "multi_timeframe":

                    multi_timeframe,


                "opportunity":

                    opportunity,


                "smart_money":

                    smart_money,


                "prediction":

                    prediction,


                "patterns":

                    patterns,


                "fibonacci":

                    fibonacci,


                "news":

                    news,


                "volume":

                    volume_analysis,


                "liquidity":

                    liquidity_analysis,


                "order_blocks":

                    order_blocks_analysis,


                "candles":

                    candle_analysis,


                "history":

                    historical_analysis

            },


            "created_at":

                datetime.utcnow().isoformat()

        }



        return report



# =====================================================
# DATA QUALITY ENGINE
# =====================================================


    def evaluate_data_quality(
        self,
        candles
    ) -> Dict[str, Any]:


        count = len(candles)



        quality = "LOW"

        score = 0



        if count >= 200:

            quality = "EXCELLENT"

            score = 100



        elif count >= 100:

            quality = "GOOD"

            score = 80



        elif count >= 50:

            quality = "ACCEPTABLE"

            score = 60



        elif count >= 20:

            quality = "WEAK"

            score = 40




        return {

            "quality": quality,

            "score": score,

            "candles": count

        }




# =====================================================
# MARKET REGIME DETECTION
# =====================================================


    def detect_market_regime(
        self,
        market,
        trend,
        multi_timeframe
    ) -> str:


        trend_score = abs(

            trend.get(

                "score",

                0

            )

        )



        mtf_confidence = multi_timeframe.get(

            "confidence",

            0

        )



        volatility = market.get(

            "volatility",

            0

        )



        if (

            trend_score >= 70

            and

            mtf_confidence >= 70

        ):

            return "TRENDING"



        if volatility > 5:

            return "HIGH_VOLATILITY"



        return "RANGING"




# =====================================================
# AI CONFIDENCE FUSION ENGINE
# =====================================================


    def calculate_confidence(
        self,
        trend,
        multi_timeframe,
        opportunity,
        smart_money,
        prediction,
        market,
        fibonacci,
        news,
        patterns,
        volume_analysis,
        liquidity_analysis,
        order_blocks_analysis,
        candle_analysis,
        historical_analysis,
        economic
    ):


        confidence = 0

        details = []



        engines = {


            "trend": trend,


            "multi_timeframe": multi_timeframe,


            "opportunity": opportunity,


            "smart_money": smart_money,


            "prediction": prediction,


            "market": market,


            "news": news,


            "fibonacci": fibonacci,


            "volume": volume_analysis,


            "liquidity": liquidity_analysis,


            "order_blocks": order_blocks_analysis,


            "candles": candle_analysis,


            "history": historical_analysis

        }



        for name, data in engines.items():


            weight = self.weights.get(

                name,

                0

            )


            if not data:

                continue



            engine_confidence = data.get(

                "confidence",

                0

            )



            contribution = (

                engine_confidence

                *

                weight

                /

                100

            )



            confidence += contribution



            if engine_confidence >= 70:

                details.append(

                    f"{name} strong"

                )



        # Economic adjustment


        if economic.get(

            "available",

            False

        ):


            risk = economic.get(

                "risk",

                ""

            )


            if risk in [

                "HIGH",

                "EXTREME"

            ]:


                confidence -= 10

                details.append(

                    "Economic risk reduced confidence"

                )




        return (

            int(

                max(

                    0,

                    min(

                        confidence,

                        100

                    )

                )

            ),

            details

        )




# =====================================================
# WEIGHTED AI DECISION ENGINE
# =====================================================


    def make_decision(
        self,
        trend,
        multi_timeframe,
        opportunity,
        smart_money,
        prediction,
        market,
        fibonacci,
        news,
        early_trend,
        volume_analysis,
        liquidity_analysis,
        order_blocks_analysis,
        candle_analysis,
        historical_analysis,
        economic,
        market_regime
    ):


        bullish_score = 0

        bearish_score = 0


        reasons = []

        warnings = []



        modules = {


            "trend": trend,


            "multi_timeframe": multi_timeframe,


            "opportunity": opportunity,


            "smart_money": smart_money,


            "prediction": prediction,


            "fibonacci": fibonacci,


            "news": news,


            "volume": volume_analysis,


            "liquidity": liquidity_analysis,


            "order_blocks": order_blocks_analysis,


            "candles": candle_analysis,


            "history": historical_analysis

        }




        for name, data in modules.items():


            if not data:

                continue



            weight = self.weights.get(

                name,

                0

            )



            signal = data.get(

                "signal",

                "WAIT"

            )



            if signal in [

                "BUY",

                "BULLISH",

                "STRONG_BUY"

            ]:


                bullish_score += weight

                reasons.append(

                    f"{name} supports BUY"

                )



            elif signal in [

                "SELL",

                "BEARISH",

                "STRONG_SELL"

            ]:


                bearish_score += weight

                reasons.append(

                    f"{name} supports SELL"

                )




        # Early movement


        if early_trend == "EARLY_BULLISH":

            bullish_score += 5



        elif early_trend == "EARLY_BEARISH":

            bearish_score += 5




        # Economic protection


        if economic.get(

            "risk"

        ) in [

            "HIGH",

            "EXTREME"

        ]:


            warnings.append(

                "High economic risk"

            )



        # Conflict protection


        difference = abs(

            bullish_score

            -

            bearish_score

        )



        if difference < 10:


            return {


                "signal":

                    "WAIT",


                "bullish_score":

                    bullish_score,


                "bearish_score":

                    bearish_score,


                "reasons":

                    reasons,


                "warnings":

                    warnings + [

                        "AI conflict detected"

                    ]

            }




        if bullish_score > bearish_score:


            signal = "BUY"



        else:

            signal = "SELL"




        return {


            "signal":

                signal,


            "bullish_score":

                bullish_score,


            "bearish_score":

                bearish_score,


            "market_regime":

                market_regime,


            "reasons":

                reasons,


            "warnings":

                warnings

        }
