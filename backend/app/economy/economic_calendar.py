from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod



# =====================================================
# Economic Event Data Model
# =====================================================


class EconomicEvent:

    """
    FalconAI Economic Event Object

    يمثل أي حدث اقتصادي:
    - Fed Decision
    - CPI
    - NFP
    - GDP
    - Unemployment
    - Bonds
    """


    def __init__(
        self,
        name: str,
        country: str,
        actual: Optional[float] = None,
        forecast: Optional[float] = None,
        previous: Optional[float] = None,
        unit: str = "",
        importance: str = "MEDIUM",
        date: Optional[str] = None
    ):


        self.name = name

        self.country = country

        self.actual = actual

        self.forecast = forecast

        self.previous = previous

        self.unit = unit

        self.importance = importance

        self.date = (

            date

            or

            datetime.utcnow().isoformat()

        )



    def to_dict(
        self
    ) -> Dict[str, Any]:


        return {


            "name":
                self.name,


            "country":
                self.country,


            "actual":
                self.actual,


            "forecast":
                self.forecast,


            "previous":
                self.previous,


            "unit":
                self.unit,


            "importance":
                self.importance,


            "date":
                self.date

        }




# =====================================================
# Economic Provider Interface
# =====================================================


class BaseEconomicProvider(ABC):

    """
    واجهة مصادر البيانات الاقتصادية

    جاهز للربط مع:

    - FRED API
    - Financial Modeling Prep
    - Investing Calendar
    - Central Bank APIs
    """


    @property
    @abstractmethod
    def provider_name(
        self
    ) -> str:

        pass



    @abstractmethod
    def fetch_events(
        self,
        country: str = "US",
        limit: int = 50
    ) -> List[EconomicEvent]:

        pass




# =====================================================
# Economic Calendar Engine
# =====================================================


class EconomicCalendar:


    def __init__(
        self
    ):


        self.providers: List[
            BaseEconomicProvider
        ] = []



        self.supported_events = {


            "FED":

                [
                    "interest rate",
                    "fed decision",
                    "fomc"
                ],


            "CPI":

                [
                    "inflation",
                    "cpi",
                    "consumer price"
                ],


            "NFP":

                [
                    "nfp",
                    "non farm payroll",
                    "employment"
                ],


            "GDP":

                [
                    "gdp",
                    "economic growth"
                ],


            "UNEMPLOYMENT":

                [
                    "unemployment",
                    "jobless"
                ],


            "BONDS":

                [
                    "bond yield",
                    "treasury",
                    "10 year yield"
                ]

        }



        self.high_impact_events = [

            "FED",

            "CPI",

            "NFP"

        ]



    # =====================================================
    # Provider Management
    # =====================================================


    def add_provider(
        self,
        provider: BaseEconomicProvider
    ):


        self.providers.append(
            provider
        )



    def get_providers(
        self
    ) -> List[str]:


        return [

            provider.provider_name

            for provider in self.providers

      ]



