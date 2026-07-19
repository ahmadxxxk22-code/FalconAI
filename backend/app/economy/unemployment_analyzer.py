from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod



# =====================================================
# UNEMPLOYMENT DATA MODEL
# =====================================================


class UnemploymentData:


    """
    FalconAI Unemployment Intelligence Object

    يمثل بيانات سوق العمل:

    - Unemployment Rate
    - Jobless Claims
    - Labor Conditions
    - Actual
    - Forecast
    - Previous
    """



    def __init__(
        self,
        unemployment_rate: Optional[float] = None,
        forecast: Optional[float] = None,
        previous: Optional[float] = None,
        jobless_claims: Optional[float] = None,
        country: str = "US",
        date: Optional[str] = None
    ):


        self.unemployment_rate = unemployment_rate

        self.forecast = forecast

        self.previous = previous

        self.jobless_claims = jobless_claims

        self.country = country


        self.date = (

            date

            or

            datetime.utcnow().isoformat()

        )



    def to_dict(
        self
    ) -> Dict[str, Any]:


        return {


            "unemployment_rate":

                self.unemployment_rate,


            "forecast":

                self.forecast,


            "previous":

                self.previous,


            "jobless_claims":

                self.jobless_claims,


            "country":

                self.country,


            "date":

                self.date

        }




# =====================================================
# UNEMPLOYMENT PROVIDER INTERFACE
# =====================================================


class BaseUnemploymentProvider(ABC):


    """
    واجهة مصادر بيانات البطالة

    جاهز لاحقاً:

    - FRED API
    - Financial Modeling Prep
    - Government Labor APIs
    """



    @property
    @abstractmethod
    def provider_name(
        self
    ) -> str:

        pass




    @abstractmethod
    def fetch_unemployment(
        self,
        country: str = "US"
    ) -> UnemploymentData:

        pass




# =====================================================
# UNEMPLOYMENT ANALYZER ENGINE
# =====================================================


class UnemploymentAnalyzer:


    def __init__(
        self
    ):


        self.providers: List[
            BaseUnemploymentProvider
        ] = []


        self.history: List[
            Dict[str, Any]
        ] = []



        self.full_employment_level = 4.0



        self.market_assets = [

            "usd",

            "gold",

            "crypto",

            "stocks",

            "indices",

            "bonds"

  ]



