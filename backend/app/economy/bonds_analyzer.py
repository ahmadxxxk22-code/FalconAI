from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod



# =====================================================
# BOND DATA MODEL
# =====================================================


class BondData:


    """
    FalconAI Bond Market Object

    يمثل بيانات السندات:

    - Treasury Yield
    - 10Y Yield
    - 2Y Yield
    - Yield Curve
    """


    def __init__(
        self,
        symbol: str,
        yield_value: float,
        maturity: str,
        country: str = "US",
        date: Optional[str] = None
    ):


        self.symbol = symbol

        self.yield_value = yield_value

        self.maturity = maturity

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


            "symbol":

                self.symbol,


            "yield":

                self.yield_value,


            "maturity":

                self.maturity,


            "country":

                self.country,


            "date":

                self.date

        }




# =====================================================
# BOND PROVIDER INTERFACE
# =====================================================


class BaseBondProvider(ABC):


    """
    واجهة مصادر السندات

    جاهز لـ:

    - FRED API
    - Treasury API
    - Financial Modeling Prep
    """


    @property
    @abstractmethod
    def provider_name(
        self
    ) -> str:

        pass



    @abstractmethod
    def fetch_bonds(
        self,
        country: str = "US"
    ) -> List[BondData]:

        pass




# =====================================================
# BOND ANALYZER ENGINE
# =====================================================


class BondsAnalyzer:


    def __init__(
        self
    ):


        self.providers: List[
            BaseBondProvider
        ] = []



        self.history = []



        self.key_maturities = [

            "2Y",

            "5Y",

            "10Y",

            "30Y"

      ]



# =====================================================
# YIELD TREND ANALYSIS
# =====================================================


    def analyze_yield_trend(
        self,
        current_yield: float,
        previous_yield: Optional[float] = None
    ) -> Dict[str, Any]:


        trend = "stable"

        change = 0



        if previous_yield is not None:


            change = (

                current_yield

                -

                previous_yield

            )



            if change > 0.05:

                trend = "rising"



            elif change < -0.05:

                trend = "falling"



        return {


            "current_yield":

                current_yield,


            "previous_yield":

                previous_yield,


            "change":

                round(

                    change,

                    4

                ),


            "trend":

                trend

        }




# =====================================================
# YIELD CURVE ANALYSIS
# =====================================================


    def analyze_yield_curve(
        self,
        bonds: List[BondData]
    ) -> Dict[str, Any]:


        yields = {}



        for bond in bonds:


            yields[bond.maturity] = bond.yield_value




        short = yields.get(

            "2Y",

            0

        )


        long = yields.get(

            "10Y",

            0

        )



        spread = long - short



        condition = "normal"



        if spread < 0:

            condition = "inverted"



        elif spread < 0.25:

            condition = "flat"




        return {


            "2Y":

                short,


            "10Y":

                long,


            "spread":

                round(

                    spread,

                    4

                ),


            "curve":

                condition,


            "recession_risk":

                condition == "inverted"

        }




# =====================================================
# MARKET IMPACT ANALYSIS
# =====================================================


    def analyze_market_impact(
        self,
        curve_data: Dict[str, Any],
        yield_trend: Dict[str, Any]
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

                "neutral"

        }



        trend = yield_trend.get(

            "trend"

        )


        curve = curve_data.get(

            "curve"

        )



        # Rising yields

        if trend == "rising":


            impact["usd"] = "bullish"

            impact["gold"] = "bearish"

            impact["crypto"] = "bearish"

            impact["stocks"] = "bearish"

            impact["indices"] = "bearish"




        # Falling yields

        elif trend == "falling":


            impact["usd"] = "bearish"

            impact["gold"] = "bullish"

            impact["crypto"] = "bullish"

            impact["stocks"] = "bullish"

            impact["indices"] = "bullish"




        # Yield inversion

        if curve == "inverted":


            impact["gold"] = "bullish"

            impact["stocks"] = "bearish"

            impact["indices"] = "bearish"



        return impact



# =====================================================
# BOND INTELLIGENCE REPORT
# =====================================================


    def generate_bond_report(
        self,
        bonds: List[BondData],
        current_yield: float,
        previous_yield: Optional[float] = None
    ) -> Dict[str, Any]:


        curve = self.analyze_yield_curve(

            bonds

        )


        trend = self.analyze_yield_trend(

            current_yield,

            previous_yield

        )


        impact = self.analyze_market_impact(

            curve,

            trend

        )



        report = {


            "engine":

                "FalconAI Bond Intelligence",



            "timestamp":

                datetime.utcnow().isoformat(),



            "yield_analysis":

                trend,



            "yield_curve":

                curve,



            "market_impact":

                impact



        }



        self.history.append(

            report

        )


        return report




# =====================================================
# BOND IMPACT LEARNING ENGINE
# =====================================================


    def evaluate_prediction(
        self,
        report: Dict[str, Any],
        actual_move: Dict[str, str]
    ) -> Dict[str, Any]:


        predicted = report.get(

            "market_impact",

            {}

        )



        results = {}

        correct = 0

        total = 0



        for market, movement in actual_move.items():


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
# HISTORY
# =====================================================


    def get_history(
        self
    ) -> List[Dict[str, Any]]:


        return self.history




# =====================================================
# ENGINE STATUS
# =====================================================


    def status(
        self
    ) -> Dict[str, Any]:


        return {


            "engine":

                "Bonds Analyzer",



            "status":

                "online",



            "supported":

                [

                    "Treasury Yields",

                    "Yield Curve",

                    "2Y/10Y Spread",

                    "Recession Risk",

                    "USD Impact",

                    "Gold Impact",

                    "Crypto Impact",

                    "Stocks Impact"

                ],



            "history_records":

                len(

                    self.history

                )

          }
