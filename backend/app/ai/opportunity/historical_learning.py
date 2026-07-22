# =====================================================
# FALCONAI HISTORICAL LEARNING ENGINE
# PRODUCTION VERSION
# PART 1
# =====================================================


from datetime import datetime
from collections import deque
import statistics
import math



class HistoricalLearning:


    def __init__(self):


        self.version = "FalconAI Historical Learning v2"


        # عدد الشموع لتحليل النمط
        self.lookback_window = 50


        # أقل بيانات مطلوبة
        self.minimum_history = 500


        # ذاكرة الإشارات
        self.signal_memory = deque(
            maxlen=10000
        )


        # ذاكرة الأنماط
        self.pattern_memory = deque(
            maxlen=5000
        )


        # إحصائيات التعلم
        self.statistics = {


            "signals":

                0,


            "successful":

                0,


            "failed":

                0,


            "win_rate":

                0


        }



    # =====================================================
    # SAFE NUMBER
    # =====================================================


    def safe_number(

        self,

        value,

        default=0

    ):


        try:

            return float(value)


        except:

            return default



    # =====================================================
    # RETURNS ENGINE
    # =====================================================


    def calculate_returns(

        self,

        closes

    ):


        returns = []


        for i in range(1,len(closes)):


            previous = self.safe_number(

                closes[i-1]

            )


            current = self.safe_number(

                closes[i]

            )


            if previous == 0:

                continue



            change = (

                current - previous

            ) / previous



            returns.append(

                change

            )


        return returns



    # =====================================================
    # AVERAGE MOVE
    # =====================================================


    def average_move(

        self,

        returns

    ):


        if not returns:

            return 0


        return statistics.mean(

            returns

        )



    # =====================================================
    # VOLATILITY ENGINE
    # =====================================================


    def volatility(

        self,

        returns

    ):


        if len(returns) < 2:

            return 0



        return statistics.stdev(

            returns

        )



    # =====================================================
    # DRAWDOWN ANALYSIS ENGINE
    # =====================================================


    def calculate_drawdown(

        self,

        closes

    ):


        if not closes:

            return 0



        peak = self.safe_number(

            closes[0]

        )


        max_drawdown = 0



        for price in closes:


            price = self.safe_number(

                price

            )


            if price > peak:

                peak = price



            if peak == 0:

                continue



            drop = (

                peak - price

            ) / peak * 100



            if drop > max_drawdown:

                max_drawdown = drop



        return round(

            max_drawdown,

            2

        )



    # =====================================================
    # MARKET DIRECTION MEMORY
    # =====================================================


    def calculate_direction_memory(

        self,

        returns

    ):


        if not returns:


            return {


                "bullish":

                    50,


                "bearish":

                    50


            }



        bullish = 0

        bearish = 0



        for move in returns:


            if move > 0:

                bullish += 1


            elif move < 0:

                bearish += 1



        total = bullish + bearish



        if total == 0:


            return {


                "bullish":

                    50,


                "bearish":

                    50


            }



        return {


            "bullish":

                round(

                    bullish /
                    total *
                    100,

                    2

                ),


            "bearish":

                round(

                    bearish /
                    total *
                    100,

                    2

                )

        }



    # =====================================================
    # PATTERN MEMORY STORAGE
    # =====================================================


    def store_pattern(

        self,

        pattern

    ):


        if not pattern:

            return False



        record = {


            "time":

                datetime.utcnow().isoformat(),


            "pattern":

                pattern

        }



        self.pattern_memory.append(

            record

        )


        return True



    # =====================================================
    # PATTERN SIMILARITY AI
    # =====================================================


    def pattern_similarity(

        self,

        current,

        previous

    ):


        if not current or not previous:

            return 0



        length = min(

            len(current),

            len(previous)

        )


        if length == 0:

            return 0



        difference = 0



        for i in range(length):


            difference += abs(

                current[i]

                -

                previous[i]

            )



        average_difference = (

            difference /

            length

        )



        score = (

            100 -

            (
                average_difference *
                100
            )

        )



        return round(

            max(

                0,

                min(

                    score,

                    100

                )

            ),

            2

        )



    # =====================================================
    # SAVE SIGNAL LEARNING MEMORY
    # =====================================================


    def save_signal_result(

        self,

        symbol,

        signal,

        confidence,

        entry_price,

        result=None

    ):


        record = {


            "symbol":

                symbol,


            "signal":

                signal,


            "confidence":

                confidence,


            "entry_price":

                entry_price,


            "result":

                result,


            "time":

                datetime.utcnow().isoformat()

        }



        self.signal_memory.append(

            record

        )



        self.statistics["signals"] += 1



        return True



    # =====================================================
    # UPDATE SIGNAL RESULT
    # =====================================================


    def update_signal_result(

        self,

        index,

        result

    ):


        if index < 0:

            return False



        if index >= len(

            self.signal_memory

        ):

            return False



        self.signal_memory[index]["result"] = result



        if result == "SUCCESS":


            self.statistics["successful"] += 1



        elif result == "FAILED":


            self.statistics["failed"] += 1



        total = (

            self.statistics["successful"]

            +

            self.statistics["failed"]

        )



        if total > 0:


            self.statistics["win_rate"] = round(

                (

                    self.statistics["successful"]

                    /

                    total

                )

                *

                100,

                2

            )



        return True



    # =====================================================
    # LEARNING FROM HISTORY
    # =====================================================


    def learn_from_history(

        self,

        signal,

        market_condition=None

    ):


        successful = []

        failed = []



        for item in self.signal_memory:



            if item["signal"] != signal:

                continue



            if item["result"] == "SUCCESS":

                successful.append(item)



            elif item["result"] == "FAILED":

                failed.append(item)



        total = len(successful) + len(failed)



        if total == 0:


            return {


                "signal":

                    signal,


                "experience":

                    0,


                "success_rate":

                    50


            }



        success_rate = (

            len(successful)

            /

            total

        ) * 100



        return {


            "signal":

                signal,


            "experience":

                total,


            "success_rate":

                round(

                    success_rate,

                    2

                ),


            "market_condition":

                market_condition

        }



    # =====================================================
    # LEARNING REPORT
    # =====================================================


    def get_learning_report(

        self

    ):


        return {


            "engine":

                self.version,


            "memory_size":

                len(

                    self.signal_memory

                ),


            "patterns":

                len(

                    self.pattern_memory

                ),


            "statistics":

                self.statistics,


            "last_update":

                datetime.utcnow().isoformat()

        }



    # =====================================================
    # HISTORICAL SIGNAL GENERATOR
    # =====================================================


    def get_historical_signal(

        self,

        analysis

    ):


        if not analysis:


            return {


                "signal":

                    "WAIT",


                "strength":

                    0,


                "reason":

                    "No historical data"

            }



        probability = self.safe_number(

            analysis.get(

                "trend_probability",

                50

            )

        )


        confidence = self.safe_number(

            analysis.get(

                "confidence",

                0

            )

        )



        if (

            probability >= 65

            and

            confidence >= 60

        ):


            return {


                "signal":

                    "BUY",


                "strength":

                    confidence,


                "reason":

                    "Historical bullish advantage"

            }




        if (

            probability <= 35

            and

            confidence >= 60

        ):


            return {


                "signal":

                    "SELL",


                "strength":

                    confidence,


                "reason":

                    "Historical bearish advantage"

            }




        return {


            "signal":

                "WAIT",


            "strength":

                confidence,


            "reason":

                "Historical confirmation weak"

        }



    # =====================================================
    # HISTORICAL MARKET SUMMARY
    # =====================================================


    def market_summary(

        self,

        analysis

    ):


        if not analysis:


            return {}



        signal = self.get_historical_signal(

            analysis

        )



        return {


            "historical_signal":

                signal["signal"],


            "historical_strength":

                signal["strength"],


            "historical_reason":

                signal["reason"],


            "bullish_probability":

                analysis.get(

                    "bullish_probability",

                    50

                ),


            "bearish_probability":

                analysis.get(

                    "bearish_probability",

                    50

                ),


            "similarity":

                analysis.get(

                    "historical_similarity",

                    0

                ),


            "confidence":

                analysis.get(

                    "confidence",

                    0

                )

        }



    # =====================================================
    # RECENT HISTORY SNAPSHOT
    # =====================================================


    def recent_history(

        self,

        limit=20

    ):


        return list(

            self.signal_memory[-limit:]

            )



    # =====================================================
    # MEMORY EXPORT
    # =====================================================


    def export_memory(

        self

    ):


        return {


            "signals":

                list(

                    self.signal_memory

                ),


            "patterns":

                list(

                    self.pattern_memory

                ),


            "statistics":

                self.statistics,


            "export_time":

                datetime.utcnow().isoformat()

        }



    # =====================================================
    # RESET LEARNING MEMORY
    # =====================================================


    def reset_learning(

        self

    ):


        self.signal_memory.clear()


        self.pattern_memory.clear()



        self.statistics = {


            "signals":

                0,


            "successful":

                0,


            "failed":

                0,


            "win_rate":

                0

        }



        return True



    # =====================================================
    # HEALTH CHECK
    # =====================================================


    def health_check(

        self

    ):


        return {


            "engine":

                self.version,


            "status":

                "ACTIVE",


            "signal_memory":

                len(

                    self.signal_memory

                ),


            "pattern_memory":

                len(

                    self.pattern_memory

                ),


            "win_rate":

                self.statistics.get(

                    "win_rate",

                    0

                ),


            "time":

                datetime.utcnow().isoformat()

        }



    # =====================================================
    # ENGINE STATUS
    # =====================================================


    def status(

        self

    ):


        return {


            "name":

                "HistoricalLearning",


            "version":

                self.version,


            "ready":

                True,


            "memory":

            {


                "signals":

                    len(

                        self.signal_memory

                    ),


                "patterns":

                    len(

                        self.pattern_memory

                    )

            },


            "statistics":

                self.statistics

        }



