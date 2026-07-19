from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod



# =====================================================
# MACRO DATA MODEL
# =====================================================


class MacroSnapshot:


    """
    FalconAI Macro Intelligence Object

    يجمع حالة الاقتصاد الكلي:

    - Fed
    - Inflation
    - NFP
    - GDP
    - Unemployment
    - Bonds
    - News Sentiment
    """


    def __init__(
        self,
        fed: Optional[Dict[str, Any]] = None,
        inflation: Optional[Dict[str, Any]] = None,
        nfp: Optional[Dict[str, Any]] = None,
        gdp: Optional[Dict[str, Any]] = None,
        unemployment: Optional[Dict[str, Any]] = None,
        bonds: Optional[Dict[str, Any]] = None,
        news: Optional[Dict[str, Any]] = None,
        sentiment: Optional[Dict[str, Any]] = None,
        date: Optional[str] = None
    ):


        self.fed = fed or {}

        self.inflation = inflation or {}

        self.nfp = nfp or {}

        self.gdp = gdp or {}

        self.unemployment = unemployment or {}

        self.bonds = bonds or {}

        self.news = news or {}

        self.sentiment = sentiment or {}


        self.date = (

            date

            or

            datetime.utcnow().isoformat()

        )



    def to_dict(
        self
    ) -> Dict[str, Any]:


        return {


            "fed":

                self.fed,


            "inflation":

                self.inflation,


            "nfp":

                self.nfp,


            "gdp":

                self.gdp,


            "unemployment":

                self.unemployment,


            "bonds":

                self.bonds,


            "news":

                self.news,


            "sentiment":

                self.sentiment,


            "date":

                self.date

        }




# =====================================================
# MACRO ENGINE INTERFACE
# =====================================================


