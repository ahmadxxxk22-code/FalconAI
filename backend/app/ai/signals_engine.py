from datetime import datetime


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



class SignalEngine:


    def __init__(self):

        # تحليل السوق الأساسي
        self.market = MarketAnalyzer()


        # الاتجاه
        self.trend = TrendEngine()


        # النماذج السعرية
        self.patterns = PatternAnalyzer()


        # Smart Money / Liquidity
        self.smart_money = SmartMoneyAnalyzer()


        # التوقع
        self.prediction = PredictionEngine()


        # إدارة المخاطر
        self.risk = RiskManager()


        # الأخبار والاقتصاد
        self.news = NewsAnalyzer()


        # فيبوناتشي
        self.fibonacci = FibonacciAnalyzer()


        # محرك الفرص
        self.opportunity = OpportunityEngine()


        # تحليل كل الفريمات
        self.multi_timeframe = MultiTimeframeEngine()



    # =====================================
    # التحليل الرئيسي
    # =====================================


    def analyze(

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

            candles=market_data.get(

                "candles",

                []

            )

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



        # كشف الترند قبل حدوثه
        early_trend = self.detect_early_trend(

            market_data,

            opportunity,

            smart_money,

            multi_timeframe

        )



        confidence, confidence_details = self.calculate_confidence(

            trend,

            multi_timeframe,

            opportunity,

            smart_money,

            prediction,

            market_data,

            fibonacci,

            news,

            patterns

        )



        direction, reasons, warnings = self.make_decision(

            trend,

            multi_timeframe,

            opportunity,

            smart_money,

            prediction,

            market_data,

            fibonacci,

            news,

            early_trend

        )



        risk = self.risk.calculate(

            direction=direction,

            price=market_data["price"],

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

            market_state=market_data.get(

                "market_state",

                "UNKNOWN"

            ),

            smart_money=smart_money,

            fibonacci=fibonacci,

            market=market

        )


        return {

            "symbol": symbol,

            "interval": interval,

            "market": market,

            "direction": direction,

            "confidence": confidence,

            "confidence_details": confidence_details,

            "decision_reasons": reasons,

            "warnings": warnings,

            "early_trend": early_trend,

            "price": market_data.get(
                "price"
            ),

            "market_analysis": market_data,

            "trend": trend,

            "multi_timeframe": multi_timeframe,

            "opportunity": opportunity,

            "smart_money": smart_money,

            "prediction": prediction,

            "patterns": patterns,

            "fibonacci": fibonacci,

            "news": news,

            "risk": risk,

            "created_at": datetime.utcnow().isoformat()

        }

    # =====================================
    # حساب قوة الإشارة
    # =====================================

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

        patterns

    ):


        score = 0

        details = []



        # ==========================
        # Trend 25%
        # ==========================

        trend_score = abs(

            trend.get(
                "score",
                0
            )

        )


        if trend_score >= 70:

            score += 25

            details.append(
                "اتجاه قوي جداً"
            )


        elif trend_score >= 35:

            score += 15

            details.append(
                "اتجاه واضح"
            )



        # ==========================
        # Multi Timeframe 20%
        # ==========================

        mtf_conf = multi_timeframe.get(

            "confidence",

            0

        )


        if mtf_conf >= 80:

            score += 20

            details.append(
                "توافق قوي بين الفريمات"
            )


        elif mtf_conf >= 50:

            score += 10

            details.append(
                "توافق متوسط بين الفريمات"
            )



        # ==========================
        # Smart Money 20%
        # ==========================

        smart_conf = smart_money.get(

            "confidence",

            0

        )


        if smart_conf >= 80:

            score += 20

            details.append(
                "Smart Money قوي"
            )


        elif smart_conf >= 50:

            score += 10



        # ==========================
        # Opportunity 15%
        # ==========================

        opp_conf = opportunity.get(

            "confidence",

            0

        )


        if opp_conf >= 70:

            score += 15

            details.append(
                "فرصة تداول قوية"
            )


        elif opp_conf >= 40:

            score += 8



        # ==========================
        # Market Structure 10%
        # ==========================

        if market.get(

            "volume_power",

            0

        ) > 1:


            score += 5

            details.append(
                "حجم تداول داعم"
            )



        if market.get(

            "momentum",

            0

        ) > 0:


            score += 5



        # ==========================
        # News + Fibonacci
        # ==========================

        if news.get(

            "confidence",

            0

        ) >= 70:


            score += 5


            details.append(
                "الأخبار مؤثرة"
            )



        if fibonacci.get(

            "signal"

        ) != "WAIT":


            score += 5

            details.append(
                "فيبوناتشي يدعم منطقة"
            )



        # ==========================
        # Pattern
        # ==========================

        if patterns.get(

            "confidence",

            0

        ) >= 30:


            score += 5



        return (

            min(score,100),

            details

        )





    # =====================================
    # كشف الترند المبكر
    # =====================================


    def detect_early_trend(

        self,

        market,

        opportunity,

        smart_money,

        multi_timeframe

    ):


        bullish = 0

        bearish = 0



        if market.get(

            "momentum",

            0

        ) > 0:

            bullish += 1


        else:

            bearish += 1



        if opportunity.get(

            "signal"

        ) == "BUY":

            bullish += 2


        elif opportunity.get(

            "signal"

        ) == "SELL":

            bearish += 2



        if smart_money.get(

            "bullish",

            False

        ):

            bullish += 2



        if smart_money.get(

            "bearish",

            False

        ):

            bearish += 2



        mtf = multi_timeframe.get(

            "signal",

            "WAIT"

        )


        if mtf in [

            "BUY",

            "STRONG_BUY"

        ]:

            bullish += 1



        if mtf in [

            "SELL",

            "STRONG_SELL"

        ]:

            bearish += 1



        if bullish >= 4:

            return "EARLY_BULLISH"



        if bearish >= 4:

            return "EARLY_BEARISH"



        return "NO_EARLY_SIGNAL"


    # =====================================
    # اتخاذ القرار النهائي
    # =====================================


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

        early_trend

    ):


        bullish = 0

        bearish = 0


        reasons = []

        warnings = []



        # ==========================
        # Trend
        # ==========================


        trend_score = trend.get(

            "score",

            0

        )


        if trend_score > 0:

            bullish += 2

            reasons.append(
                "الاتجاه العام صاعد"
            )


        elif trend_score < 0:

            bearish += 2

            reasons.append(
                "الاتجاه العام هابط"
            )



        # ==========================
        # Multi Timeframe
        # ==========================


        mtf_signal = multi_timeframe.get(

            "signal",

            "WAIT"

        )


        if mtf_signal in [

            "BUY",

            "STRONG_BUY"

        ]:

            bullish += 3

            reasons.append(
                "كل الفريمات تدعم الصعود"
            )


        elif mtf_signal in [

            "SELL",

            "STRONG_SELL"

        ]:

            bearish += 3

            reasons.append(
                "كل الفريمات تدعم الهبوط"
            )



        # ==========================
        # Opportunity Engine
        # ==========================


        opp_signal = opportunity.get(

            "signal",

            "WAIT"

        )


        if opp_signal == "BUY":

            bullish += 2

            reasons.append(
                "Opportunity Engine BUY"
            )


        elif opp_signal == "SELL":

            bearish += 2

            reasons.append(
                "Opportunity Engine SELL"
            )



        # ==========================
        # Smart Money
        # ==========================


        smart_bull = smart_money.get(

            "bullish",

            False

        )


        smart_bear = smart_money.get(

            "bearish",

            False

        )


        if smart_bull:

            bullish += 2

            reasons.append(
                "Smart Money accumulation"
            )


        if smart_bear:

            bearish += 2

            reasons.append(
                "Smart Money distribution"
            )



        # ==========================
        # Prediction
        # ==========================


        if prediction.get(

            "bullish",

            False

        ):

            bullish += 1



        if prediction.get(

            "bearish",

            False

        ):

            bearish += 1




        # ==========================
        # Fibonacci
        # ==========================


        if fibonacci.get(

            "signal"

        ) == "BUY":

            bullish += 1

            reasons.append(
                "Fibonacci supports BUY"
            )


        elif fibonacci.get(

            "signal"

        ) == "SELL":

            bearish += 1

            reasons.append(
                "Fibonacci supports SELL"
            )



        # ==========================
        # News
        # ==========================


        if news.get(

            "bullish",

            False

        ):

            bullish += 1



        if news.get(

            "bearish",

            False

        ):

            bearish += 1



        # ==========================
        # كشف التعارض
        # ==========================


        conflict = False


        if (

            bullish >= 4

            and

            bearish >= 4

        ):

            conflict = True


            warnings.append(

                "تعارض بين التحليلات"

            )



        if conflict:

            return (

                "WAIT",

                reasons,

                warnings

            )



        # ==========================
        # قرار نهائي
        # ==========================


        if bullish >= 5 and bullish > bearish:


            reasons.append(

                "توافق عدة محركات للشراء"

            )


            return (

                "BUY",

                reasons,

                warnings

            )



        if bearish >= 5 and bearish > bullish:


            reasons.append(

                "توافق عدة محركات للبيع"

            )


            return (

                "SELL",

                reasons,

                warnings

            )



        warnings.append(

            "لا يوجد توافق كافي"

        )


        return (

            "WAIT",

            reasons,

            warnings

        )
