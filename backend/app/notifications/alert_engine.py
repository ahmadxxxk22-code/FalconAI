# =====================================================
# FalconAI Advanced Alert Engine
# Responsible for intelligent user alerts
# =====================================================


from typing import (

    Dict,

    Any,

    List,

    Optional

)


from datetime import datetime


from .models import (

    Alert,

    AlertType,

    AlertPriority

)





class AlertEngine:
    """
    FalconAI Alert Intelligence Layer

    مسؤول عن:

    - تحليل نتائج AI Prediction
    - اكتشاف الترند المبكر
    - اكتشاف الانعكاس
    - اكتشاف الاختراق
    - تقييم أهمية التنبيه
    - منع التنبيهات الضعيفة
    """



    def __init__(self):


        self.minimum_confidence = 70


        self.minimum_probability = 70


        self.alert_history = []



        self.cooldown_minutes = 30





    # =====================================================
    # MAIN ALERT ANALYSIS
    # =====================================================


    def analyze_prediction(

        self,

        prediction: Dict[str, Any]

    ) -> Optional[Alert]:


        if not prediction:


            return None



        symbol = prediction.get(

            "symbol",

            "UNKNOWN"

        )



        confidence = prediction.get(

            "confidence",

            0

        )



        reasons = prediction.get(

            "reasons",

            []

        )



        early_move = prediction.get(

            "early_move",

            {}

        )



        reversal = prediction.get(

            "reversal",

            {}

        )



        breakout = prediction.get(

            "breakout",

            {}

        )



        # كشف الترند المبكر

        if self.is_early_trend(

            early_move

        ):


            return self.create_alert(

                symbol=symbol,

                alert_type=AlertType.EARLY_TREND,

                confidence=early_move.get(

                    "probability",

                    0

                ),

                reasons=early_move.get(

                    "reasons",

                    []

                )

            )



        # كشف الانعكاس

        if self.is_reversal(

            reversal

        ):


            return self.create_alert(

                symbol=symbol,

                alert_type=AlertType.REVERSAL,

                confidence=reversal.get(

                    "probability",

                    0

                ),

                reasons=reversal.get(

                    "reasons",

                    []

                )

                )



# =====================================================
# BREAKOUT DETECTION
# =====================================================


    def is_breakout(

        self,

        breakout: Dict[str, Any]

    ) -> bool:


        return (

            breakout.get(

                "probability",

                0

            )

            >= self.minimum_probability

        )





# =====================================================
# EARLY TREND DETECTION
# =====================================================


    def is_early_trend(

        self,

        early_move: Dict[str, Any]

    ) -> bool:


        return (

            early_move.get(

                "probability",

                0

            )

            >= self.minimum_probability

        )





# =====================================================
# REVERSAL DETECTION
# =====================================================


    def is_reversal(

        self,

        reversal: Dict[str, Any]

    ) -> bool:


        return (

            reversal.get(

                "probability",

                0

            )

            >= self.minimum_probability

        )





# =====================================================
# CREATE ALERT
# =====================================================


    def create_alert(

        self,

        symbol: str,

        alert_type: AlertType,

        confidence: float,

        reasons: List[str]

    ) -> Alert:



        priority = self.calculate_priority(

            confidence

        )


        title = self.alert_title(

            alert_type

        )


        message = self.alert_message(

            symbol,

            alert_type,

            confidence

        )



        alert = Alert(

            symbol=symbol,

            alert_type=alert_type,

            priority=priority,

            title=title,

            message=message,

            confidence=confidence,

            reasons=reasons,

            data={

                "engine":

                    "FalconAI Alert Engine",

                "created":

                    datetime.utcnow().isoformat()

            }

        )



        self.alert_history.append(

            alert.to_dict()

        )


        return alert





