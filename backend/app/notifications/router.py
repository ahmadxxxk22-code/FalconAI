# =====================================================
# FalconAI Notifications API Router
# Production Notification Interface
# =====================================================


from typing import List


from fastapi import (
    APIRouter,
    HTTPException
)


from .models import Alert


from .notification_manager import (
    NotificationManager
)



router = APIRouter(

    prefix="/notifications",

    tags=[

        "Notifications"

    ]

)



notification_manager = NotificationManager()





# =====================================================
# GET ALL NOTIFICATIONS
# =====================================================


@router.get("/")


async def get_notifications():



    return {


        "count":

            len(

                notification_manager.notifications

            ),



        "notifications":

            [

                alert.to_dict()

                for alert in notification_manager.notifications

            ]

    }







# =====================================================
# GET LATEST NOTIFICATIONS
# =====================================================


@router.get("/latest")


async def latest_notifications(

    limit: int = 20

):


    alerts = (

        notification_manager.notifications[-limit:]

    )



    return {


        "count": len(alerts),



        "notifications":

            [

                alert.to_dict()

                for alert in alerts

            ]

    }







# =====================================================
# MARK ALERT AS READ
# =====================================================


@router.post("/{symbol}/read")


async def mark_read(

    symbol: str

):


    result = notification_manager.mark_read(

        symbol

    )



    return {


        "success": result,


        "symbol": symbol

    }



# =====================================================
# CREATE TEST NOTIFICATION
# =====================================================


@router.post("/test")


async def create_test_notification():



    from .models import (

        AlertType,

        AlertPriority

    )



    alert = Alert(

        symbol="BTCUSDT",

        alert_type=AlertType.EARLY_TREND,

        priority=AlertPriority.HIGH,

        title="FalconAI Early Trend",

        message="تم اكتشاف بداية حركة قوية",

        confidence=85,

        reasons=[

            "ارتفاع الزخم",

            "زيادة حجم التداول"

        ],

        data={

            "source": "FalconAI"

        }

    )



    notification_manager.add_notification(

        alert

    )



    return {


        "success": True,


        "alert": alert.to_dict()

    }







# =====================================================
# DELETE ALL NOTIFICATIONS
# =====================================================


@router.delete("/clear")


async def clear_notifications():



    notification_manager.notifications.clear()



    return {


        "success": True,


        "message":

            "Notifications cleared"

    }
