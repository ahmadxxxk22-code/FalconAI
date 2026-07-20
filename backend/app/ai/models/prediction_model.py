# backend/app/ai/models/prediction_model.py


from typing import (

    Dict,

    Any,

    List,

    Optional

)


from datetime import datetime


from pydantic import (

    BaseModel,

    Field

)



# =====================================================
# FalconAI Prediction Model
# Core AI Output Schema
# =====================================================



class ProbabilityModel(BaseModel):

    """
    احتمالات الاتجاه
    """

    bullish: float = Field(

        default=0,

        ge=0,

        le=100

    )


    bearish: float = Field(

        default=0,

        ge=0,

        le=100

    )




class ScoreModel(BaseModel):

    """
    نقاط المحركات الداخلية
    """

    bullish: float = 0


    bearish: float = 0




class MarketContextModel(BaseModel):

    """
    حالة السوق العامة
    """

    regime: str = "UNKNOWN"


    volatility: float = 0


    trend: str = "SIDEWAYS"



class ReasonModel(BaseModel):

    """
    أسباب القرار
    """

    reasons: List[str] = []


    conflicts: List[str] = []



class PredictionModel(BaseModel):

    """
    النموذج الأساسي لتنبؤ FalconAI

    يستخدم بين:
    - Prediction Engine
    - API
    - Mobile App
    - Historical Learning
    """



    symbol: str



    market: str = "crypto"



    interval: str = "1h"



    signal: str = "WAIT"



    direction: str = "NEUTRAL"



    confidence: float = Field(

        default=0,

        ge=0,

        le=100

    )


    probability: ProbabilityModel = ProbabilityModel()



    quality: str = "WEAK"



    scores: ScoreModel = ScoreModel()



    market_context: MarketContextModel = MarketContextModel()



    reasons: List[str] = []



    conflicts: List[str] = []



    created_at: str = Field(

        default_factory=lambda:

            datetime.utcnow().isoformat()

  )



# =====================================================
# ADVANCED INTELLIGENCE MODELS
# =====================================================



class RiskModel(BaseModel):

    """
    نموذج إدارة المخاطر
    """

    risk_level: str = "LOW"


    stop_loss: Optional[float] = None


    take_profit: Optional[float] = None


    risk_reward: float = 0



class TechnicalModel(BaseModel):

    """
    التحليل الفني
    """

    rsi: float = 50


    macd: float = 0


    momentum: float = 0


    volume_ratio: float = 1


    ema_fast: Optional[float] = None


    ema_slow: Optional[float] = None




class EarlyMoveModel(BaseModel):

    """
    كشف الحركة المبكرة
    """

    detected: bool = False


    direction: str = "NONE"


    probability: float = 0


    score: float = 0


    reasons: List[str] = []




class ReversalModel(BaseModel):

    """
    احتمال الانعكاس
    """

    detected: bool = False


    probability: float = 0


    score: float = 0


    reasons: List[str] = []




class BreakoutModel(BaseModel):

    """
    ذكاء الاختراق
    """

    detected: bool = False


    breakout_type: str = "NONE"


    probability: float = 0


    level: Optional[float] = None


    reasons: List[str] = []




class SmartMoneyModel(BaseModel):

    """
    تحليل الأموال الذكية
    """

    available: bool = False


    direction: str = "NONE"


    strength: float = 0


    signals: List[str] = []




class LiquidityModel(BaseModel):

    """
    تحليل السيولة
    """

    available: bool = False


    liquidity_zone: Optional[str] = None


    strength: float = 0


    warnings: List[str] = []




class OrderBlockModel(BaseModel):

    """
    مناطق Order Blocks
    """

    available: bool = False


    bullish_blocks: List[Dict[str, Any]] = []


    bearish_blocks: List[Dict[str, Any]] = []




class FibonacciModel(BaseModel):

    """
    مستويات Fibonacci
    """

    available: bool = False


    support_levels: List[float] = []


    resistance_levels: List[float] = []



class EconomicImpactModel(BaseModel):

    """
    تأثير الأخبار والاقتصاد
    """

    available: bool = False


    event: Optional[str] = None


    impact: str = "NONE"


    risk_score: float = 0




class LearningFeedbackModel(BaseModel):

    """
    بيانات التعلم من النتائج السابقة
    """

    evaluated: bool = False


    prediction_correct: Optional[bool] = None


    reward: float = 0


    feedback: Dict[str, Any] = {}



class MultiTimeframeModel(BaseModel):

    """
    تحليل جميع الفريمات
    """

    timeframes: Dict[str, Any] = {}



# =====================================================
# ADVANCED PREDICTION RESPONSE MODEL
# =====================================================