# =====================================================
# ECONOMIC EVENT ANALYSIS
# =====================================================


    def detect_event_type(
        self,
        event: EconomicEvent
    ) -> str:


        text = (

            event.name

        ).lower()



        for event_type, keywords in self.supported_events.items():


            for keyword in keywords:


                if keyword in text:

                    return event_type



        return "UNKNOWN"




    # =====================================================
    # ACTUAL VS FORECAST ANALYSIS
    # =====================================================


    def analyze_result(
        self,
        event: EconomicEvent
    ) -> Dict[str, Any]:


        if (

            event.actual is None

            or

            event.forecast is None

        ):


            return {


                "status":

                    "no_data",


                "direction":

                    "neutral",


                "difference":

                    None

            }



        difference = (

            event.actual

            -

            event.forecast

        )



        direction = "neutral"



        if difference > 0:


            direction = "positive"



        elif difference < 0:


            direction = "negative"



        return {


            "status":

                "analyzed",


            "actual":

                event.actual,


            "forecast":

                event.forecast,


            "difference":

                round(

                    difference,

                    4

                ),


            "direction":

                direction

        }




    # =====================================================
    # MARKET IMPACT ANALYSIS
    # =====================================================


    def calculate_market_impact(
        self,
        event_type: str,
        direction: str
    ) -> Dict[str, str]:



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




        # FED / Interest Rate

        if event_type == "FED":


            if direction == "positive":


                impact["usd"] = "bullish"

                impact["gold"] = "bearish"

                impact["crypto"] = "bearish"

                impact["stocks"] = "bearish"



            elif direction == "negative":


                impact["usd"] = "bearish"

                impact["gold"] = "bullish"

                impact["crypto"] = "bullish"

                impact["stocks"] = "bullish"





        # CPI

        elif event_type == "CPI":


            if direction == "positive":


                impact["gold"] = "bullish"

                impact["crypto"] = "bullish"


            elif direction == "negative":


                impact["usd"] = "weak"



        # NFP

        elif event_type == "NFP":


            if direction == "positive":


                impact["usd"] = "bullish"


                impact["stocks"] = (

                    "volatile"

                )


            elif direction == "negative":


                impact["usd"] = "bearish"



        # GDP

        elif event_type == "GDP":


            if direction == "positive":


                impact["stocks"] = "bullish"


            elif direction == "negative":


                impact["stocks"] = "bearish"




        # Bonds

        elif event_type == "BONDS":


            impact["gold"] = (

                "yield_sensitive"

            )


            impact["stocks"] = (

                "rate_sensitive"

            )




        return impact



# =====================================================
# FETCH ECONOMIC EVENTS FROM PROVIDERS
# =====================================================


    def fetch_events(
        self,
        country: str = "US",
        limit: int = 50
    ) -> List[Dict[str, Any]]:


        all_events = []


        for provider in self.providers:


            try:


                events = provider.fetch_events(

                    country=country,

                    limit=limit

                )


                for event in events:


                    all_events.append(

                        event.to_dict()

                    )



            except Exception as e:


                all_events.append({

                    "provider_error":

                        provider.provider_name,


                    "error":

                        str(e)

                })



        return all_events




    # =====================================================
    # FULL ECONOMIC EVENT PIPELINE
    # =====================================================


    def analyze_event(
        self,
        event: EconomicEvent
    ) -> Dict[str, Any]:


        event_type = self.detect_event_type(
            event
        )


        result = self.analyze_result(
            event
        )


        market_impact = self.calculate_market_impact(

            event_type,

            result.get(
                "direction",
                "neutral"
            )

        )



        return {


            "event":

                event.to_dict(),


            "event_type":

                event_type,


            "result_analysis":

                result,


            "market_impact":

                market_impact,


            "timestamp":

                datetime.utcnow().isoformat()

        }




    # =====================================================
    # HIGH IMPACT FILTER
    # =====================================================


    def get_high_impact_events(
        self,
        events: List[EconomicEvent]
    ) -> List[EconomicEvent]:


        important = []



        for event in events:


            event_type = self.detect_event_type(

                event

            )


            if event_type in self.high_impact_events:


                important.append(

                    event

                )



        return important



