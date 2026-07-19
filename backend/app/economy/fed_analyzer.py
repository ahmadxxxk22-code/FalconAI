from typing import Dict, Any, List, Optional
from datetime import datetime



# =====================================================
# FED EVENT MODEL
# =====================================================


class FedEvent:


    """
    FalconAI Federal Reserve Event Object

    يمثل:
    - قرار الفائدة
    - تصريح عضو Fed
    - FOMC Meeting
    - توقعات السياسة النقدية
    """


    def __init__(
        self,
        title: str,
        speaker: Optional[str] = None,
        rate_change: Optional[float] = None,
        statement: str = "",
        date: Optional[str] = None
    ):


        self.title = title

        self.speaker = speaker

        self.rate_change = rate_change

        self.statement = statement

        self.date = (

            date

            or

            datetime.utcnow().isoformat()

        )



    def to_dict(
        self
    ) -> Dict[str, Any]:


        return {


            "title":

                self.title,


            "speaker":

                self.speaker,


            "rate_change":

                self.rate_change,


            "statement":

                self.statement,


            "date":

                self.date

        }




# =====================================================
# FED ANALYZER ENGINE
# =====================================================


class FedAnalyzer:


    def __init__(
        self
    ):


        self.hawkish_keywords = [

            "higher rates",

            "rate hike",

            "inflation concern",

            "tightening",

            "restrictive policy",

            "strong labor market"

        ]



        self.dovish_keywords = [

            "rate cut",

            "lower rates",

            "easing",

            "economic slowdown",

            "weak labor market",

            "stimulus"

        ]



        self.history: List[Dict[str, Any]] = []




    # =====================================================
    # POLICY STANCE DETECTION
    # =====================================================


    def analyze_statement(
        self,
        statement: str
    ) -> Dict[str, Any]:


        text = (

            statement

            or

            ""

        ).lower()



        hawkish_score = 0

        dovish_score = 0



        for word in self.hawkish_keywords:


            if word in text:

                hawkish_score += 1




        for word in self.dovish_keywords:


            if word in text:

                dovish_score += 1




        stance = "neutral"



        if hawkish_score > dovish_score:


            stance = "hawkish"



        elif dovish_score > hawkish_score:


            stance = "dovish"




        confidence = 0



        total = (

            hawkish_score

            +

            dovish_score

        )



        if total > 0:


            confidence = int(

                (

                    max(

                        hawkish_score,

                        dovish_score

                    )

                    /

                    total

                )

                *

                100

            )




        return {


            "stance":

                stance,


            "confidence":

                confidence,


            "hawkish_score":

                hawkish_score,


            "dovish_score":

                dovish_score

          }



# =====================================================
# INTEREST RATE DECISION ANALYSIS
# =====================================================


    def analyze_rate_decision(
        self,
        event: FedEvent
    ) -> Dict[str, Any]:


        result = {


            "policy":

                "neutral",


            "rate_direction":

                "unchanged",


            "impact":

                {}

        }



        if event.rate_change is None:

            return result




        if event.rate_change > 0:


            result["policy"] = "tightening"

            result["rate_direction"] = "increase"



            result["impact"] = {


                "usd":

                    "bullish",


                "gold":

                    "bearish",


                "crypto":

                    "bearish",


                "stocks":

                    "bearish",


                "bonds":

                    "bearish"

            }




        elif event.rate_change < 0:


            result["policy"] = "easing"

            result["rate_direction"] = "decrease"



            result["impact"] = {


                "usd":

                    "bearish",


                "gold":

                    "bullish",


                "crypto":

                    "bullish",


                "stocks":

                    "bullish",


                "bonds":

                    "bullish"

            }




        return result




# =====================================================
# FED MARKET IMPACT ANALYSIS
# =====================================================


    def analyze_market_effect(
        self,
        event: FedEvent
    ) -> Dict[str, Any]:


        statement_analysis = self.analyze_statement(

            event.statement

        )


        rate_analysis = self.analyze_rate_decision(

            event

        )



        impact = {


            "usd":

                "neutral",


            "gold":

                "neutral",


            "crypto":

                "neutral",


            "stocks":

                "neutral",


            "bonds":

                "neutral"

        }



        stance = statement_analysis.get(

            "stance",

            "neutral"

        )



        if stance == "hawkish":


            impact["usd"] = "bullish"

            impact["gold"] = "bearish"

            impact["crypto"] = "bearish"

            impact["stocks"] = "bearish"

            impact["bonds"] = "bearish"



        elif stance == "dovish":


            impact["usd"] = "bearish"

            impact["gold"] = "bullish"

            impact["crypto"] = "bullish"

            impact["stocks"] = "bullish"

            impact["bonds"] = "bullish"




        return {


            "event":

                event.to_dict(),


            "stance":

                statement_analysis,


            "rate_analysis":

                rate_analysis,


            "market_impact":

                impact,


            "timestamp":

                datetime.utcnow().isoformat()

        }




# =====================================================
# SAVE FED HISTORY
# =====================================================


    def save_history(
        self,
        analysis: Dict[str, Any]
    ):


        self.history.append(

            analysis

        )



    def get_history(
        self
    ) -> List[Dict[str, Any]]:


        return self.history



# =====================================================
# FED INTELLIGENCE REPORT
# =====================================================


    def generate_fed_report(
        self,
        event: FedEvent
    ) -> Dict[str, Any]:


        analysis = self.analyze_market_effect(

            event

        )


        self.save_history(

            analysis

        )



        stance = analysis.get(

            "stance",

            {}

        ).get(

            "stance",

            "neutral"

        )



        rate = analysis.get(

            "rate_analysis",

            {}

        )



        market_mode = "neutral"



        if stance == "hawkish":


            market_mode = "risk_off"



        elif stance == "dovish":


            market_mode = "risk_on"




        return {


            "engine":

                "FalconAI Fed Intelligence",



            "event":

                event.to_dict(),



            "policy_stance":

                stance,



            "market_mode":

                market_mode,



            "impact":

                analysis.get(

                    "market_impact",

                    {}

                ),



            "rate_analysis":

                rate,



            "confidence":

                analysis.get(

                    "stance",

                    {}

                ).get(

                    "confidence",

                    0

                ),



            "created_at":

                datetime.utcnow().isoformat()

        }




# =====================================================
# FED LEARNING ENGINE
# =====================================================


    def evaluate_fed_prediction(
        self,
        previous_report: Dict[str, Any],
        actual_market_move: Dict[str, str]
    ) -> Dict[str, Any]:


        predicted = previous_report.get(

            "impact",

            {}

        )



        results = {}

        correct = 0

        total = 0



        for market, movement in actual_market_move.items():


            predicted_move = predicted.get(

                market,

                "neutral"

            )


            results[market] = {


                "predicted":

                    predicted_move,


                "actual":

                    movement,


                "correct":

                    predicted_move == movement

            }



            total += 1



            if predicted_move == movement:

                correct += 1




        accuracy = 0



        if total > 0:


            accuracy = int(

                (

                    correct

                    /

                    total

                )

                *

                100

            )




        return {


            "accuracy":

                accuracy,


            "details":

                results

        }




# =====================================================
# ENGINE STATUS
# =====================================================


    def status(
        self
    ) -> Dict[str, Any]:


        return {


            "engine":

                "Fed Analyzer",


            "status":

                "online",


            "supported":

                [

                    "FED Decisions",

                    "FOMC Statements",

                    "Interest Rates",

                    "USD Impact",

                    "Gold Impact",

                    "Crypto Impact",

                    "Stocks Impact",

                    "Bond Impact"

                ],


            "history_records":

                len(

                    self.history

                )

      }