class BaseMacroModule(ABC):


    """
    واجهة أي وحدة ماكرو داخل FalconAI

    جاهزة لأي محرك اقتصادي جديد
    """



    @property
    @abstractmethod
    def module_name(
        self
    ) -> str:

        pass



    @abstractmethod
    def analyze(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:

        pass




# =====================================================
# FALCONAI MACRO ENGINE
# =====================================================


class MacroEngine:


    def __init__(
        self
    ):


        self.modules: List[
            BaseMacroModule
        ] = []



        self.history: List[
            Dict[str, Any]
        ] = []



        self.market_assets = [

            "usd",

            "gold",

            "crypto",

            "stocks",

            "indices",

            "bonds"

        ]



        self.score_limits = {


            "maximum":

                100,


            "minimum":

                -100

        }



# =====================================================
# MODULE MANAGEMENT
# =====================================================


    def add_module(
        self,
        module: BaseMacroModule
    ):


        self.modules.append(
            module
        )



    def get_modules(
        self
    ) -> List[str]:


        return [

            module.module_name

            for module in self.modules

        ]




# =====================================================
# MACRO SCORE ENGINE
# =====================================================


    def calculate_macro_score(
        self,
        snapshot: MacroSnapshot
    ) -> Dict[str, Any]:


        score = 0


        factors = {}



        # =====================================
        # FED IMPACT
        # =====================================


        fed_policy = snapshot.fed.get(

            "fed_policy",

            snapshot.fed.get(

                "fed_reaction",

                "neutral"

            )

        )



        if fed_policy == "hawkish":


            score += 20


            factors["fed"] = "hawkish"



        elif fed_policy == "dovish":


            score -= 20


            factors["fed"] = "dovish"



        else:


            factors["fed"] = "neutral"




        # =====================================
        # INFLATION IMPACT
        # =====================================


        inflation_condition = snapshot.inflation.get(

            "condition",

            "neutral"

        )



        if inflation_condition in [

            "high",

            "strong_positive"

        ]:


            score += 10


            factors["inflation"] = "pressure"



        elif inflation_condition in [

            "low",

            "negative"

        ]:


            score -= 10


            factors["inflation"] = "cooling"



        else:


            factors["inflation"] = "neutral"




        # =====================================
        # GDP IMPACT
        # =====================================


        economic_strength = snapshot.gdp.get(

            "economic_strength",

            {}

        ).get(

            "economic_strength",

            "stable"

        )



        if economic_strength == "strong":


            score += 15


            factors["gdp"] = "strong"



        elif economic_strength in [

            "weak",

            "slow"

        ]:


            score -= 15


            factors["gdp"] = "weak"



        else:


            factors["gdp"] = "stable"




        # =====================================
        # LABOR MARKET IMPACT
        # =====================================


        labor = snapshot.unemployment.get(

            "labor_analysis",

            {}

        ).get(

            "score",

            50

        )



        if labor >= 75:


            score += 15


            factors["labor"] = "strong"



        elif labor <= 35:


            score -= 15


            factors["labor"] = "weak"



        else:


            factors["labor"] = "stable"




        # Limit score


        score = max(

            self.score_limits["minimum"],

            min(

                score,

                self.score_limits["maximum"]

            )

        )



        return {


            "macro_score":

                score,


            "factors":

                factors

      }



# =====================================================
# RISK SENTIMENT ANALYSIS
# =====================================================


    def detect_market_regime(
        self,
        macro_score: int
    ) -> Dict[str, Any]:


        regime = "neutral"

        confidence = abs(

            macro_score

        )



        if macro_score >= 40:


            regime = "risk_on"



        elif macro_score <= -40:


            regime = "risk_off"




        return {


            "regime":

                regime,


            "confidence":

                min(

                    confidence,

                    100

                )

        }




# =====================================================
# MARKET BIAS GENERATOR
# =====================================================


    def generate_market_bias(
        self,
        regime: Dict[str, Any]
    ) -> Dict[str, Any]:


        bias = {


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



        state = regime.get(

            "regime",

            "neutral"

        )



        # =====================================
        # RISK ON
        # المستثمرون يقبلون المخاطرة
        # =====================================


        if state == "risk_on":


            bias["usd"] = "neutral"


            bias["gold"] = "bearish"


            bias["crypto"] = "bullish"


            bias["stocks"] = "bullish"


            bias["indices"] = "bullish"


            bias["bonds"] = "bearish"




        # =====================================
        # RISK OFF
        # الهروب للأمان
        # =====================================


        elif state == "risk_off":


            bias["usd"] = "bullish"


            bias["gold"] = "bullish"


            bias["crypto"] = "bearish"


            bias["stocks"] = "bearish"


            bias["indices"] = "bearish"


            bias["bonds"] = "bullish"




        return bias




# =====================================================
# MACRO INTELLIGENCE REPORT
# =====================================================


    def generate_report(
        self,
        snapshot: MacroSnapshot
    ) -> Dict[str, Any]:


        score = self.calculate_macro_score(

            snapshot

        )



        regime = self.detect_market_regime(

            score["macro_score"]

        )



        market_bias = self.generate_market_bias(

            regime

        )



        report = {


            "engine":

                "FalconAI Macro Intelligence",



            "timestamp":

                datetime.utcnow().isoformat(),



            "macro_data":

                snapshot.to_dict(),



            "macro_score":

                score,



            "market_regime":

                regime,



            "market_bias":

                market_bias

        }



        self.history.append(

            report

        )



        return report



# =====================================================
# MACRO LEARNING ENGINE
# =====================================================


    def evaluate_prediction(
        self,
        report: Dict[str, Any],
        actual_market_move: Dict[str, str]
    ) -> Dict[str, Any]:


        predicted = report.get(

            "market_bias",

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

                * 100

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

                "FalconAI Macro Engine",



            "status":

                "online",



            "modules":

                self.get_modules(),



            "supported":

                [

                    "Fed Analysis",

                    "Inflation Analysis",

                    "NFP Analysis",

                    "GDP Analysis",

                    "Unemployment Analysis",

                    "Bond Analysis",

                    "News Impact",

                    "Macro Score",

                    "Risk On / Risk Off",

                    "Market Bias",

                    "Learning Accuracy"

                ],



            "history_records":

                len(

                    self.history

                )

      }