# =====================================================
# ADVANCED ECONOMIC IMPACT ENGINE
# =====================================================


    def analyze_fed_policy(
        self,
        event: EconomicEvent
    ) -> Dict[str, Any]:


        text = event.name.lower()


        policy = {

            "stance": "neutral",

            "usd_effect": "neutral",

            "market_mode": "normal"

        }



        if any(word in text for word in [

            "rate hike",

            "higher rates",

            "hawkish"

        ]):


            policy["stance"] = "hawkish"

            policy["usd_effect"] = "bullish"

            policy["market_mode"] = "risk_off"



        elif any(word in text for word in [

            "rate cut",

            "lower rates",

            "dovish"

        ]):


            policy["stance"] = "dovish"

            policy["usd_effect"] = "bearish"

            policy["market_mode"] = "risk_on"



        return policy




    # =====================================================
    # INFLATION ANALYSIS
    # =====================================================


    def analyze_inflation(
        self,
        event: EconomicEvent
    ) -> Dict[str, Any]:


        result = {


            "inflation_state":

                "neutral",


            "fed_pressure":

                "neutral",


            "gold_bias":

                "neutral"

        }



        if (

            event.actual is not None

            and

            event.forecast is not None

        ):


            if event.actual > event.forecast:


                result["inflation_state"] = (

                    "higher_than_expected"

                )


                result["fed_pressure"] = (

                    "increase_rates"

                )


                result["gold_bias"] = (

                    "positive"

                )



            elif event.actual < event.forecast:


                result["inflation_state"] = (

                    "lower_than_expected"

                )


                result["fed_pressure"] = (

                    "reduce_pressure"

                )


                result["gold_bias"] = (

                    "neutral_positive"

                )



        return result




    # =====================================================
    # BOND MARKET ANALYSIS
    # =====================================================


    def analyze_bonds(
        self,
        yield_value: float,
        previous_yield: Optional[float] = None
    ) -> Dict[str, Any]:


        result = {


            "yield_direction":

                "neutral",


            "risk_signal":

                "neutral"

        }



        if previous_yield is None:

            return result




        if yield_value > previous_yield:


            result["yield_direction"] = (

                "rising"

            )


            result["risk_signal"] = (

                "risk_off"

            )



           

        elif yield_value < previous_yield:


            result["yield_direction"] = (

                "falling"

            )


            result["risk_signal"] = (

                "risk_on"

            )



        return result




    # =====================================================
    # GLOBAL MARKET REGIME
    # =====================================================


    def detect_market_regime(
        self,
        events: List[EconomicEvent]
    ) -> str:


        risk_score = 0



        for event in events:


            analysis = self.analyze_event(

                event

            )


            impacts = analysis.get(

                "market_impact",

                {}

            )



            if impacts.get("stocks") == "bearish":

                risk_score -= 1



            if impacts.get("crypto") == "bearish":

                risk_score -= 1



            if impacts.get("gold") == "bullish":

                risk_score -= 1



            if impacts.get("stocks") == "bullish":

                risk_score += 1



        if risk_score >= 2:

            return "RISK_ON"



        elif risk_score <= -2:

            return "RISK_OFF"



        return "NEUTRAL"



# =====================================================
# ECONOMIC PROVIDER REGISTRY
# =====================================================


    def register_default_providers(
        self
    ) -> Dict[str, Any]:


        """
        تسجيل مصادر البيانات الاقتصادية

        جاهز لـ:
        - FRED
        - Financial Modeling Prep
        - RSS Economic Feeds
        - Central Banks
        """


        providers = {


            "fred":

                "Federal Reserve Economic Data",



            "financial_modeling_prep":

                "Financial Market Economic Calendar",



            "rss":

                "Economic News RSS Sources"

        }



        return {


            "registered":

                list(
                    providers.keys()
                ),


            "count":

                len(providers)

        }




# =====================================================
# ECONOMIC DATA VALIDATION
# =====================================================


    def validate_event(
        self,
        event: EconomicEvent
    ) -> bool:


        if not event.name:

            return False



        if not event.country:

            return False



        if event.actual is not None:


            if not isinstance(
                event.actual,
                (int, float)
            ):

                return False



        if event.forecast is not None:


            if not isinstance(
                event.forecast,
                (int, float)
            ):

                return False



        return True




# =====================================================
# ECONOMIC SUMMARY
# =====================================================


    def generate_summary(
        self,
        events: List[EconomicEvent]
    ) -> Dict[str, Any]:


        summary = {


            "total_events":

                len(events),


            "high_impact":

                0,


            "markets":

                {


                    "usd":

                        "neutral",


                    "gold":

                        "neutral",


                    "crypto":

                        "neutral",


                    "stocks":

                        "neutral"


                }

        }



        for event in events:


            if not self.validate_event(event):

                continue



            if event.importance == "HIGH":

                summary["high_impact"] += 1



            analysis = self.analyze_event(

                event

            )


            impact = analysis.get(

                "market_impact",

                {}

            )



            for market, value in impact.items():


                if value != "neutral":

                    summary["markets"][market] = value



        return summary



