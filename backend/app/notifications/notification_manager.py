# =====================================================
# FalconAI Notification Manager
# Production Notification Controller
# =====================================================


from typing import (

    Dict,

    Any,

    List,

    Optional

)


from datetime import datetime


from .models import (

    Alert

)




class NotificationManager:


    """
    FalconAI Notification Management System


    مسؤول عن:

    - استقبال التنبيهات
    - تخزين سجل التنبيهات
    - إرسال التنبيهات للمستخدمين
    - تجهيز WebSocket
    - تجهيز Push Notifications
    """



    def __init__(self):


        self.notifications = []


        self.connected_users = {}


        self.sent_count = 0


        self.failed_count = 0





    # =====================================================
    # REGISTER USER
    # =====================================================


    def register_user(

        self,

        user_id: str,

        connection=None

    ):


        self.connected_users[user_id] = connection



        return {


            "status": "registered",

            "user_id": user_id

        }





    # =====================================================
    # REMOVE USER
    # =====================================================


    def remove_user(

        self,

        user_id: str

    ):


        if user_id in self.connected_users:


            del self.connected_users[user_id]



        return {


            "status": "removed",

            "user_id": user_id

        }





    # =====================================================
    # ADD NOTIFICATION
    # =====================================================


    def add_notification(

        self,

        alert: Alert

    ):


        data = alert.to_dict()



        self.notifications.append(

            data

        )



        return data



# =====================================================
# SEND NOTIFICATION
# =====================================================


    async def send_notification(

        self,

        alert: Alert

    ):


        try:


            notification = self.add_notification(

                alert

            )


            # إرسال للمستخدمين المتصلين

            await self.broadcast(

                notification

            )


            self.sent_count += 1



            return {


                "status": "sent",

                "notification": notification

            }



        except Exception as e:


            self.failed_count += 1



            return {


                "status": "failed",

                "error": str(e)

            }





# =====================================================
# BROADCAST SYSTEM
# =====================================================


    async def broadcast(

        self,

        notification: Dict[str, Any]

    ):



        for user_id, connection in self.connected_users.items():


            try:


                if connection:


                    await connection.send_json(

                        notification

                    )



            except Exception:


                continue





# =====================================================
# GET USER NOTIFICATIONS
# =====================================================


    def get_notifications(

        self,

        limit: int = 50

    ):


        return self.notifications[-limit:]





# =====================================================
# CLEAR NOTIFICATIONS
# =====================================================


    def clear_notifications(

        self

    ):


        self.notifications.clear()



        return {


            "status":

                "cleared"

        }





# =====================================================
# STATISTICS
# =====================================================


    def statistics(

        self

    ):


        return {


            "total":

                len(

                    self.notifications

                ),


            "sent":

                self.sent_count,


            "failed":

                self.failed_count,


            "connected_users":

                len(

                    self.connected_users

                )

      }



# =====================================================
# PRIORITY FILTER
# =====================================================


    def filter_by_priority(

        self,

        priority: str

    ):


        return [

            notification

            for notification in self.notifications

            if notification.get(

                "priority"

            ) == priority

        ]





# =====================================================
# CRITICAL ALERTS
# =====================================================


    def get_critical_alerts(

        self

    ):


        return self.filter_by_priority(

            "CRITICAL"

        )





# =====================================================
# PUSH SERVICE HOOK
# =====================================================


    async def push_notification(

        self,

        user_id: str,

        notification: Dict[str, Any]

    ):


        """
        جاهز للربط مع:

        - Firebase Cloud Messaging

        - Apple Push Notification

        - Android Push

        """



        try:


            # لاحقاً يتم وضع API الخاص بمزود Push هنا


            return {


                "status":

                    "push_ready",


                "user_id":

                    user_id,


                "notification":

                    notification

            }



        except Exception as e:


            return {


                "status":

                    "failed",


                "error":

                    str(e)

            }





# =====================================================
# UNREAD NOTIFICATIONS
# =====================================================


    def unread_count(

        self

    ):


        return len(

            self.notifications

        )





# =====================================================
# HEALTH CHECK
# =====================================================


    def health_check(

        self

    ):


        return {


            "engine":

                "NotificationManager",


            "status":

                "running",


            "statistics":

                self.statistics(),


            "modules":

                {


                    "websocket":

                        True,


                    "push_service":

                        True,


                    "priority_filter":

                        True,


                    "history":

                        True


                }

      }
