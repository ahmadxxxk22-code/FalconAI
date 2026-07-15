from app.ai.signals_engine import SignalEngine
from app.ai.explanation_engine import ExplanationEngine
from app.ai.learning import LearningEngine
from app.ai.assistant import FalconAssistant


class AIEngine:


    def __init__(self):

        # المحرك الرئيسي للتحليل
        self.signal_engine = SignalEngine()


        # شرح التحليل حسب نوع المستخدم
        self.explanation = ExplanationEngine()


        # نظام التعلم
        self.learning = LearningEngine()


        # مساعد FalconAI
        self.assistant = FalconAssistant()



    def analyze(
        self,
        symbol="BTCUSDT",
        interval="1h",
        market="crypto",
        user_type="trader"
    ):


        # التحليل الكامل من SignalEngine
        analysis = self.signal_engine.analyze(

            symbol=symbol,

            interval=interval,

            market=market

        )



        # شرح النتيجة
        explanation = self.explanation.explain(

            analysis,

            user_type=user_type

        )



        # مساعد FalconAI
        assistant = self.assistant.explain(

            analysis

        )



        return {


            "analysis": analysis,


            "explanation": explanation,


            "assistant": assistant

        }
