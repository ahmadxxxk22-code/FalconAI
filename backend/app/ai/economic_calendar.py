from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum



# =====================================================
# ECONOMIC EVENT IMPACT LEVEL
# =====================================================


class EconomicImpact(Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"




# =====================================================
# MARKET SENTIMENT
# =====================================================


class MarketSentiment(Enum):

    BULLISH = "BULLISH"

    BEARISH = "BEARISH"

    NEUTRAL = "NEUTRAL"

    RISK_OFF = "RISK_OFF"




# =====================================================
# FALCONAI ECONOMIC CALENDAR AI ENGINE
# =====================================================


class EconomicCalendar:


    """
    FalconAI Economic Calendar AI


    مسؤول عن:

    - تحليل الأخبار الاقتصادية
    - تصنيف الأحداث
    - قياس قوة التأثير
    - كشف المفاجآت
    - تحليل تأثير السوق
    - إنشاء تفسير AI


    لا يجلب البيانات
    يعتمد على البيانات القادمة من مزودي البيانات
    """



    def __init__(
        self
    ):


        # ==============================
        # High Impact Events
        # ==============================


        self.event_keywords = {


            "central_bank": [

                "fed",

                "fomc",

                "federal reserve",

                "ecb",

                "boj",

                "bank of england",

                "interest rate"

            ],



            "inflation": [

                "cpi",

                "inflation",

                "ppi",

                "consumer price"

            ],



            "employment": [

                "nfp",

                "nonfarm",

                "non farm payroll",

                "employment",

                "unemployment",

                "jobless"

            ],



            "growth": [

                "gdp",

                "pmi",

                "economic growth"

            ],



            "policy": [

                "rate hike",

                "rate cut",

                "monetary policy",

                "hawkish",

                "dovish"

            ]

        }



        # ==============================
        # Supported Markets
        # ==============================


        self.market_assets = [

            "usd",

            "gold",

            "crypto",

            "stocks",

            "indices",

            "oil",

            "bonds"

        ]



        # ==============================
        # Learning Memory
        # ==============================


        self.history: List[

            Dict[str, Any]

        ] = []




# =====================================================
# TEXT NORMALIZATION
# =====================================================


    def normalize_text(
        self,
        text: Optional[str]
    ) -> str:


        if not text:

            return ""


        return str(text).lower().strip()



# =====================================================
# EVENT CLASSIFICATION ENGINE
# =====================================================


    def classify_event(
        self,
        headline: str
    ) -> Dict[str, Any]:


        text = self.normalize_text(

            headline

        )


        categories = {}

        detected_events = []



        for category, keywords in self.event_keywords.items():


            matches = []



            for keyword in keywords:


                if keyword in text:


                    matches.append(

                        keyword

                    )

                    detected_events.append(

                        keyword

                    )



            categories[category] = matches




        return {


            "categories":

                categories,


            "detected_events":

                detected_events,


            "event_count":

                len(

                    detected_events

                )

        }




# =====================================================
# IMPACT SCORE ENGINE
# =====================================================


    def calculate_impact_score(
        self,
        classification: Dict[str, Any]
    ) -> Dict[str, Any]:


        categories = classification.get(

            "categories",

            {}

        )



        score = 0



        # Central Bank = strongest effect

        if categories.get(

            "central_bank"

        ):


            score += 40




        # Inflation

        if categories.get(

            "inflation"

        ):


            score += 25




        # Employment

        if categories.get(

            "employment"

        ):


            score += 20




        # Growth

        if categories.get(

            "growth"

        ):


            score += 15




        # Policy language

        if categories.get(

            "policy"

        ):


            score += 20




        score = min(

            score,

            100

        )



        level = EconomicImpact.LOW.value



        if score >= 80:


            level = EconomicImpact.CRITICAL.value



        elif score >= 55:


            level = EconomicImpact.HIGH.value



        elif score >= 25:


            level = EconomicImpact.MEDIUM.value




        confidence = min(

            score + 15,

            100

        )




        return {


            "impact":

                level,


            "score":

                score,


            "confidence":

                confidence

        }



# =====================================================
# ECONOMIC SURPRISE ENGINE
# =====================================================


    def analyze_surprise(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:


        actual = data.get(

            "actual"

        )


        forecast = data.get(

            "forecast"

        )


        previous = data.get(

            "previous"

        )



        if (

            actual is None

            or

            forecast is None

        ):


            return {


                "available":

                    False,


                "surprise":

                    0,


                "direction":

                    "unknown"

            }




        surprise = actual - forecast



        direction = "neutral"



        if surprise > 0:


            direction = "positive"



        elif surprise < 0:


            direction = "negative"




        strength = "weak"



        if abs(surprise) >= 1:


            strength = "strong"



        elif abs(surprise) >= 0.3:


            strength = "medium"




        return {


            "available":

                True,


            "actual":

                actual,


            "forecast":

                forecast,


            "previous":

                previous,


            "surprise":

                round(

                    surprise,

                    3

                ),


            "direction":

                direction,


            "strength":

                strength

        }




# =====================================================
# MARKET IMPACT ENGINE
# =====================================================


    def analyze_market_impact(
        self,
        event_data: Dict[str, Any]
    ) -> Dict[str, str]:


        impact = {


            "usd":

                MarketSentiment.NEUTRAL.value,


            "gold":

                MarketSentiment.NEUTRAL.value,


            "crypto":

                MarketSentiment.NEUTRAL.value,


            "stocks":

                MarketSentiment.NEUTRAL.value,


            "indices":

                MarketSentiment.NEUTRAL.value,


            "oil":

                MarketSentiment.NEUTRAL.value,


            "bonds":

                MarketSentiment.NEUTRAL.value

        }



        event_type = event_data.get(

            "event_type",

            ""

        )



        surprise = event_data.get(

            "surprise",

            {}

        )



        direction = surprise.get(

            "direction",

            "neutral"

        )




        # =====================================
        # FED / INTEREST RATE
        # =====================================


        if event_type in [

            "central_bank",

            "policy"

        ]:


            if direction == "positive":


                impact["usd"] = "BULLISH"

                impact["gold"] = "BEARISH"

                impact["crypto"] = "BEARISH"



            elif direction == "negative":


                impact["usd"] = "BEARISH"

                impact["gold"] = "BULLISH"

                impact["crypto"] = "BULLISH"




        # =====================================
        # INFLATION
        # =====================================


        elif event_type == "inflation":


            if direction == "positive":


                impact["gold"] = "BULLISH"

                impact["crypto"] = "BULLISH"



            elif direction == "negative":


                impact["gold"] = "BEARISH"




        # =====================================
        # EMPLOYMENT
        # =====================================


        elif event_type == "employment":


            if direction == "positive":


                impact["stocks"] = "BULLISH"

                impact["indices"] = "BULLISH"



            elif direction == "negative":


                impact["stocks"] = "BEARISH"

                impact["indices"] = "BEARISH"




        return impact



# =====================================================
# MAIN ECONOMIC ANALYSIS
# =====================================================


    def analyze(
        self,
        event: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:


        if not event:


            return self.empty()



        headline = self.normalize_text(

            event.get(

                "headline",

                ""

            )

        )



        classification = self.classify_event(

            headline

        )



        impact = self.calculate_impact_score(

            classification

        )



        event_type = "unknown"



        categories = classification.get(

            "categories",

            {}

        )



        for category, values in categories.items():


            if values:


                event_type = category

                break




        surprise = self.analyze_surprise(

            event

        )




        market = self.analyze_market_impact(

            {

                "event_type":

                    event_type,


                "surprise":

                    surprise

            }

        )




        report = {


            "engine":

                "FalconAI Economic Calendar AI",



            "event":

                headline,



            "event_type":

                event_type,



            "classification":

                classification,



            "impact":

                impact,



            "surprise":

                surprise,



            "market_impact":

                market,



            "trade_allowed":

                impact["score"] < 80,



            "risk_level":

                self.calculate_risk_level(

                    impact["score"]

                ),



            "explanation":

                self.generate_explanation(

                    classification,

                    impact,

                    surprise

                ),



            "timestamp":

                datetime.utcnow().isoformat()

        }



        self.history.append(

            report

        )



        return report




# =====================================================
# RISK LEVEL
# =====================================================


    def calculate_risk_level(
        self,
        score: int
    ) -> str:


        if score >= 80:

            return "EXTREME"



        elif score >= 55:

            return "HIGH"



        elif score >= 25:

            return "MEDIUM"



        return "LOW"




# =====================================================
# AI EXPLANATION
# =====================================================


    def generate_explanation(
        self,
        classification: Dict[str,Any],
        impact: Dict[str,Any],
        surprise: Dict[str,Any]
    ) -> str:


        events = classification.get(

            "detected_events",

            []

        )



        if not events:


            return (

                "No important economic event detected."

            )



        message = (

            f"Detected economic event: "

            f"{', '.join(events)}. "

            f"Impact level: "

            f"{impact['impact']}."

        )



        if surprise.get(

            "available",

            False

        ):


            message += (

                f" Surprise direction: "

                f"{surprise['direction']}."

            )




        return message




# =====================================================
# LEARNING / HISTORY
# =====================================================


    def get_history(
        self
    ) -> List[Dict[str,Any]]:


        return self.history




    def evaluate_prediction(
        self,
        report: Dict[str,Any],
        actual_result: Dict[str,str]
    ) -> Dict[str,Any]:


        prediction = report.get(

            "market_impact",

            {}

        )



        correct = 0

        total = 0



        details = {}



        for asset, movement in actual_result.items():


            predicted = prediction.get(

                asset,

                "NEUTRAL"

            )



            is_correct = (

                predicted == movement

            )



            details[asset] = {


                "prediction":

                    predicted,


                "actual":

                    movement,


                "correct":

                    is_correct

            }



            total += 1



            if is_correct:

                correct += 1




        accuracy = 0



        if total:


            accuracy = int(

                correct

                /

                total

                *

                100

            )




        return {


            "accuracy":

                accuracy,


            "details":

                details

        }




# =====================================================
# STATUS
# =====================================================


    def status(
        self
    ) -> Dict[str,Any]:


        return {


            "engine":

                "FalconAI Economic Calendar AI",



            "status":

                "online",



            "history_records":

                len(

                    self.history

                ),



            "supported":

                [

                    "Fed Events",

                    "CPI",

                    "NFP",

                    "GDP",

                    "PMI",

                    "Interest Rates",

                    "Employment Data",

                    "Market Impact",

                    "Economic Surprise"

                ]

        }




# =====================================================
# EMPTY RESPONSE
# =====================================================


    def empty(
        self
    ) -> Dict[str,Any]:


        return {


            "impact":

                "UNKNOWN",


            "confidence":

                0,


            "trade_allowed":

                True,


            "explanation":

                "No economic event available.",


            "timestamp":

                datetime.utcnow().isoformat()

        }
