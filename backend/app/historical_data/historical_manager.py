# backend/app/historical_data/historical_manager.py


from typing import (
    Dict,
    Any,
    List,
    Optional
)

from datetime import (
    datetime,
    timezone
)

import logging


# =====================================================
# LOGGER
# =====================================================

logger = logging.getLogger(
    "FalconAI.HistoricalManager"
)



# =====================================================
# HISTORICAL DATA MANAGER
# =====================================================


class HistoricalManager:


    """
    FalconAI Historical Intelligence Layer

    مسؤول عن:
    - إدارة البيانات التاريخية
    - تجهيز البيانات للتعلم الذكي
    - دعم تعدد الأسواق والفريمات
    - تجهيز البيانات للتحليل المستقبلي
    """



    def __init__(

        self,

        storage=None,

        max_history_years=None

    ):


        self.storage = storage


        self.max_history_years = max_history_years


        self.market_cache = {}


        self.statistics = {

            "loaded": 0,

            "failed": 0,

            "updated": 0

        }



        self.version = (

            "FalconAI Historical Manager V1.0"

        )



        logger.info(

            "Historical Manager initialized"

        )



    # =================================================
    # MARKET KEY
    # =================================================


    def _market_key(

        self,

        symbol: str,

        market: str,

        interval: str

    ) -> str:


        return (

            f"{market}:"

            f"{symbol}:"

            f"{interval}"

        )



    # =================================================
    # LOAD HISTORICAL DATA
    # =================================================


    def load(

        self,

        symbol: str,

        market: str,

        interval: str,

        candles: Optional[List[Dict[str, Any]]] = None

    ) -> Dict[str, Any]:


        try:


            key = self._market_key(

                symbol,

                market,

                interval

            )



            if candles is None:


                candles = []



            self.market_cache[key] = candles



            self.statistics["loaded"] += 1



            return {


                "status": "success",


                "symbol": symbol,


                "market": market,


                "interval": interval,


                "candles": len(candles)


            }



        except Exception as e:


            self.statistics["failed"] += 1


            logger.error(

                f"Historical load error: {e}"

            )


            return {


                "status": "error",

                "message": str(e)

              }



# =====================================================
# GET HISTORICAL DATA
# =====================================================


    def get(

        self,

        symbol: str,

        market: str,

        interval: str

    ) -> Dict[str, Any]:


        try:


            key = self._market_key(

                symbol,

                market,

                interval

            )


            candles = self.market_cache.get(

                key,

                []

            )


            return {


                "status": "success",


                "symbol": symbol,


                "market": market,


                "interval": interval,


                "candles": candles,


                "count": len(candles)

            }



        except Exception as e:


            logger.error(

                f"Historical get error: {e}"

            )


            return {


                "status": "error",

                "message": str(e)

            }




# =====================================================
# UPDATE HISTORICAL DATA
# =====================================================


    def update(

        self,

        symbol: str,

        market: str,

        interval: str,

        new_candles: List[Dict[str, Any]]

    ) -> Dict[str, Any]:


        try:


            key = self._market_key(

                symbol,

                market,

                interval

            )



            old_data = self.market_cache.get(

                key,

                []

            )



            combined = (

                old_data

                +

                new_candles

            )



            # إزالة التكرار حسب الوقت

            unique = {}



            for candle in combined:


                timestamp = candle.get(

                    "time",

                    candle.get(

                        "timestamp",

                        None

                    )

                )


                if timestamp is not None:


                    unique[timestamp] = candle



            updated_data = list(

                unique.values()

            )



            updated_data.sort(

                key=lambda x:

                x.get(

                    "time",

                    x.get(

                        "timestamp",

                        0

                    )

                )

            )



            self.market_cache[key] = updated_data



            self.statistics["updated"] += 1



            return {


                "status": "success",


                "updated":

                    len(updated_data),


                "symbol":

                    symbol,


                "market":

                    market,


                "interval":

                    interval

            }



        except Exception as e:


            self.statistics["failed"] += 1


            logger.error(

                f"Historical update error: {e}"

            )


            return {


                "status": "error",

                "message": str(e)

            }




# =====================================================
# PREPARE AI DATA
# =====================================================


    def prepare_for_learning(

        self,

        candles: List[Dict[str, Any]]

    ) -> Dict[str, Any]:


        try:


            if not candles:


                return {


                    "samples": 0,

                    "data": []

                }



            dataset = []



            for candle in candles:


                dataset.append({


                    "open":

                        candle.get(

                            "open",

                            0

                        ),


                    "high":

                        candle.get(

                            "high",

                            0

                        ),


                    "low":

                        candle.get(

                            "low",

                            0

                        ),


                    "close":

                        candle.get(

                            "close",

                            0

                        ),


                    "volume":

                        candle.get(

                            "volume",

                            0

                        ),


                    "time":

                        candle.get(

                            "time",

                            candle.get(

                                "timestamp",

                                None

                            )

                        )

                })



            return {


                "samples":

                    len(dataset),


                "data":

                    dataset

            }



        except Exception as e:


            logger.error(

                f"Learning preparation error: {e}"

            )


            return {


                "samples": 0,

                "data": []

      }