# =====================================================
# PROVIDER MANAGEMENT
# =====================================================


    def add_provider(
        self,
        provider: BaseUnemploymentProvider
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
# UNEMPLOYMENT SURPRISE ANALYSIS
# =====================================================


    def analyze_surprise(
        self,
        data: UnemploymentData
    ) -> Dict[str, Any]:


        surprise = 0

        condition = "neutral"



        if (
            data.unemployment_rate is not None
            and
            data.forecast is not None
        ):


            surprise = (

                data.unemployment_rate

                -

                data.forecast

            )



            # ارتفاع البطالة أسوأ من المتوقع

            if surprise >= 0.3:

                condition = "negative"



            # انخفاض البطالة أفضل من المتوقع

            elif surprise <= -0.3:

                condition = "positive"



            elif surprise > 0:

                condition = "slightly_negative"



            elif surprise < 0:

                condition = "slightly_positive"




        return {


            "actual":

                data.unemployment_rate,


            "forecast":

                data.forecast,


            "surprise":

                round(

                    surprise,

                    3

                ),


            "condition":

                condition

        }




# =====================================================
# LABOR MARKET STRENGTH ANALYSIS
# =====================================================


    def analyze_labor_strength(
        self,
        data: UnemploymentData
    ) -> Dict[str, Any]:


        strength = "stable"

        score = 50



        if data.unemployment_rate is not None:


            if data.unemployment_rate < 4:


                strength = "strong"

                score = 85



            elif data.unemployment_rate > 6:


                strength = "weak"

                score = 25



            elif data.unemployment_rate > 5:


                strength = "soft"

                score = 40




        # Jobless claims impact

        if data.jobless_claims is not None:


            if data.jobless_claims > 300000:


                score -= 15



            elif data.jobless_claims < 200000:


                score += 10




        return {


            "labor_strength":

                strength,


            "score":

                max(

                    0,

                    min(

                        score,

                        100

                    )

                )

        }




# =====================================================
# FED LABOR POLICY ANALYSIS
# =====================================================


    def analyze_fed_reaction(
        self,
        labor: Dict[str, Any]
    ) -> Dict[str, Any]:


        score = labor.get(

            "score",

            50

        )


        reaction = "neutral"

        probability = 50



        if score >= 75:


            reaction = "hawkish"

            probability = 70




        elif score <= 35:


            reaction = "dovish"

            probability = 75




        return {


            "fed_reaction":

                reaction,


            "probability":

                probability

        }



# =====================================================
# UNEMPLOYMENT MARKET IMPACT ENGINE
# =====================================================


    def analyze_market_impact(
        self,
        fed_reaction: Dict[str, Any]
    ) -> Dict[str, Any]:


        impact = {


            "usd":

                "neutral",


            "gold":

                "neutral",


            "crypto":

                "neutral",


            "stocks":

                "neutral",


            "indices":

                "neutral",


            "bonds":

                "neutral"

        }



        reaction = fed_reaction.get(

            "fed_reaction",

            "neutral"

        )



        # =================================
        # Strong Labor Market
        # Higher rate pressure
        # =================================


        if reaction == "hawkish":


            impact["usd"] = "bullish"

            impact["gold"] = "bearish"

            impact["crypto"] = "bearish"

            impact["stocks"] = "bearish"

            impact["indices"] = "bearish"

            impact["bonds"] = "bearish"




        # =================================
        # Weak Labor Market
        # Rate cut expectations
        # =================================


        elif reaction == "dovish":


            impact["usd"] = "bearish"

            impact["gold"] = "bullish"

            impact["crypto"] = "bullish"

            impact["stocks"] = "bullish"

            impact["indices"] = "bullish"

            impact["bonds"] = "bullish"



        return impact




# =====================================================
# UNEMPLOYMENT INTELLIGENCE REPORT
# =====================================================


    def generate_report(
        self,
        data: UnemploymentData
    ) -> Dict[str, Any]:


        surprise = self.analyze_surprise(

            data

        )


        labor = self.analyze_labor_strength(

            data

        )


        fed = self.analyze_fed_reaction(

            labor

        )


        market = self.analyze_market_impact(

            fed

        )



        report = {


            "engine":

                "FalconAI Unemployment Intelligence",



            "timestamp":

                datetime.utcnow().isoformat(),



            "unemployment_data":

                data.to_dict(),



            "surprise_analysis":

                surprise,



            "labor_analysis":

                labor,



            "fed_analysis":

                fed,



            "market_impact":

                market

        }



        self.history.append(

            report

        )



        return report



# =====================================================
# UNEMPLOYMENT LEARNING ENGINE
# =====================================================


    def evaluate_prediction(
        self,
        report: Dict[str, Any],
        actual_market_move: Dict[str, str]
    ) -> Dict[str, Any]:


        predicted = report.get(

            "market_impact",

            {}

        )


        results = {}

        correct = 0

        total = 0



        for market, movement in actual_market_move.items():


            prediction = predicted.get(

                market,

                "neutral"

            )


            is_correct = (

                prediction == movement

            )


            results[market] = {


                "prediction":

                    prediction,


                "actual":

                    movement,


                "correct":

                    is_correct

            }



            total += 1



            if is_correct:

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
# HISTORY MANAGEMENT
# =====================================================


    def get_history(
        self
    ) -> List[Dict[str, Any]]:


        return self.history




    def latest_analysis(
        self
    ) -> Optional[Dict[str, Any]]:


        if not self.history:

            return None


        return self.history[-1]




# =====================================================
# ENGINE STATUS
# =====================================================


    def status(
        self
    ) -> Dict[str, Any]:


        return {


            "engine":

                "FalconAI Unemployment Analyzer",



            "status":

                "online",



            "supported":

                [

                    "Unemployment Rate",

                    "Jobless Claims",

                    "Labor Market Strength",

                    "Employment Surprise",

                    "Fed Labor Reaction",

                    "USD Impact",

                    "Gold Impact",

                    "Crypto Impact",

                    "Stocks Impact",

                    "Bond Impact"

                ],



            "providers":

                self.get_providers(),



            "history_records":

                len(

                    self.history

                )

      }
