from typing import Dict, Any

from app.ai.signals_engine import SignalEngine
from app.ai.explanation_engine import ExplanationEngine
from app.ai.learning import LearningEngine
from app.ai.assistant import FalconAssistant


class AIEngine:
    """
    Main FalconAI orchestration engine.

    مسؤول عن:
    - تشغيل محرك الإشارات
    - شرح التحليل
    - التعلم من النتائج
    - مساعد FalconAI
    """

    def __init__(self):
        self.signal_engine = SignalEngine()
        self.explanation_engine = ExplanationEngine()
        self.learning_engine = LearningEngine()
        self.assistant = FalconAssistant()


    def analyze(
        self,
        symbol: str,
        interval: str,
        market: str,
        user_type: str = "trader",
        user_id: str | None = None
    ) -> Dict[str, Any]:

        analysis = self.signal_engine.analyze(
            symbol=symbol,
            interval=interval,
            market=market
        )

        explanation = self.explanation_engine.explain(
            analysis,
            user_type=user_type
        )

        assistant_response = self.assistant.explain(
            analysis
        )

        return {
            "symbol": symbol,
            "interval": interval,
            "market": market,
            "analysis": analysis,
            "explanation": explanation,
            "assistant": assistant_response
        }


    def learn_from_result(
        self,
        prediction: Dict[str, Any],
        actual_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        تحديث التعلم بعد معرفة نتيجة التحليل.
        """

        return self.learning_engine.update(
            prediction=prediction,
            actual_result=actual_result
        )


    def health_check(self) -> Dict[str, str]:
        return {
            "engine": "AIEngine",
            "status": "running"
        }