# =====================================================
# MULTI TIMEFRAME MEMORY
# =====================================================

    def save_timeframe_result(

        self,

        symbol,

        timeframe,

        signal,

        confidence,

        result

    ):

        if not hasattr(self, "timeframe_memory"):

            self.timeframe_memory = {}

        key = f"{symbol}_{timeframe}"

        if key not in self.timeframe_memory:

            self.timeframe_memory[key] = []

        self.timeframe_memory[key].append({

            "signal": signal,

            "confidence": confidence,

            "result": result,

            "time": datetime.utcnow().isoformat()

        })

        if len(self.timeframe_memory[key]) > 500:

            self.timeframe_memory[key] = self.timeframe_memory[key][-500:]

        return True


# =====================================================
# BEST TIMEFRAME
# =====================================================

    def best_timeframe(

        self,

        symbol

    ):

        if not hasattr(self, "timeframe_memory"):

            return None

        best_tf = None
        best_rate = 0

        for key, records in self.timeframe_memory.items():

            if not key.startswith(symbol):

                continue

            success = sum(
                1 for r in records
                if r["result"] == "SUCCESS"
            )

            total = len(records)

            if total == 0:

                continue

            rate = success / total * 100

            if rate > best_rate:

                best_rate = rate
                best_tf = key.split("_")[1]

        return {

            "timeframe": best_tf,

            "success_rate": round(best_rate, 2)

        }