# =====================================================
# PRIORITY CALCULATOR
# =====================================================


    def calculate_priority(

        self,

        confidence: float

    ) -> AlertPriority:



        if confidence >= 90:


            return AlertPriority.CRITICAL



        if confidence >= 80:


            return AlertPriority.HIGH



        if confidence >= 70:


            return AlertPriority.MEDIUM



        return AlertPriority.LOW





# =====================================================
# ALERT TITLE
# =====================================================


    def alert_title(

        self,

        alert_type: AlertType

    ) -> str:



        titles = {


            AlertType.EARLY_TREND:

                "🚨 ترند مبكر مكتشف",



            AlertType.REVERSAL:

                "🔄 احتمال انعكاس",



            AlertType.BREAKOUT:

                "📈 اختراق سعري",



            AlertType.SMART_MONEY:

                "💰 نشاط أموال ذكية",



            AlertType.LIQUIDITY:

                "💧 تغير في السيولة",



            AlertType.NEWS:

                "📰 خبر مؤثر"

        }



        return titles.get(

            alert_type,

            "⚡ FalconAI Alert"

        )





# =====================================================
# ALERT MESSAGE
# =====================================================


    def alert_message(

        self,

        symbol: str,

        alert_type: AlertType,

        confidence: float

    ) -> str:


        return (

            f"FalconAI اكتشف {alert_type.value} "

            f"على {symbol} "

            f"بثقة {round(confidence,2)}%"

      )



# =====================================================
# COOLDOWN CHECK
# =====================================================


    def can_send_alert(

        self,

        symbol: str,

        alert_type: AlertType

    ) -> bool:


        now = datetime.utcnow()



        for old_alert in reversed(

            self.alert_history

        ):


            if (

                old_alert.get(

                    "symbol"

                ) == symbol

                and

                old_alert.get(

                    "type"

                ) == alert_type.value

            ):


                created = datetime.fromisoformat(

                    old_alert.get(

                        "created_at"

                    )

                )


                diff = (

                    now - created

                ).total_seconds() / 60



                if diff < self.cooldown_minutes:


                    return False



                break



        return True





# =====================================================
# SMART MONEY ALERT
# =====================================================


    def smart_money_alert(

        self,

        symbol: str,

        smart_money: Dict[str, Any]

    ) -> Optional[Alert]:


        confidence = smart_money.get(

            "confidence",

            0

        )


        if confidence < self.minimum_confidence:


            return None



        if not self.can_send_alert(

            symbol,

            AlertType.SMART_MONEY

        ):


            return None



        return self.create_alert(

            symbol=symbol,

            alert_type=AlertType.SMART_MONEY,

            confidence=confidence,

            reasons=smart_money.get(

                "reasons",

                []

            )

        )





# =====================================================
# LIQUIDITY ALERT
# =====================================================


    def liquidity_alert(

        self,

        symbol: str,

        liquidity: Dict[str, Any]

    ) -> Optional[Alert]:


        confidence = liquidity.get(

            "confidence",

            0

        )



        if confidence < self.minimum_confidence:


            return None



        if not self.can_send_alert(

            symbol,

            AlertType.LIQUIDITY

        ):


            return None



        return self.create_alert(

            symbol=symbol,

            alert_type=AlertType.LIQUIDITY,

            confidence=confidence,

            reasons=liquidity.get(

                "reasons",

                []

            )

        )





# =====================================================
# GET ALERT HISTORY
# =====================================================


    def get_history(

        self,

        limit: int = 50

    ):


        return self.alert_history[-limit:]





# =====================================================
# HEALTH CHECK
# =====================================================


    def health_check(

        self

    ):


        return {


            "engine":

                "AlertEngine",


            "status":

                "running",


            "alerts_count":

                len(

                    self.alert_history

                ),


            "cooldown_minutes":

                self.cooldown_minutes,


            "modules": {


                "early_trend":

                    True,


                "reversal":

                    True,


                "breakout":

                    True,


                "smart_money":

                    True,


                "liquidity":

                    True

            }

      }
