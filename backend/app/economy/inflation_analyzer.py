from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod



# =====================================================
# INFLATION DATA MODEL
# =====================================================


class InflationData:


    """
    FalconAI Inflation Intelligence Object

    يمثل بيانات التضخم:

    - CPI
    - Core CPI
    - Inflation Rate
    - Actual
    - Forecast
    - Previous
    """


    def __init__(
        self,
        indicator: str,
        country: str,
        actual: Optional[float] = None,
        forecast: Optional[float] = None,
        previous: Optional[float] = None,
        unit: str = "%",
        date: Optional[str] = None
    ):


        self.indicator = indicator

        self.country = country

        self.actual = actual

        self.forecast = forecast

        self.previous = previous

        self.unit = unit

        self.date = (

            date

            or

            datetime.utcnow().isoformat()

        )



    def to_dict(
        self
    ) -> Dict[str, Any]:


        return {


            "indicator":

                self.indicator,


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


            "date":

                self.date

        }




# =====================================================
# INFLATION PROVIDER INTERFACE
# =====================================================


class BaseInflationProvider(ABC):


    """
    واجهة مصادر بيانات التضخم

    جاهز للربط مع:

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
    def fetch_inflation(
        self,
        country: str = "US"
    ) -> List[InflationData]:

        pass




# =====================================================
# INFLATION ANALYZER ENGINE
# =====================================================


class InflationAnalyzer:


    def __init__(
        self
    ):


        self.providers: List[
            BaseInflationProvider
        ] = []



        self.history: List[
            Dict[str, Any]
        ] = []



        self.key_indicators = [


            "CPI",

            "CORE CPI",

            "INFLATION RATE"

        ]



        self.target_inflation = 2.0



# =====================================================
# PROVIDER MANAGEMENT
# =====================================================


    def add_provider(
        self,
        provider: BaseInflationProvider
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
# ACTUAL VS FORECAST ANALYSIS
# =====================================================


    def analyze_surprise(
        self,
        inflation: InflationData
    ) -> Dict[str, Any]:


        surprise = 0

        status = "neutral"



        if (
            inflation.actual is not None
            and
            inflation.forecast is not None
        ):


            surprise = (

                inflation.actual

                -

                inflation.forecast

            )



            if surprise > 0.2:

                status = "hot"



            elif surprise < -0.2:

                status = "cool"




        return {


            "actual":

                inflation.actual,


            "forecast":

                inflation.forecast,


            "surprise":

                round(

                    surprise,

                    3

                ),


            "status":

                status

        }




# =====================================================
# INFLATION TREND ANALYSIS
# =====================================================


    def analyze_trend(
        self,
        inflation: InflationData
    ) -> Dict[str, Any]:


        trend = "stable"


        if (
            inflation.actual is not None
            and
            inflation.previous is not None
        ):


            difference = (

                inflation.actual

                -

                inflation.previous

            )



            if difference > 0.1:

                trend = "rising"



            elif difference < -0.1:

                trend = "falling"



        return {


            "current":

                inflation.actual,


            "previous":

                inflation.previous,


            "trend":

                trend

        }




# =====================================================
# FED POLICY PRESSURE
# =====================================================


    def analyze_fed_pressure(
        self,
        inflation: InflationData
    ) -> Dict[str, Any]:


        pressure = "neutral"

        probability = 50



        if inflation.actual is None:

            return {


                "pressure":

                    pressure,


                "probability":

                    probability

            }



        if inflation.actual > self.target_inflation:


            pressure = "hawkish"

            probability = 75



        elif inflation.actual < self.target_inflation:


            pressure = "dovish"

            probability = 65




        return {


            "fed_pressure":

                pressure,


            "probability":

                probability,


            "target":

                self.target_inflation

  }



# =====================================================
# INFLATION MARKET IMPACT
# =====================================================


    def analyze_market_impact(
        self,
        inflation: InflationData,
        fed_pressure: Dict[str, Any]
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



        pressure = fed_pressure.get(

            "fed_pressure",

            "neutral"

        )



        # ---------------------------------
        # Hot Inflation
        # ---------------------------------

        if pressure == "hawkish":


            impact["usd"] = "bullish"


            impact["gold"] = "bearish"


            impact["crypto"] = "bearish"


            impact["stocks"] = "bearish"


            impact["indices"] = "bearish"


            impact["bonds"] = "bearish"




        # ---------------------------------
        # Cool Inflation
        # ---------------------------------

        elif pressure == "dovish":


            impact["usd"] = "bearish"


            impact["gold"] = "bullish"


            impact["crypto"] = "bullish"


            impact["stocks"] = "bullish"


            impact["indices"] = "bullish"


            impact["bonds"] = "bullish"



        return impact




# =====================================================
# INFLATION INTELLIGENCE REPORT
# =====================================================


    def generate_inflation_report(
        self,
        inflation: InflationData
    ) -> Dict[str, Any]:


        surprise = self.analyze_surprise(

            inflation

        )


        trend = self.analyze_trend(

            inflation

        )


        fed = self.analyze_fed_pressure(

            inflation

        )


        market = self.analyze_market_impact(

            inflation,

            fed

        )



        report = {


            "engine":

                "FalconAI Inflation Intelligence",



            "timestamp":

                datetime.utcnow().isoformat(),



            "inflation":

                inflation.to_dict(),



            "surprise":

                surprise,



            "trend":

                trend,



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
# INFLATION PREDICTION LEARNING
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


            "results":

                results

        }




# =====================================================
# HISTORY MANAGEMENT
# =====================================================


    def get_history(
        self
    ) -> List[Dict[str, Any]]:


        return self.history




# =====================================================
# LATEST INFLATION ANALYSIS
# =====================================================


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

                "FalconAI Inflation Analyzer",



            "status":

                "online",



            "supported":

                [

                    "CPI",

                    "Core CPI",

                    "Inflation Rate",

                    "Fed Pressure",

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