# =====================================================
# PERFORMANCE MONITOR
# =====================================================

    def performance_monitor(self):

        success = self.statistics.get(
            "successful",
            0
        )

        failed = self.statistics.get(
            "failed",
            0
        )

        total = success + failed

        if total == 0:

            return {

                "status": "NO_DATA",

                "warning": False

            }

        win_rate = success / total * 100

        warning = win_rate < 55

        return {

            "status": "OK" if not warning else "DEGRADED",

            "win_rate": round(win_rate, 2),

            "warning": warning

        }


# =====================================================
# LEARNING RECOMMENDATION
# =====================================================

    def learning_recommendation(self):

        monitor = self.performance_monitor()

        if monitor["status"] == "DEGRADED":

            return {

                "action": "RETRAIN_AI",

                "reason": "Historical performance dropped"

            }

        return {

            "action": "KEEP_RUNNING",

            "reason": "Performance stable"

        }


# =====================================================
# FINAL PRODUCTION STATUS
# =====================================================

    def production_status(self):

        return {

            "engine": self.version,

            "status": "ACTIVE",

            "signals": len(self.signal_memory),

            "patterns": len(self.pattern_memory),

            "statistics": self.statistics,

            "performance": self.performance_monitor(),

            "recommendation": self.learning_recommendation(),

            "ready": True

        }
