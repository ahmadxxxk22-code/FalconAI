from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod



# =====================================================
# NFP DATA MODEL
# =====================================================


class NFPData:

    """
    FalconAI NFP Intelligence Object

    يمثل بيانات الوظائف الأمريكية:

    - Non Farm Payroll
    - Employment Change
    - Unemployment Rate
    - Average Hourly Earnings
    """


    def __init__(
        self,
        payrolls: Optional[float] = None,
        forecast: Optional[float] = None,
        previous: Optional[float] = None,
        unemployment_rate: Optional[float] = None,
        wage_growth: Optional[float] = None,
        country: str = "US",
        date: Optional[str] = None
    ):


        self.payrolls = payrolls

        self.forecast = forecast

        self.previous = previous

        self.unemployment_rate = unemployment_rate

        self.wage_growth = wage_growth

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


            "payrolls":

                self.payrolls,


            "forecast":

                self.forecast,


            "previous":

                self.previous,


            "unemployment_rate":

                self.unemployment_rate,


            "wage_growth":

                self.wage_growth,


            "country":

                self.country,


            "date":

                self.date

        }




# =====================================================
# NFP PROVIDER INTERFACE
# =====================================================


class BaseNFPProvider(ABC):


    """
    واجهة مصادر بيانات الوظائف

    جاهز لاحقاً:

    - FRED API
    - Financial Modeling Prep
    - Government APIs
    """


    @property
    @abstractmethod
    def provider_name(
        self
    ) -> str:

        pass



    @abstractmethod
    def fetch_nfp(
        self,
        country: str = "US"
    ) -> NFPData:

        pass




# =====================================================
# NFP ANALYZER ENGINE
# =====================================================


class NFPAnalyzer:


    def __init__(
        self
    ):


        self.providers: List[
            BaseNFPProvider
        ] = []


        self.history: List[
            Dict[str, Any]
        ] = []



        self.high_impact_level = {


            "VERY_HIGH":

                300000,


            "HIGH":

                200000,


            "MEDIUM":

                100000

        }



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
        provider: BaseNFPProvider
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
# NFP SURPRISE ANALYSIS
# =====================================================


    def analyze_surprise(
        self,
        nfp: NFPData
    ) -> Dict[str, Any]:


        surprise = 0

        condition = "neutral"



        if (
            nfp.payrolls is not None
            and
            nfp.forecast is not None
        ):


            surprise = (

                nfp.payrolls

                -

                nfp.forecast

            )



            if surprise >= 100000:

                condition = "strong_positive"



            elif surprise <= -100000:

                condition = "strong_negative"



            elif surprise > 0:

                condition = "positive"



            elif surprise < 0:

                condition = "negative"




        return {


            "actual":

                nfp.payrolls,


            "forecast":

                nfp.forecast,


            "surprise":

                surprise,


            "condition":

                condition

        }




# =====================================================
# EMPLOYMENT STRENGTH ANALYSIS
# =====================================================


    def analyze_employment_strength(
        self,
        nfp: NFPData
    ) -> Dict[str, Any]:


        strength = "stable"

        score = 50



        if nfp.payrolls is not None:


            if nfp.payrolls >= 250000:

                strength = "strong"

                score = 85



            elif nfp.payrolls <= 100000:

                strength = "weak"

                score = 30




        if (
            nfp.unemployment_rate is not None
        ):


            if nfp.unemployment_rate > 5:

                score -= 15



            elif nfp.unemployment_rate < 4:

                score += 10




        return {


            "employment_strength":

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
# FED REACTION ANALYSIS
# =====================================================


    def analyze_fed_reaction(
        self,
        nfp: NFPData
    ) -> Dict[str, Any]:


        reaction = "neutral"

        probability = 50



        strength = self.analyze_employment_strength(

            nfp

        )



        score = strength["score"]



        if score >= 75:


            reaction = "hawkish"

            probability = 75




        elif score <= 35:


            reaction = "dovish"

            probability = 70




        return {


            "fed_reaction":

                reaction,


            "probability":

                probability

        }



# =====================================================
# NFP MARKET IMPACT ENGINE
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
        # Strong Employment
        # Usually supports USD
        # =================================


        if reaction == "hawkish":


            impact["usd"] = "bullish"


            impact["gold"] = "bearish"


            impact["crypto"] = "bearish"


            impact["stocks"] = "bearish"


            impact["indices"] = "bearish"


            impact["bonds"] = "bearish"




        # =================================
        # Weak Employment
        # Supports Rate Cuts
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
# NFP INTELLIGENCE REPORT
# =====================================================


    def generate_nfp_report(
        self,
        nfp: NFPData
    ) -> Dict[str, Any]:


        surprise = self.analyze_surprise(

            nfp

        )


        employment = self.analyze_employment_strength(

            nfp

        )


        fed = self.analyze_fed_reaction(

            nfp

        )


        market = self.analyze_market_impact(

            fed

        )



        report = {


            "engine":

                "FalconAI NFP Intelligence",



            "timestamp":

                datetime.utcnow().isoformat(),



            "nfp_data":

                nfp.to_dict(),



            "surprise_analysis":

                surprise,



            "employment_analysis":

                employment,



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
# NFP LEARNING ENGINE
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

                "FalconAI NFP Analyzer",



            "status":

                "online",



            "supported":

                [

                    "Non Farm Payroll",

                    "Employment Change",

                    "Unemployment Rate",

                    "Average Hourly Earnings",

                    "Fed Reaction",

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
