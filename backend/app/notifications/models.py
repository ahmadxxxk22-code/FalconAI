# =====================================================
# FalconAI Alert Models
# =====================================================


from enum import Enum

from dataclasses import dataclass, field

from datetime import datetime

from typing import (
    Dict,
    Any,
    List
)




# =====================================================
# ALERT TYPES
# =====================================================


class AlertType(str, Enum):

    EARLY_TREND = "EARLY_TREND"

    REVERSAL = "REVERSAL"

    BREAKOUT = "BREAKOUT"

    SMART_MONEY = "SMART_MONEY"

    LIQUIDITY = "LIQUIDITY"

    ORDER_BLOCK = "ORDER_BLOCK"

    FIBONACCI = "FIBONACCI"

    NEWS = "NEWS"

    RISK = "RISK"





# =====================================================
# ALERT PRIORITY
# =====================================================


class AlertPriority(str, Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"





# =====================================================
# ALERT OBJECT
# =====================================================


@dataclass

class Alert:


    symbol: str


    alert_type: AlertType


    priority: AlertPriority


    title: str


    message: str



    confidence: float = 0



    data: Dict[str, Any] = field(

        default_factory=dict

    )



    reasons: List[str] = field(

        default_factory=list

    )



    created_at: str = field(

        default_factory=lambda:

        datetime.utcnow().isoformat()

    )



    def to_dict(self):


        return {


            "symbol": self.symbol,


            "type": self.alert_type.value,


            "priority": self.priority.value,


            "title": self.title,


            "message": self.message,


            "confidence": self.confidence,


            "reasons": self.reasons,


            "data": self.data,


            "created_at": self.created_at


}