# =====================================================
# ECONOMY NEWS FUSION ENGINE
# =====================================================


    def fuse_economic_news(
        self,
        economic_events: List[EconomicEvent],
        news_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:


        result = {


            "market_sentiment":

                "neutral",


            "risk_level":

                "normal",


            "confidence":

                0,


            "drivers":

                [],


            "markets":

                {


                    "crypto":

                        "neutral",


                    "forex":

                        "neutral",


                    "gold":

                        "neutral",


                    "stocks":

                        "neutral",


                    "bonds":

                        "neutral"


                }

        }



        positive_points = 0

        negative_points = 0



        # ==============================
        # Economic Events
        # ==============================


        for event in economic_events:


            analysis = self.analyze_event(

                event

            )


            direction = analysis.get(

                "result_analysis",

                {}

            ).get(

                "direction",

                "neutral"

            )



            if direction == "positive":

                positive_points += 1



            elif direction == "negative":

                negative_points += 1



            result["drivers"].append({

                "type":

                    "economic",


                "event":

                    event.name

            })




        # ==============================
        # News Sentiment
        # ==============================


        for news in news_items:


            sentiment = news.get(

                "sentiment",

                "neutral"

            )



            if sentiment == "positive":

                positive_points += 1



            elif sentiment == "negative":

                negative_points += 1



            if news.get("markets"):


                result["drivers"].append({

                    "type":

                        "news",


                    "title":

                        news.get(
                            "title",
                            ""
                        )

                })




        # ==============================
        # Final Market Mood
        # ==============================


        total = (

            positive_points

            +

            negative_points

        )



        if total > 0:


            result["confidence"] = min(

                int(

                    (

                        abs(

                            positive_points

                            -

                            negative_points

                        )

                        /

                        total

                    )

                    *

                    100

                ),

                100

            )



        if positive_points > negative_points:


            result["market_sentiment"] = (

                "positive"

            )


            result["risk_level"] = (

                "risk_on"

            )



        elif negative_points > positive_points:


            result["market_sentiment"] = (

                "negative"

            )


            result["risk_level"] = (

                "risk_off"

            )



        return result




# =====================================================
# REAL TIME MARKET ALERT PREPARATION
# =====================================================


    def create_alert(
        self,
        event: EconomicEvent
    ) -> Dict[str, Any]:


        analysis = self.analyze_event(

            event

        )


        return {


            "alert":

                True,


            "title":

                event.name,


            "importance":

                event.importance,


            "event_type":

                self.detect_event_type(

                    event

                ),


            "impact":

                analysis.get(

                    "market_impact",

                    {}

                ),


            "created_at":

                datetime.utcnow().isoformat()

          }



# =====================================================
# NLP SENTIMENT ENGINE
# =====================================================


    def analyze_sentiment(
        self,
        text: str
    ) -> Dict[str, Any]:


        text = (

            text

            or

            ""

        ).lower()



        positive_words = [

            "growth",

            "strong",

            "positive",

            "bullish",

            "recovery",

            "beat expectations",

            "better than expected",

            "rate cut",

            "stimulus"

        ]



        negative_words = [

            "crisis",

            "recession",

            "weak",

            "negative",

            "bearish",

            "miss expectations",

            "worse than expected",

            "rate hike",

            "war",

            "default"

        ]



        positive_score = 0

        negative_score = 0



        for word in positive_words:


            if word in text:

                positive_score += 1




        for word in negative_words:


            if word in text:

                negative_score += 1




        sentiment = "neutral"



        if positive_score > negative_score:

            sentiment = "positive"



        elif negative_score > positive_score:

            sentiment = "negative"




        total = (

            positive_score

            +

            negative_score

        )



        confidence = 0



        if total > 0:


            confidence = int(

                (

                    max(

                        positive_score,

                        negative_score

                    )

                    /

                    total

                )

                *

                100

            )




        return {


            "sentiment":

                sentiment,


            "confidence":

                confidence,


            "positive_score":

                positive_score,


            "negative_score":

                negative_score

        }




# =====================================================
# AI MODEL READY INTERFACE
# =====================================================


    def analyze_with_ai_model(
        self,
        text: str,
        model_name: str = "financial_nlp"
    ) -> Dict[str, Any]:


        """
        مكان ربط نماذج الذكاء الاصطناعي لاحقاً

        أمثلة:
        - FinBERT
        - Llama Financial Model
        - OpenAI Financial Model

        حالياً يستخدم المحلل الداخلي
        """



        basic_analysis = self.analyze_sentiment(

            text

        )



        return {


            "model":

                model_name,


            "analysis":

                basic_analysis,


            "ready_for_upgrade":

                True

        }




# =====================================================
# LEARNING FROM HISTORICAL IMPACT
# =====================================================


    def store_news_impact_memory(
        self,
        news_id: str,
        market_result: Dict[str, Any]
    ) -> None:


        if not hasattr(

            self,

            "historical_impact_memory"

        ):


            self.historical_impact_memory = {}



        self.historical_impact_memory[news_id] = {


            "result":

                market_result,


            "time":

                datetime.utcnow().isoformat()

        }




    def get_news_impact_history(
        self
    ) -> Dict[str, Any]:


        return getattr(

            self,

            "historical_impact_memory",

            {}

      )



# =====================================================
# NEWS IMPACT LEARNING ENGINE
# =====================================================


    def evaluate_previous_prediction(
        self,
        news_id: str,
        actual_market_move: Dict[str, Any]
    ) -> Dict[str, Any]:


        history = self.get_news_impact_history()


        previous = history.get(
            news_id
        )


        if not previous:


            return {


                "found":

                    False,


                "message":

                    "No historical record"

            }



        predicted = previous.get(

            "result",

            {}

        )



        accuracy = {}



        for market, movement in actual_market_move.items():


            predicted_value = predicted.get(

                market,

                "neutral"

            )


            accuracy[market] = {


                "predicted":

                    predicted_value,


                "actual":

                    movement,


                "correct":

                    predicted_value == movement

            }




        correct_count = sum(

            1

            for item in accuracy.values()

            if item["correct"]

        )



        total_count = len(

            accuracy

        )



        score = 0



        if total_count > 0:


            score = int(

                (

                    correct_count

                    /

                    total_count

                )

                *

                100

            )




        return {


            "found":

                True,


            "accuracy":

                score,


            "details":

                accuracy

        }




    # =====================================================
    # SAVE MARKET REACTION
    # =====================================================


    def learn_market_reaction(
        self,
        news_id: str,
        event: EconomicEvent,
        market_result: Dict[str, Any]
    ) -> Dict[str, Any]:


        event_type = self.detect_event_type(

            event

        )



        record = {


            "event_type":

                event_type,


            "event":

                event.to_dict(),


            "market_result":

                market_result,


            "timestamp":

                datetime.utcnow().isoformat()

        }




        if not hasattr(

            self,

            "learning_database"

        ):


            self.learning_database = {}



        self.learning_database[news_id] = record



        return record




    # =====================================================
    # LEARNING STATISTICS
    # =====================================================


    def learning_statistics(
        self
    ) -> Dict[str, Any]:


        database = getattr(

            self,

            "learning_database",

            {}

        )



        return {


            "total_learned_events":

                len(database),


            "status":

                "active",


            "learning_mode":

                "historical_market_reaction"

      }



# =====================================================
# FINAL ECONOMIC REPORT ENGINE
# =====================================================


    def generate_economic_report(
        self,
        events: List[EconomicEvent],
        news_items: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:


        news_items = news_items or []



        high_impact = self.get_high_impact_events(

            events

        )



        summary = self.generate_summary(

            events

        )



        fusion = self.fuse_economic_news(

            events,

            news_items

        )



        regime = self.detect_market_regime(

            events

        )




        return {


            "report_time":

                datetime.utcnow().isoformat(),



            "events_analyzed":

                len(events),



            "high_impact_events":

                [

                    event.to_dict()

                    for event in high_impact

                ],



            "economic_summary":

                summary,



            "market_sentiment":

                fusion,



            "market_regime":

                regime,



            "learning":

                self.learning_statistics(),



            "engine":

                "FalconAI Economic Intelligence Engine"

        }




# =====================================================
# ENGINE STATUS
# =====================================================


    def status(
        self
    ) -> Dict[str, Any]:


        return {


            "engine":

                "Economic Calendar",



            "status":

                "online",



            "providers":

                self.get_providers(),



            "supported_events":

                list(

                    self.supported_events.keys()

                ),



            "high_impact":

                self.high_impact_events



      }
