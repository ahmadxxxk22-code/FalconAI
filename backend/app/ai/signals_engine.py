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

        self.market = MarketAnalyzer()

        self.trend = TrendEngine()

        self.patterns = PatternAnalyzer()

        self.smart_money = SmartMoneyAnalyzer()

        self.prediction = PredictionEngine()

        self.risk = RiskManager()

        self.news = NewsAnalyzer()

        self.fibonacci = FibonacciAnalyzer()

        self.opportunity = OpportunityEngine()

        # تحليل جميع الفريمات من المضارب للمستثمر
        self.multi_timeframe = MultiTimeframeEngine()



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



        # تحليل توافق جميع الفريمات
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



        trend = self.trend.analyze(
            symbol=symbol,
            interval=interval,
            market=market
        )



        patterns = self.patterns.analyze(
            symbol,
            interval
        )



        smart = self.smart_money.analyze(
            symbol,
            interval
        )



        prediction = self.prediction.predict(
            symbol=symbol,
            interval=interval,
            market=market
        )



        news = self.news.analyze(
            symbol
        )



        fibo = self.fibonacci.analyze(
            symbol,
            interval
        )



        confidence, confidence_details = self.calculate_confidence(

            trend,

            market_data,

            patterns,

            smart,

            prediction,

            news,

            fibo,

            opportunity,

            multi_timeframe

        )



        direction, decision_reasons = self.choose_direction(

            trend,

            market_data,

            prediction,

            smart,

            patterns,

            fibo,

            news,

            opportunity,

            multi_timeframe

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

            smart_money=smart,

            fibonacci=fibo,

            market=market

        )



        return {

            "symbol": symbol,

            "interval": interval,

            "direction": direction,

            "confidence": confidence,

            "confidence_details": confidence_details,

            "decision_reasons": decision_reasons,


            "price": market_data["price"],


            "trend": trend,

            "market": market_data,

            "patterns": patterns,

            "smart_money": smart,

            "prediction": prediction,

            "opportunity": opportunity,

            "multi_timeframe": multi_timeframe,

            "news": news,

            "fibonacci": fibo,

            "risk": risk,


            "created_at": datetime.utcnow().isoformat()

        }

    def calculate_confidence(

        self,

        trend,

        market,

        patterns,

        smart,

        prediction,

        news,

        fibo,

        opportunity,

        multi_timeframe

    ):


        score = 0

        details = []



        trend_score = trend.get(
            "score",
            0
        )



        if abs(trend_score) > 50:

            score += 20

            details.append(
                "قوة الاتجاه عالية"
            )


        elif abs(trend_score) > 20:

            score += 10

            details.append(
                "الاتجاه متوسط القوة"
            )



        if market.get(
            "market_state"
        ) in [

            "BULLISH_TREND",

            "BEARISH_TREND"

        ]:

            score += 15

            details.append(
                "السوق في اتجاه واضح"
            )



        if prediction.get(
            "confidence",
            0
        ) > 50:

            score += 15

            details.append(
                "التنبؤ يدعم الاتجاه"
            )



        if smart.get(
            "confidence",
            0
        ) >= 50:

            score += 15

            details.append(
                "Smart Money يدعم القرار"
            )



        if patterns.get(
            "strength",
            0
        ) > 50:

            score += 10

            details.append(
                "نمط سعري قوي"
            )



        if news.get(
            "confidence",
            0
        ) >= 60:

            score += 10

            details.append(
                "الأخبار لها تأثير"
            )



        if fibo.get(
            "bullish",
            False
        ) or fibo.get(
            "bearish",
            False
        ):

            score += 15

            details.append(
                "فيبوناتشي يدعم منطقة مهمة"
            )



        if opportunity.get(
            "confidence",
            0
        ) >= 50:

            score += 20

            details.append(
                "Opportunity Engine يدعم القرار"
            )



        # توافق الفريمات المتعددة
        mtf_confidence = multi_timeframe.get(
            "confidence",
            0
        )


        if mtf_confidence >= 70:

            score += 20

            details.append(
                "توافق قوي بين الفريمات"
            )


        elif mtf_confidence >= 50:

            score += 10

            details.append(
                "توافق متوسط بين الفريمات"
            )



        return min(
            score,
            100
        ), details

    def choose_direction(

        self,

        trend,

        market,

        prediction,

        smart,

        patterns,

        fibo,

        news,

        opportunity,

        multi_timeframe

    ):


        bullish = 0

        bearish = 0


        reasons = []



        trend_score = trend.get(
            "score",
            0
        )



        if trend_score > 0:

            bullish += 2

            reasons.append(
                "الاتجاه العام إيجابي"
            )


        elif trend_score < 0:

            bearish += 2

            reasons.append(
                "الاتجاه العام سلبي"
            )



        for item in [

            prediction,

            smart,

            patterns,

            fibo,

            news

        ]:


            if item.get(
                "bullish",
                False
            ):

                bullish += 1



            if item.get(
                "bearish",
                False
            ):

                bearish += 1




        if opportunity.get(
            "signal"
        ) == "BUY":

            bullish += 2

            reasons.append(
                "Opportunity Engine BUY"
            )


        elif opportunity.get(
            "signal"
        ) == "SELL":

            bearish += 2

            reasons.append(
                "Opportunity Engine SELL"
            )



        # إضافة توافق الفريمات
        mtf_signal = multi_timeframe.get(
            "signal",
            "WAIT"
        )


        if mtf_signal in [

            "BUY",

            "STRONG_BUY"

        ]:

            bullish += 2

            reasons.append(
                "الفريمات الزمنية تدعم الصعود"
            )


        elif mtf_signal in [

            "SELL",

            "STRONG_SELL"

        ]:

            bearish += 2

            reasons.append(
                "الفريمات الزمنية تدعم الهبوط"
            )



        if market.get(
            "bullish",
            False
        ):

            bullish += 1



        if market.get(
            "bearish",
            False
        ):

            bearish += 1




        if bullish >= 4 and bullish > bearish:

            reasons.append(
                "توافق عدة عوامل للشراء"
            )

            return "BUY", reasons



        if bearish >= 4 and bearish > bullish:

            reasons.append(
                "توافق عدة عوامل للبيع"
            )

            return "SELL", reasons



        reasons.append(
            "لا يوجد توافق كافٍ للدخول"
        )


        return "WAIT", reasons
