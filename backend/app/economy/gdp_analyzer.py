from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod



# =====================================================
# GDP DATA MODEL
# =====================================================


class GDPData:


    """
    FalconAI GDP Intelligence Object

    يمثل بيانات الناتج المحلي:

    - GDP Growth
    - Quarterly GDP
    - Annual GDP
    - Actual
    - Forecast
    - Previous
    """


    def __init__(
        self,
        growth: Optional[float] = None,
        forecast: Optional[float] = None,
        previous: Optional[float] = None,
        period: str = "quarterly",
        country: str = "US",
        date: Optional[str] = None
    ):


        self.growth = growth

        self.forecast = forecast

        self.previous = previous

        self.period = period

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


            "growth":

                self.growth,


            "forecast":

                self.forecast,


            "previous":

                self.previous,


            "period":

                self.period,


            "country":

                self.country,


            "date":

                self.date

        }




# =====================================================
# GDP PROVIDER INTERFACE
# =====================================================


class BaseGDPProvider(ABC):


    """
    واجهة مصادر بيانات GDP

    جاهز لاحقاً:

    - FRED API
    - Financial Modeling Prep
    - Government Economic APIs
    """


    @property
    @abstractmethod
    def provider_name(
        self
    ) -> str:

        pass



    @abstractmethod
    def fetch_gdp(
        self,
        country: str = "US"
    ) -> GDPData:

        pass




# =====================================================
# GDP ANALYZER ENGINE
# =====================================================


class GDPAnalyzer:


    def __init__(
        self
    ):


        self.providers: List[
            BaseGDPProvider
        ] = []


        self.history: List[
            Dict[str, Any]
        ] = []



        self.recession_threshold = 0.0



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
        provider: BaseGDPProvider
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
# GDP SURPRISE ANALYSIS
# =====================================================


    def analyze_surprise(
        self,
        gdp: GDPData
    ) -> Dict[str, Any]:


        surprise = 0

        condition = "neutral"



        if (
            gdp.growth is not None
            and
            gdp.forecast is not None
        ):


            surprise = (

                gdp.growth

                -

                gdp.forecast

            )



            if surprise >= 0.5:

                condition = "strong_positive"



            elif surprise > 0:

                condition = "positive"



            elif surprise <= -0.5:

                condition = "strong_negative"



            elif surprise < 0:

                condition = "negative"




        return {


            "actual":

                gdp.growth,


            "forecast":

                gdp.forecast,


            "surprise":

                round(

                    surprise,

                    3

                ),


            "condition":

                condition

        }




# =====================================================
# ECONOMIC STRENGTH ANALYSIS
# =====================================================


    def analyze_economic_strength(
        self,
        gdp: GDPData
    ) -> Dict[str, Any]:


        strength = "stable"

        score = 50



        if gdp.growth is not None:


            if gdp.growth >= 3:

                strength = "strong"

                score = 85



            elif gdp.growth <= 0:

                strength = "weak"

                score = 25



            elif gdp.growth < 1:

                strength = "slow"

                score = 40




        return {


            "economic_strength":

                strength,


            "score":

                score

        }




# =====================================================
# RECESSION DETECTION
# =====================================================


    def detect_recession_risk(
        self,
        gdp: GDPData
    ) -> Dict[str, Any]:


        risk = "low"

        probability = 20



        if gdp.growth is None:


            return {


                "risk":

                    risk,


                "probability":

                    probability

            }




        if gdp.growth < 0:


            risk = "high"

            probability = 75



        elif gdp.growth < 1:


            risk = "medium"

            probability = 45




        return {


            "risk":

                risk,


            "probability":

                probability

              }



# =====================================================
# GDP FED POLICY ANALYSIS
# =====================================================


    def analyze_fed_policy(
        self,
        gdp: GDPData,
        recession: Dict[str, Any]
    ) -> Dict[str, Any]:


        policy = "neutral"

        probability = 50



        risk = recession.get(

            "risk",

            "low"

        )



        if risk == "high":


            policy = "dovish"

            probability = 75




        elif (
            gdp.growth is not None
            and
            gdp.growth > 3
        ):


            policy = "hawkish"

            probability = 70




        return {


            "fed_policy":

                policy,


            "probability":

                probability

        }




# =====================================================
# GDP MARKET IMPACT ENGINE
# =====================================================


    def analyze_market_impact(
        self,
        fed_policy: Dict[str, Any]
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



        policy = fed_policy.get(

            "fed_policy",

            "neutral"

        )



        # Strong Economy
        # Higher rates possibility


        if policy == "hawkish":


            impact["usd"] = "bullish"

            impact["gold"] = "bearish"

            impact["crypto"] = "bearish"

            impact["stocks"] = "bearish"

            impact["indices"] = "bearish"

            impact["bonds"] = "bearish"




        # Weak Economy
        # Rate cuts possibility


        elif policy == "dovish":


            impact["usd"] = "bearish"

            impact["gold"] = "bullish"

            impact["crypto"] = "bullish"

            impact["stocks"] = "bullish"

            impact["indices"] = "bullish"

            impact["bonds"] = "bullish"



        return impact




# =====================================================
# GDP INTELLIGENCE REPORT
# =====================================================


    def generate_gdp_report(
        self,
        gdp: GDPData
    ) -> Dict[str, Any]:


        surprise = self.analyze_surprise(

            gdp

        )


        strength = self.analyze_economic_strength(

            gdp

        )


        recession = self.detect_recession_risk(

            gdp

        )


        fed = self.analyze_fed_policy(

            gdp,

            recession

        )


        market = self.analyze_market_impact(

            fed

        )



        report = {


            "engine":

                "FalconAI GDP Intelligence",



            "timestamp":

                datetime.utcnow().isoformat(),



            "gdp_data":

                gdp.to_dict(),



            "surprise":

                surprise,



            "economic_strength":

                strength,



            "recession_risk":

                recession,



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
# GDP LEARNING ENGINE
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



            results[market] = {


                "prediction":

                    prediction,


                "actual":

                    movement,


                "correct":

                    prediction == movement

            }



            total += 1



            if prediction == movement:

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

                "FalconAI GDP Analyzer",



            "status":

                "online",



            "supported":

                [

                    "Quarterly GDP",

                    "Annual GDP",

                    "GDP Surprise",

                    "Economic Strength",

                    "Recession Risk",

                    "Fed Policy Impact",

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