class PredictionResponseModel(BaseModel):

    """
    النموذج النهائي الذي يخرج من FalconAI
    """

    symbol: str


    market: str


    interval: str



    signal: str = "WAIT"


    direction: str = "NEUTRAL"



    confidence: float = Field(

        default=0,

        ge=0,

        le=100

    )



    probability: ProbabilityModel = Field(

        default_factory=ProbabilityModel

    )



    quality: str = "WEAK"



    scores: ScoreModel = Field(

        default_factory=ScoreModel

    )



    technical: TechnicalModel = Field(

        default_factory=TechnicalModel

    )



    market_context: MarketContextModel = Field(

        default_factory=MarketContextModel

    )



    risk: RiskModel = Field(

        default_factory=RiskModel

    )



    early_move: EarlyMoveModel = Field(

        default_factory=EarlyMoveModel

    )



    reversal: ReversalModel = Field(

        default_factory=ReversalModel

    )



    breakout: BreakoutModel = Field(

        default_factory=BreakoutModel

    )



    smart_money: SmartMoneyModel = Field(

        default_factory=SmartMoneyModel

    )



    liquidity: LiquidityModel = Field(

        default_factory=LiquidityModel

    )



    order_blocks: OrderBlockModel = Field(

        default_factory=OrderBlockModel

    )



    fibonacci: FibonacciModel = Field(

        default_factory=FibonacciModel

    )



    economic: EconomicImpactModel = Field(

        default_factory=EconomicImpactModel

    )



    multi_timeframe: MultiTimeframeModel = Field(

        default_factory=MultiTimeframeModel

    )



    learning: LearningFeedbackModel = Field(

        default_factory=LearningFeedbackModel

    )



    reasons: List[str] = []


    conflicts: List[str] = []



    metadata: Dict[str, Any] = {}



    created_at: str = Field(

        default_factory=lambda:

        datetime.utcnow().isoformat()

    )





# =====================================================
# MODEL CONVERTER
# تحويل خرج المحرك إلى نموذج موحد
# =====================================================



def build_prediction_model(

    data: Dict[str, Any]

) -> PredictionResponseModel:


    return PredictionResponseModel(

        symbol=data.get(

            "symbol",

            ""

        ),


        market=data.get(

            "market",

            "crypto"

        ),


        interval=data.get(

            "interval",

            "1h"

        ),


        signal=data.get(

            "signal",

            "WAIT"

        ),


        direction=data.get(

            "direction",

            "NEUTRAL"

        ),


        confidence=data.get(

            "confidence",

            0

        ),


        probability=data.get(

            "probability",

            {}

        ),


        quality=data.get(

            "quality",

            "WEAK"

        ),


        reasons=data.get(

            "reasons",

            []

        ),


        conflicts=data.get(

            "conflicts",

            []


        ),


        metadata={

            "source":

                "PredictionEngine",

            "version":

                "2.0"

        }

    )



# =====================================================
# JSON EXPORT FOR MOBILE / API
# =====================================================


def prediction_to_json(

    data: Dict[str, Any]

):


    model = build_prediction_model(

        data

    )


    return model.model_dump()



# =====================================================
# PREDICTION PERFORMANCE TRACKING
# =====================================================



class PredictionPerformanceModel(BaseModel):

    """
    متابعة أداء نموذج التنبؤ
    """

    total_predictions: int = 0


    successful_predictions: int = 0


    failed_predictions: int = 0


    accuracy: float = 0



    def calculate_accuracy(self):

        if self.total_predictions == 0:

            self.accuracy = 0

        else:

            self.accuracy = round(

                (

                    self.successful_predictions /

                    self.total_predictions

                ) * 100,

                2

            )

        return self.accuracy




# =====================================================
# FEATURE INTELLIGENCE TRACKING
# =====================================================



class FeatureTrackingModel(BaseModel):

    """
    مراقبة تأثير كل محرك AI
    """

    features: Dict[str, float] = Field(

        default_factory=dict

    )


    active_features: List[str] = Field(

        default_factory=list

    )


    disabled_features: List[str] = Field(

        default_factory=list

    )




# =====================================================
# PREDICTION HISTORY MODEL
# =====================================================



class PredictionHistoryModel(BaseModel):

    """
    تخزين نتائج التوقعات السابقة
    لاستخدام التعلم والتحسين
    """

    symbol: str


    signal: str


    confidence: float


    entry_price: Optional[float] = None


    exit_price: Optional[float] = None


    result: str = "PENDING"


    profit_loss: float = 0


    created_at: str = Field(

        default_factory=lambda:

        datetime.utcnow().isoformat()

    )




# =====================================================
# AI ENGINE STATUS MODEL
# =====================================================



class PredictionEngineStatusModel(BaseModel):

    """
    حالة محرك التنبؤ
    """

    engine: str = "PredictionEngine"


    status: str = "running"


    version: str = "2.0"



    modules: Dict[str, bool] = Field(

        default_factory=dict

    )



    performance: PredictionPerformanceModel = Field(

        default_factory=PredictionPerformanceModel

    )



# =====================================================
# COMPLETE AI PACKAGE EXPORT
# =====================================================



class FalconAIPredictionPackage(BaseModel):

    """
    الحزمة النهائية التي تستخدمها المنصة
    """

    prediction: PredictionResponseModel


    performance: PredictionPerformanceModel = Field(

        default_factory=PredictionPerformanceModel

    )


    features: FeatureTrackingModel = Field(

        default_factory=FeatureTrackingModel

    )


    history: Optional[PredictionHistoryModel] = None


    engine_status: PredictionEngineStatusModel = Field(

        default_factory=PredictionEngineStatusModel

    )




# =====================================================
# VALIDATION FUNCTION
# =====================================================



def validate_prediction(

    data: Dict[str, Any]

) -> bool:


    required_fields = [

        "symbol",

        "signal",

        "confidence"

    ]


    for field in required_fields:


        if field not in data:

            return False



    confidence = data.get(

        "confidence",

        0

    )



    if confidence < 0 or confidence > 100:


        return False



    return True
