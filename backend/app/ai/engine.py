from typing import Dict, Any, Optional
import logging
import time

from app.ai.signals_engine import SignalEngine
from app.ai.explanation_engine import ExplanationEngine
from app.ai.learning import LearningEngine
from app.ai.assistant import FalconAssistant


logger = logging.getLogger(__name__)


class AIEngine:
    """
    FalconAI Core AI Orchestration Engine.

    مسؤول عن:
    - تشغيل محرك الإشارات
    - تشغيل الشرح الذكي
    - تحديث التعلم من النتائج
    - تشغيل مساعد FalconAI
    - مراقبة حالة المحرك
    """

    def __init__(self):

        self.signal_engine = SignalEngine()
        self.explanation_engine = ExplanationEngine()
        self.learning_engine = LearningEngine()
        self.assistant = FalconAssistant()

        self.started_at = time.time()
        self.requests_count = 0
        self.status = "running"


    def analyze(
        self,
        symbol: str,
        interval: str,
        market: str,
        user_type: str = "trader",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:

        try:

            self.requests_count += 1

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
                "success": True,
                "symbol": symbol,
                "interval": interval,
                "market": market,
                "user_id": user_id,
                "analysis": analysis,
                "explanation": explanation,
                "assistant": assistant_response,
                "engine_status": self.status
            }


        except Exception as error:

            logger.exception(
                "FalconAI analysis error: %s",
                error
            )

            return {
                "success": False,
                "error": str(error),
                "symbol": symbol,
                "market": market
            }



    def learn_from_result(
        self,
        prediction: Dict[str, Any],
        actual_result: Dict[str, Any]
    ) -> Dict[str, Any]:

        try:

            result = self.learning_engine.update(
                prediction=prediction,
                actual_result=actual_result
            )

            return {
                "success": True,
                "learning_result": result
            }


        except Exception as error:

            logger.exception(
                "FalconAI learning error: %s",
                error
            )

            return {
                "success": False,
                "error": str(error)
            }



    def health_check(self) -> Dict[str, Any]:

        uptime = int(
            time.time() - self.started_at
        )

        return {
            "engine": "AIEngine",
            "status": self.status,
            "requests": self.requests_count,
            "uptime_seconds": uptime
            }
