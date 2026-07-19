from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod
import hashlib
import re


# =====================================================
# NEWS DATA MODEL
# =====================================================

class NewsItem:
    """
    Standard FalconAI News Object

    نموذج موحد لكل الأخبار من أي مصدر
    """


    def __init__(
        self,
        title: str,
        source: str,
        published_at: Optional[str] = None,
        content: Optional[str] = None,
        url: Optional[str] = None,
        sentiment: Optional[str] = None,
        impact: Optional[str] = None,
        markets: Optional[List[str]] = None
    ):

        self.title = title

        self.source = source

        self.published_at = (
            published_at
            or datetime.utcnow().isoformat()
        )

        self.content = content or ""

        self.url = url

        self.sentiment = sentiment or "neutral"

        self.impact = impact or "low"

        self.markets = markets or []



    def to_dict(self) -> Dict[str, Any]:

        return {

            "title": self.title,

            "source": self.source,

            "published_at": self.published_at,

            "content": self.content,

            "url": self.url,

            "sentiment": self.sentiment,

            "impact": self.impact,

            "markets": self.markets

        }



# =====================================================
# NEWS PROVIDER INTERFACE
# =====================================================

class BaseNewsProvider(ABC):

    """
    Interface لكل مصادر الأخبار

    جاهز لـ:
    - Reuters
    - Financial Modeling Prep
    - RSS
    - Crypto News API
    """


    @property
    @abstractmethod
    def provider_name(self) -> str:

        pass



    @abstractmethod
    def fetch_news(
        self,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[NewsItem]:

        pass




# =====================================================
# FALCON AI NEWS INTELLIGENCE ENGINE
# =====================================================

class NewsAnalyzer:


    def __init__(self):


        self.providers: List[
            BaseNewsProvider
        ] = []


        # الأسواق المدعومة

        self.supported_markets = [

            "crypto",
            "forex",
            "gold",
            "stocks",
            "oil",
            "indices"

        ]



        # الأخبار عالية التأثير

        self.high_impact_keywords = [

            "fed",
            "federal reserve",
            "interest rate",
            "rate decision",

            "inflation",
            "cpi",

            "nfp",
            "employment",

            "gdp",

            "unemployment",

            "central bank",

            "bond yield",

            "treasury",

            "recession",

            "crisis",

            "war",

            "sanctions"

        ]



        # ربط الأخبار بالأسواق


        self.market_keywords = {


            "crypto":[

                "bitcoin",
                "btc",
                "ethereum",
                "crypto",
                "blockchain"

            ],



            "forex":[

                "usd",
                "dollar",
                "euro",
                "eur",
                "currency"

            ],



            "gold":[

                "gold",
                "xau",
                "precious metal"

            ],



            "oil":[

                "oil",
                "brent",
                "wti",
                "energy"

            ],



            "stocks":[

                "stock",
                "shares",
                "nasdaq",
                "dow",
                "s&p"

            ],



            "indices":[

                "index",
                "market index"

            ]


        }



        # كلمات إيجابية

        self.positive_words = [

            "growth",
            "positive",
            "bullish",
            "strong",
            "increase",
            "recovery"

        ]



        # كلمات سلبية

        self.negative_words = [

            "crash",
            "negative",
            "bearish",
            "weak",
            "decline",
            "risk"

        ]



    # =====================================================
    # PROVIDERS
    # =====================================================


    def add_provider(
        self,
        provider: BaseNewsProvider
    ):

        self.providers.append(
            provider
        )



    def get_providers(self) -> List[str]:

        return [

            provider.provider_name

            for provider in self.providers

        ]



    # =====================================================
    # TEXT CLEANING
    # =====================================================


    def clean_text(
        self,
        text: str
    ) -> str:


        if not text:

            return ""


        text = re.sub(
            r"\s+",
            " ",
            text
        )


        return text.strip()



    # =====================================================
    # NEWS ID GENERATION
    # =====================================================

    def generate_news_id(
        self,
        title: str
    ) -> str:


        return hashlib.sha256(
            title.encode("utf-8")
        ).hexdigest()



    # =====================================================
    # NEWS IMPORTANCE FILTER
    # =====================================================

    def calculate_importance(
        self,
        title: str,
        content: str = ""
    ) -> Dict[str, Any]:


        text = (
            title +
            " " +
            content
        ).lower()



        score = 0


        matched = []



        for keyword in self.high_impact_keywords:


            if keyword in text:

                score += 10

                matched.append(
                    keyword
                )



        if score >= 40:

            impact = "high"


        elif score >= 20:

            impact = "medium"


        else:

            impact = "low"



        return {


            "impact": impact,


            "score": min(
                score,
                100
            ),


            "keywords": matched

        }



    # =====================================================
    # SENTIMENT ANALYSIS
    # =====================================================

    def analyze_sentiment(
        self,
        title: str,
        content: str = ""
    ) -> Dict[str, Any]:


        text = (

            title +

            " " +

            content

        ).lower()



        positive = 0

        negative = 0



        for word in self.positive_words:

            if word in text:

                positive += 1



        for word in self.negative_words:

            if word in text:

                negative += 1




        if positive > negative:

            sentiment = "positive"



        elif negative > positive:

            sentiment = "negative"



        else:

            sentiment = "neutral"



        total = positive + negative



        if total:

            confidence = int(

                max(
                    positive,
                    negative
                )
                /
                total
                *
                100

            )

        else:

            confidence = 0



        return {


            "sentiment": sentiment,


            "confidence": confidence,


            "positive_score": positive,


            "negative_score": negative

        }



    # =====================================================
    # MARKET DETECTION
    # =====================================================

    def detect_markets(
        self,
        text: str
    ) -> List[str]:


        text = text.lower()


        markets = []



        for market, keywords in self.market_keywords.items():


            for keyword in keywords:


                if keyword in text:


                    markets.append(
                        market
                    )

                    break



        return markets



    # =====================================================
    # PROCESS RAW NEWS
    # =====================================================

    def process_news(
        self,
        news: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:



        title = self.clean_text(

            news.get(
                "title",
                ""
            )

        )


        content = self.clean_text(

            news.get(
                "content",
                ""
            )

        )



        if not title:

            return None



        importance = self.calculate_importance(

            title,

            content

        )



        sentiment = self.analyze_sentiment(

            title,

            content

        )



        markets = self.detect_markets(

            title +

            " " +

            content

        )



        item = NewsItem(

            title=title,

            source= news.get(
                "source",
                "unknown"
            ),

            published_at= news.get(
                "published_at"
            ),

            content=content,

            url= news.get(
                "url"
            ),

            sentiment=sentiment["sentiment"],

            impact=importance["impact"],

            markets=markets

        )



        return {


            "id": self.generate_news_id(
                title
            ),


            "news": item.to_dict(),


            "analysis": {


                "impact": importance,


                "sentiment": sentiment,


                "markets": markets


            },



            "processed_at":
            datetime.utcnow().isoformat()


        }



    # =====================================================
    # REMOVE DUPLICATE NEWS
    # =====================================================

    def remove_duplicates(
        self,
        news_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:


        unique = {}

        result = []


        for news in news_list:

            news_id = news.get(
                "id"
            )


            if news_id not in unique:

                unique[news_id] = True

                result.append(
                    news
                )


        return result



    # =====================================================
    # FETCH FROM ALL PROVIDERS
    # =====================================================

    def fetch_all_news(
        self,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:


        collected = []



        for provider in self.providers:


            try:


                news_items = provider.fetch_news(

                    symbol=symbol,

                    category=category,

                    limit=limit

                )


                for item in news_items:


                    processed = self.process_news(

                        item.to_dict()

                    )


                    if processed:

                        collected.append(
                            processed
                        )


            except Exception as error:


                continue



        return self.remove_duplicates(
            collected
        )



    # =====================================================
    # SORT NEWS BY IMPACT
    # =====================================================

    def rank_news(
        self,
        news_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:


        impact_weight = {


            "high": 3,

            "medium": 2,

            "low": 1

        }



        return sorted(

            news_list,

            key=lambda x:

            impact_weight.get(

                x.get(
                    "news",
                    {}
                )
                .get(
                    "impact",
                    "low"
                ),

                1

            ),

            reverse=True

        )



    # =====================================================
    # COMPLETE NEWS PIPELINE
    # =====================================================

    def analyze_news_feed(
        self,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:


        news = self.fetch_all_news(

            symbol=symbol,

            category=category,

            limit=limit

        )


        ranked = self.rank_news(

            news

        )


        return {


            "count": len(ranked),


            "high_impact": [

                item

                for item in ranked

                if item["news"]["impact"] == "high"

            ],


            "news": ranked,


            "generated_at":

            datetime.utcnow().isoformat()

        }



# =====================================================
# RSS NEWS PROVIDER
# =====================================================

class RSSNewsProvider(BaseNewsProvider):


    def __init__(
        self,
        feed_urls: List[str]
    ):

        self.feed_urls = feed_urls



    @property
    def provider_name(self) -> str:

        return "RSS"



    def fetch_news(
        self,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[NewsItem]:


        news = []


        try:

            import feedparser


            for url in self.feed_urls:


                feed = feedparser.parse(
                    url
                )


                for item in feed.entries[:limit]:


                    news.append(

                        NewsItem(

                            title=item.get(
                                "title",
                                ""
                            ),

                            source="RSS",

                            published_at=item.get(
                                "published",
                                None
                            ),

                            content=item.get(
                                "summary",
                                ""
                            ),

                            url=item.get(
                                "link",
                                None
                            )

                        )

                    )


        except Exception:


            pass



        return news




# =====================================================
# FINANCIAL MODELING PREP PROVIDER
# =====================================================

class FinancialModelingPrepProvider(
    BaseNewsProvider
):


    def __init__(
        self,
        api_key: str
    ):

        self.api_key = api_key


        self.base_url = (
            "https://financialmodelingprep.com/api/v3"
        )



    @property
    def provider_name(self) -> str:

        return "FinancialModelingPrep"



    def fetch_news(
        self,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[NewsItem]:


        news = []


        try:

            import requests


            url = (

                f"{self.base_url}/stock_news"

                f"?limit={limit}"

                f"&apikey={self.api_key}"

            )


            response = requests.get(
                url,
                timeout=10
            )


            data = response.json()



            for item in data:


                news.append(

                    NewsItem(

                        title=item.get(
                            "title",
                            ""
                        ),

                        source="FinancialModelingPrep",

                        published_at=item.get(
                            "publishedDate"
                        ),

                        content=item.get(
                            "text",
                            ""
                        ),

                        url=item.get(
                            "url"
                        )

                    )

                )


        except Exception:


            pass



        return news




# =====================================================
# REUTERS PROVIDER INTERFACE
# =====================================================

class ReutersNewsProvider(
    BaseNewsProvider
):


    def __init__(
        self,
        api_key: Optional[str] = None
    ):

        self.api_key = api_key



    @property
    def provider_name(self) -> str:

        return "Reuters"



    def fetch_news(
        self,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[NewsItem]:


        """
        Reuters يحتاج اشتراك API رسمي.

        هذا المكان جاهز للربط
        عند إضافة المفتاح.
        """


        if not self.api_key:

            return []



        news = []



        # سيتم وضع اتصال Reuters الرسمي هنا


        return news



# =====================================================
# ECONOMIC EVENT MODEL
# =====================================================

class EconomicEvent:


    def __init__(
        self,
        name: str,
        country: str,
        date: str,
        actual: Optional[float] = None,
        forecast: Optional[float] = None,
        previous: Optional[float] = None,
        importance: str = "medium"
    ):


        self.name = name

        self.country = country

        self.date = date

        self.actual = actual

        self.forecast = forecast

        self.previous = previous

        self.importance = importance



    def to_dict(
        self
    ) -> Dict[str, Any]:


        return {


            "name": self.name,

            "country": self.country,

            "date": self.date,

            "actual": self.actual,

            "forecast": self.forecast,

            "previous": self.previous,

            "importance": self.importance

        }




# =====================================================
# ECONOMIC ANALYZER
# =====================================================

class EconomicAnalyzer:



    def __init__(self):


        self.events = []


        self.high_impact_events = [


            "interest rate",

            "fed decision",

            "cpi",

            "inflation",

            "nfp",

            "non farm payroll",

            "gdp",

            "unemployment"

        ]




    # =====================================================
    # ADD EVENT
    # =====================================================


    def add_event(
        self,
        event: EconomicEvent
    ):


        self.events.append(
            event
        )




    # =====================================================
    # EVENT IMPACT
    # =====================================================


    def analyze_event(
        self,
        event: EconomicEvent
    ) -> Dict[str, Any]:


        impact = "neutral"

        score = 0


        if (

            event.actual is not None

            and

            event.forecast is not None

        ):


            difference = (

                event.actual

                -

                event.forecast

            )



            if difference > 0:

                score = 1


            elif difference < 0:

                score = -1




        name = event.name.lower()



        # التضخم

        if "cpi" in name or "inflation" in name:


            if score > 0:


                impact = "negative_for_risk_assets"


            elif score < 0:


                impact = "positive_for_risk_assets"




        # الفائدة

        elif "rate" in name or "fed" in name:


            if score > 0:


                impact = "positive_for_usd"


            elif score < 0:


                impact = "negative_for_usd"




        # الوظائف

        elif "nfp" in name or "employment" in name:


            if score > 0:


                impact = "positive_for_usd"


            elif score < 0:


                impact = "negative_for_usd"



        return {


            "event": event.to_dict(),


            "impact": impact,


            "direction_score": score,


            "markets": self.market_effects(

                impact

            )


        }




    # =====================================================
    # MARKET EFFECT MAPPING
    # =====================================================


    def market_effects(
        self,
        impact: str
    ) -> Dict[str, str]:


        effects = {}



        if impact == "positive_for_usd":


            effects = {


                "forex": "USD strength",

                "gold": "possible pressure",

                "crypto": "possible pressure",

                "stocks": "mixed"

            }




        elif impact == "negative_for_usd":


            effects = {


                "forex": "USD weakness",

                "gold": "possible support",

                "crypto": "possible support",

                "stocks": "possible positive"

            }



        elif impact == "positive_for_risk_assets":


            effects = {


                "crypto": "positive",

                "stocks": "positive",

                "gold": "neutral"

            }



        elif impact == "negative_for_risk_assets":


            effects = {


                "crypto": "negative",

                "stocks": "negative",

                "gold": "possible safe haven"

            }



        return effects




    # =====================================================
    # FULL ECONOMIC REPORT
    # =====================================================


    def generate_report(
        self
    ) -> Dict[str, Any]:


        analyzed = []


        for event in self.events:


            analyzed.append(

                self.analyze_event(
                    event
                )

            )



        return {


            "events_count": len(

                analyzed

            ),


            "events": analyzed,


            "generated_at":

            datetime.utcnow().isoformat()

        }



# =====================================================
# ECONOMIC DATA PROVIDER INTERFACE
# =====================================================

class BaseEconomicProvider(ABC):


    """
    واجهة موحدة لمصادر البيانات الاقتصادية
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
# FINANCIAL MODELING PREP ECONOMIC PROVIDER
# =====================================================

class FMPEconomicProvider(
    BaseEconomicProvider
):


    def __init__(
        self,
        api_key: str
    ):

        self.api_key = api_key


        self.base_url = (
            "https://financialmodelingprep.com/api/v3"
        )



    @property
    def provider_name(
        self
    ) -> str:

        return "FinancialModelingPrep"



    def fetch_events(
        self,
        country: str = "US",
        limit: int = 50
    ) -> List[EconomicEvent]:


        events = []


        try:

            import requests



            url = (

                f"{self.base_url}"

                "/economic_calendar"

                f"?apikey={self.api_key}"

            )



            response = requests.get(

                url,

                timeout=10

            )



            data = response.json()



            for item in data[:limit]:


                events.append(

                    EconomicEvent(

                        name=item.get(
                            "event",
                            ""
                        ),

                        country=item.get(
                            "country",
                            country
                        ),

                        date=item.get(
                            "date",
                            ""
                        ),

                        actual=item.get(
                            "actual"
                        ),

                        forecast=item.get(
                            "estimate"
                        ),

                        previous=item.get(
                            "previous"
                        ),

                        importance=item.get(
                            "impact",
                            "medium"
                        )

                    )

                )


        except Exception:


            pass



        return events




# =====================================================
# ECONOMIC PROVIDER MANAGER
# =====================================================

class EconomicDataManager:



    def __init__(self):

        self.providers = []



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



    def fetch_all_events(
        self,
        country: str = "US",
        limit: int = 50
    ) -> List[EconomicEvent]:


        events = []



        for provider in self.providers:


            try:


                provider_events = provider.fetch_events(

                    country,

                    limit

                )


                events.extend(

                    provider_events

                )


            except Exception:


                continue



        return events



# =====================================================
# ECONOMIC IMPACT ENGINE
# =====================================================

class EconomicImpactEngine:


    def __init__(self):


        self.market_rules = {


            "interest_rate": {

                "usd": "high",

                "gold": "high",

                "crypto": "high",

                "stocks": "medium"

            },


            "cpi": {

                "usd": "high",

                "gold": "high",

                "crypto": "medium",

                "stocks": "high"

            },


            "nfp": {

                "usd": "high",

                "stocks": "medium",

                "crypto": "medium"

            },


            "gdp": {

                "stocks": "high",

                "crypto": "medium",

                "forex": "medium"

            },


            "unemployment": {

                "usd": "high",

                "stocks": "medium"

            }

        }




    # =====================================================
    # EVENT TYPE DETECTION
    # =====================================================


    def detect_event_type(
        self,
        event_name: str
    ) -> str:


        name = event_name.lower()



        if (
            "rate" in name
            or
            "fed" in name
            or
            "interest" in name
        ):

            return "interest_rate"



        if (
            "cpi" in name
            or
            "inflation" in name
        ):

            return "cpi"



        if (
            "nfp" in name
            or
            "non farm" in name
            or
            "employment" in name
        ):

            return "nfp"



        if "gdp" in name:

            return "gdp"



        if (
            "unemployment" in name
            or
            "jobless" in name
        ):

            return "unemployment"



        return "unknown"




    # =====================================================
    # IMPACT ANALYSIS
    # =====================================================


    def analyze(
        self,
        event: EconomicEvent
    ) -> Dict[str, Any]:


        event_type = self.detect_event_type(

            event.name

        )



        direction = "neutral"

        strength = 0



        if (

            event.actual is not None

            and

            event.forecast is not None

        ):


            if event.actual > event.forecast:


                direction = "positive"

                strength = 70



            elif event.actual < event.forecast:


                direction = "negative"

                strength = 70



        markets = self.get_market_impact(

            event_type,

            direction

        )



        return {


            "event": event.name,


            "type": event_type,


            "direction": direction,


            "impact_strength": strength,


            "markets": markets,


            "time": datetime.utcnow().isoformat()

        }




    # =====================================================
    # MARKET IMPACT MAPPING
    # =====================================================


    def get_market_impact(
        self,
        event_type: str,
        direction: str
    ) -> Dict[str, Any]:


        result = {}



        rules = self.market_rules.get(

            event_type,

            {}

        )



        for market, importance in rules.items():


            result[market] = {


                "importance": importance,


                "direction":

                self.calculate_direction(

                    event_type,

                    market,

                    direction

                )

            }



        return result




    # =====================================================
    # DIRECTION CALCULATION
    # =====================================================


    def calculate_direction(
        self,
        event_type: str,
        market: str,
        direction: str
    ) -> str:


        # قوة الدولار

        if event_type == "interest_rate":


            if market == "usd":

                return (

                    "bullish"

                    if direction == "positive"

                    else

                    "bearish"

                )



            if market in [

                "gold",

                "crypto"

            ]:


                return (

                    "bearish"

                    if direction == "positive"

                    else

                    "bullish"

                )




        # التضخم

        if event_type == "cpi":


            if market == "gold":


                return (

                    "bearish"

                    if direction == "positive"

                    else

                    "bullish"

                )



            if market == "crypto":


                return (

                    "bearish"

                    if direction == "positive"

                    else

                    "bullish"

                )



        # الأخبار الإيجابية العامة

        if direction == "positive":


            return "positive"



        elif direction == "negative":


            return "negative"



        return "neutral"



# =====================================================
# ECONOMIC ALERT SYSTEM
# =====================================================

class EconomicAlertSystem:


    def __init__(self):


        self.blocking_events = [

            "interest_rate",

            "cpi",

            "nfp",

            "gdp"

        ]


        self.warning_minutes = 30



    # =====================================================
    # CHECK EVENT RISK
    # =====================================================


    def check_event_risk(
        self,
        event: EconomicEvent
    ) -> Dict[str, Any]:


        event_name = event.name.lower()


        event_type = self.detect_type(

            event_name

        )


        risk = "low"

        block_trading = False



        if event_type in self.blocking_events:


            risk = "high"

            block_trading = True



        elif event.importance == "high":


            risk = "medium"



        return {


            "event": event.name,


            "type": event_type,


            "risk": risk,


            "block_trading": block_trading,


            "message":

            self.generate_message(

                risk,

                event.name

            )

        }




    # =====================================================
    # DETECT EVENT TYPE
    # =====================================================


    def detect_type(
        self,
        text: str
    ) -> str:


        if (

            "fed" in text

            or

            "rate" in text

            or

            "interest" in text

        ):

            return "interest_rate"



        if (

            "cpi" in text

            or

            "inflation" in text

        ):

            return "cpi"



        if (

            "nfp" in text

            or

            "employment" in text

        ):

            return "nfp"



        if "gdp" in text:

            return "gdp"



        return "normal"




    # =====================================================
    # MESSAGE GENERATOR
    # =====================================================


    def generate_message(
        self,
        risk: str,
        event: str
    ) -> str:



        if risk == "high":


            return (

                f"تحذير: خبر اقتصادي قوي ({event}) "

                "قد يسبب حركة عالية وتقلبات. "

                "تم تعطيل الإشارات مؤقتاً."

            )



        if risk == "medium":


            return (

                f"تنبيه: خبر متوسط التأثير ({event})"

            )



        return (

            "لا توجد مخاطر اقتصادية عالية حالياً."

        )




    # =====================================================
    # TRADING PERMISSION
    # =====================================================


    def can_trade(
        self,
        events: List[EconomicEvent]
    ) -> Dict[str, Any]:


        blocked = False

        reasons = []



        for event in events:


            result = self.check_event_risk(

                event

            )


            if result["block_trading"]:


                blocked = True


                reasons.append(

                    result["message"]

                )



        return {


            "allowed":

            not blocked,


            "blocked":

            blocked,


            "reasons":

            reasons

        }



# =====================================================
# FALCONAI ECONOMY ENGINE
# =====================================================

class EconomyEngine:


    def __init__(self):


        self.news_analyzer = NewsAnalyzer()


        self.economic_analyzer = EconomicAnalyzer()


        self.impact_engine = EconomicImpactEngine()


        self.alert_system = EconomicAlertSystem()



    # =====================================================
    # REGISTER NEWS PROVIDER
    # =====================================================


    def add_news_provider(
        self,
        provider: BaseNewsProvider
    ):


        self.news_analyzer.add_provider(

            provider

        )




    # =====================================================
    # REGISTER ECONOMIC PROVIDER
    # =====================================================


    def add_economic_provider(
        self,
        provider: BaseEconomicProvider
    ):


        if not hasattr(

            self,

            "economic_providers"

        ):

            self.economic_providers = []



        self.economic_providers.append(

            provider

        )




    # =====================================================
    # FULL ECONOMY ANALYSIS
    # =====================================================


    def analyze(
        self,
        symbol: Optional[str] = None,
        category: Optional[str] = None
    ) -> Dict[str, Any]:


        news_report = (

            self.news_analyzer.analyze_news_feed(

                symbol=symbol,

                category=category

            )

        )



        economic_events = []



        if hasattr(

            self,

            "economic_providers"

        ):


            for provider in self.economic_providers:


                try:


                    events = provider.fetch_events()


                    economic_events.extend(

                        events

                    )


                except Exception:


                    continue




        economic_reports = []



        for event in economic_events:


            analysis = self.impact_engine.analyze(

                event

            )


            economic_reports.append(

                analysis

            )




        trading_permission = (

            self.alert_system.can_trade(

                economic_events

            )

        )




        return {


            "symbol": symbol,


            "news": news_report,


            "economy": economic_reports,


            "trading_permission":

            trading_permission,


            "generated_at":

            datetime.utcnow().isoformat(),


            "engine":

            "FalconAI Economy Engine"

        }




    # =====================================================
    # STATUS
    # =====================================================


    def status(
        self
    ) -> Dict[str, Any]:


        return {


            "engine":

            "FalconAI Economy Engine",


            "status":

            "online",


            "news_providers":

            self.news_analyzer.get_providers()

    }



    # =================================================
    # NEWS NORMALIZATION
    # =================================================

    def normalize_news(
        self,
        news: NewsItem
    ) -> Dict[str, Any]:

        text = (
            news.title +
            " " +
            news.content
        ).lower()


        return {

            "title": news.title,

            "source": news.source,

            "content": news.content,

            "published_at": news.published_at,

            "url": news.url,

            "text": text

        }



    # =================================================
    # HIGH IMPACT DETECTION
    # =================================================

    def detect_high_impact(
        self,
        news: NewsItem
    ) -> Dict[str, Any]:


        normalized = self.normalize_news(
            news
        )


        text = normalized["text"]


        matches = []


        for keyword in self.high_impact_keywords:

            if keyword in text:

                matches.append(
                    keyword
                )



        impact = "LOW"


        if len(matches) >= 4:

            impact = "HIGH"


        elif len(matches) >= 2:

            impact = "MEDIUM"



        return {

            "impact": impact,

            "keywords": matches,

            "is_high_impact":
                len(matches) > 0

        }



    # =================================================
    # MARKET IMPACT MAPPING
    # =================================================

    def analyze_market_impact(
        self,
        news: NewsItem
    ) -> Dict[str, Any]:


        text = (
            news.title +
            " " +
            news.content
        ).lower()



        impact = {


            "crypto": "neutral",

            "forex": "neutral",

            "gold": "neutral",

            "stocks": "neutral",

            "oil": "neutral",

            "indices": "neutral"

        }



        # Interest Rate

        if (
            "interest rate" in text
            or "fed" in text
            or "rate hike" in text
        ):


            impact["forex"] = "positive_usd"

            impact["gold"] = "negative"

            impact["stocks"] = "negative"

            impact["crypto"] = "negative"



        # Inflation

        if (
            "inflation" in text
            or "cpi" in text
        ):


            impact["gold"] = "positive"

            impact["crypto"] = "positive"



        # Recession

        if "recession" in text:


            impact["stocks"] = "negative"

            impact["indices"] = "negative"

            impact["gold"] = "positive"



        # Oil

        if (
            "war" in text
            or "sanctions" in text
        ):


            impact["oil"] = "positive"

            impact["gold"] = "positive"



        return impact



# =====================================================
# NEWS SENTIMENT ENGINE
# =====================================================

class NewsSentimentEngine:


    def __init__(self):


        self.positive_words = [

            "growth",

            "strong",

            "positive",

            "bullish",

            "recovery",

            "upgrade",

            "approval",

            "support",

            "surge",

            "record",

            "خفض الفائدة",

            "تحسن",

            "نمو",

            "انتعاش"

        ]


        self.negative_words = [

            "crisis",

            "weak",

            "negative",

            "bearish",

            "recession",

            "downgrade",

            "risk",

            "collapse",

            "war",

            "sanctions",

            "رفع الفائدة",

            "تضخم",

            "أزمة",

            "ركود"

        ]



    # =====================================================
    # TEXT SENTIMENT ANALYSIS
    # =====================================================


    def analyze(
        self,
        news: NewsItem
    ) -> Dict[str, Any]:


        text = (

            news.title

            +

            " "

            +

            news.content

        ).lower()



        positive_score = 0

        negative_score = 0



        for word in self.positive_words:


            if word in text:

                positive_score += 1



        for word in self.negative_words:


            if word in text:

                negative_score += 1



        total = (

            positive_score

            +

            negative_score

        )



        sentiment = "neutral"

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



            if positive_score > negative_score:


                sentiment = "positive"



            elif negative_score > positive_score:


                sentiment = "negative"



        return {


            "sentiment":

                sentiment,


            "confidence":

                confidence,


            "positive_score":

                positive_score,


            "negative_score":

                negative_score,


            "analyzed_at":

                datetime.utcnow().isoformat()

        }




    # =====================================================
    # MARKET SENTIMENT EFFECT
    # =====================================================


    def market_sentiment(
        self,
        sentiment: str
    ) -> Dict[str, str]:


        if sentiment == "positive":


            return {


                "crypto": "bullish",

                "stocks": "bullish",

                "gold": "neutral",

                "forex": "positive_risk"

            }



        if sentiment == "negative":


            return {


                "crypto": "bearish",

                "stocks": "bearish",

                "gold": "bullish",

                "forex": "risk_off"

            }



        return {


            "crypto": "neutral",

            "stocks": "neutral",

            "gold": "neutral",

            "forex": "neutral"

            }



# =====================================================
# ECONOMIC EVENT INTELLIGENCE ENGINE
# =====================================================


class EconomicEventEngine:


    def __init__(self):


        self.events = {


            "interest_rate": {

                "keywords": [

                    "fed",

                    "interest rate",

                    "rate decision",

                    "central bank"

                ],

                "impact": "HIGH"

            },


            "inflation": {

                "keywords": [

                    "cpi",

                    "inflation",

                    "consumer price"

                ],

                "impact": "HIGH"

            },


            "employment": {

                "keywords": [

                    "nfp",

                    "non farm payroll",

                    "employment",

                    "jobs"

                ],

                "impact": "HIGH"

            },


            "gdp": {

                "keywords": [

                    "gdp",

                    "economic growth"

                ],

                "impact": "MEDIUM"

            },


            "unemployment": {

                "keywords": [

                    "unemployment",

                    "jobless rate"

                ],

                "impact": "MEDIUM"

            },


            "bonds": {

                "keywords": [

                    "bond yield",

                    "treasury",

                    "10 year yield",

                    "government bonds"

                ],

                "impact": "HIGH"

            }

        }




    # =====================================================
    # EVENT DETECTION
    # =====================================================


    def detect_event(
        self,
        news: NewsItem
    ) -> Dict[str, Any]:


        text = (

            news.title

            +

            " "

            +

            news.content

        ).lower()



        detected = "unknown"

        impact = "LOW"



        for event, data in self.events.items():


            for keyword in data["keywords"]:


                if keyword in text:


                    detected = event

                    impact = data["impact"]

                    break



            if detected != "unknown":

                break



        return {


            "event_type":

                detected,


            "impact_level":

                impact

        }




    # =====================================================
    # ECONOMIC RESULT ANALYSIS
    # =====================================================


    def compare_result(
        self,
        actual: Optional[float],
        forecast: Optional[float]
    ) -> Dict[str, Any]:


        if actual is None or forecast is None:


            return {


                "status": "no_data",

                "direction": "neutral"

            }




        difference = actual - forecast



        if difference > 0:


            return {


                "status": "better_than_expected",

                "direction": "positive",

                "difference": difference

            }



        elif difference < 0:


            return {


                "status": "worse_than_expected",

                "direction": "negative",

                "difference": difference

            }



        return {


            "status": "as_expected",

            "direction": "neutral",

            "difference": 0

        }




    # =====================================================
    # MARKET CONSEQUENCE
    # =====================================================


    def calculate_market_effect(
        self,
        event_type: str,
        direction: str
    ) -> Dict[str, str]:


        result = {


            "crypto": "neutral",

            "gold": "neutral",

            "forex": "neutral",

            "stocks": "neutral",

            "bonds": "neutral"

        }



        if event_type == "interest_rate":


            if direction == "positive":


                result["forex"] = "USD bullish"

                result["gold"] = "bearish"

                result["crypto"] = "bearish"



            elif direction == "negative":


                result["forex"] = "USD bearish"

                result["gold"] = "bullish"

                result["crypto"] = "bullish"




        elif event_type == "inflation":


            if direction == "positive":


                result["gold"] = "bullish"

                result["crypto"] = "bullish"



        elif event_type == "employment":


            result["forex"] = (

                "USD reaction possible"

            )


            result["stocks"] = (

                "High volatility"

            )




        elif event_type == "bonds":


            result["gold"] = (

                "Yield sensitivity"

            )


            result["stocks"] = (

                "Rate sensitivity"

            )



        return result



# =====================================================
# HISTORICAL NEWS LEARNING ENGINE
# =====================================================


class HistoricalNewsLearning:


    def __init__(self):


        # ذاكرة مؤقتة
        self.history: List[Dict[str, Any]] = []



    # =====================================================
    # SAVE NEWS EVENT
    # =====================================================


    def save_event(
        self,
        news: NewsItem,
        analysis: Dict[str, Any],
        market_result: Optional[Dict[str, Any]] = None
    ):


        record = {


            "news": news.to_dict(),


            "analysis": analysis,


            "market_result":

                market_result or {},


            "created_at":

                datetime.utcnow().isoformat()

        }



        self.history.append(

            record

        )




    # =====================================================
    # SEARCH SIMILAR EVENTS
    # =====================================================


    def find_similar_events(
        self,
        event_type: str
    ) -> List[Dict[str, Any]]:



        results = []



        for item in self.history:


            analysis = item.get(

                "analysis",

                {}

            )


            if (

                analysis.get(
                    "event_type"
                )

                ==

                event_type

            ):


                results.append(

                    item

                )



        return results




    # =====================================================
    # LEARNING ACCURACY
    # =====================================================


    def calculate_accuracy(
        self
    ) -> Dict[str, Any]:


        total = len(

            self.history

        )


        if total == 0:


            return {


                "accuracy": 0,

                "samples": 0

            }



        correct = 0



        for item in self.history:


            analysis = item.get(

                "analysis",

                {}

            )


            result = item.get(

                "market_result",

                {}

            )


            predicted = analysis.get(

                "direction"

            )


            actual = result.get(

                "direction"

            )


            if (

                predicted

                and

                actual

                and

                predicted == actual

            ):


                correct += 1




        accuracy = int(

            (

                correct / total

            )

            *

            100

        )



        return {


            "accuracy":

                accuracy,


            "correct":

                correct,


            "samples":

                total

        }




    # =====================================================
    # PREDICT FROM HISTORY
    # =====================================================


    def predict_effect(
        self,
        event_type: str
    ) -> Dict[str, Any]:


        similar = self.find_similar_events(

            event_type

        )



        if not similar:


            return {


                "prediction":

                    "unknown",


                "confidence":

                    0

            }




        bullish = 0

        bearish = 0



        for item in similar:


            direction = item.get(

                "market_result",

                {}

            ).get(

                "direction"

            )



            if direction == "positive":

                bullish += 1



            elif direction == "negative":

                bearish += 1




        total = bullish + bearish



        if total == 0:


            return {


                "prediction":

                    "neutral",


                "confidence":

                    0

            }



        if bullish > bearish:


            prediction = "positive"



        else:


            prediction = "negative"



        confidence = int(

            (

                max(

                    bullish,

                    bearish

                )

                /

                total

            )

            *

            100

        )



        return {


            "prediction":

                prediction,


            "confidence":

                confidence,


            "samples":

                total

        }



# =====================================================
# NEWS API PROVIDERS LAYER
# =====================================================

import requests


# =====================================================
# GENERIC API PROVIDER
# =====================================================


class APIProvider(BaseNewsProvider):


    def __init__(
        self,
        name: str,
        api_key: Optional[str] = None
    ):


        self._provider_name = name

        self.api_key = api_key



    @property
    def provider_name(
        self
    ) -> str:

        return self._provider_name




    def fetch_news(
        self,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[NewsItem]:

        return []




# =====================================================
# REUTERS PROVIDER
# =====================================================


class ReutersProvider(APIProvider):


    def __init__(
        self,
        api_key: Optional[str] = None
    ):

        super().__init__(

            "Reuters",

            api_key

        )



    def fetch_news(
        self,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[NewsItem]:


        news = []

        # API connection will be activated
        # after adding production key


        return news




# =====================================================
# FINANCIAL MODELING PREP PROVIDER
# =====================================================


class FinancialModelingPrepProvider(APIProvider):


    BASE_URL = (

        "https://financialmodelingprep.com/api/v3"

    )



    def __init__(
        self,
        api_key: Optional[str] = None
    ):

        super().__init__(

            "FinancialModelingPrep",

            api_key

        )




    def fetch_news(
        self,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[NewsItem]:


        news = []



        if not self.api_key:

            return news



        try:


            url = (

                f"{self.BASE_URL}/stock_news"

            )


            params = {


                "limit":

                    limit,


                "apikey":

                    self.api_key

            }



            if symbol:

                params["tickers"] = symbol



            response = requests.get(

                url,

                params=params,

                timeout=10

            )



            data = response.json()



            for item in data:


                news.append(

                    NewsItem(

                        title=item.get(
                            "title",
                            ""
                        ),

                        source="FinancialModelingPrep",

                        content=item.get(
                            "text",
                            ""
                        ),

                        url=item.get(
                            "url"
                        )

                    )

                )



        except Exception:


            pass



        return news




# =====================================================
# RSS NEWS PROVIDER
# =====================================================


class RSSNewsProvider(APIProvider):


    def __init__(self):


        super().__init__(

            "RSS"

        )



    def fetch_news(
        self,
        symbol: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[NewsItem]:


        # جاهز لإضافة:
        # Reuters RSS
        # Investing RSS
        # Central Banks RSS


        return []



# =====================================================
# FINAL NEWS INTELLIGENCE ENGINE
# =====================================================


class NewsIntelligenceEngine:


    def __init__(self):


        self.analyzer = NewsAnalyzer()

        self.sentiment = NewsSentimentEngine()

        self.economic = EconomicEventEngine()

        self.history = HistoricalNewsLearning()




    # =====================================================
    # FULL NEWS ANALYSIS
    # =====================================================


    def analyze_news(
        self,
        news: NewsItem
    ) -> Dict[str, Any]:


        normalized = (

            self.analyzer.normalize_news(
                news
            )

        )


        impact = (

            self.analyzer.detect_high_impact(
                news
            )

        )


        market_effect = (

            self.analyzer.analyze_market_impact(
                news
            )

        )


        sentiment = (

            self.sentiment.analyze(
                news
            )

        )


        economic_event = (

            self.economic.detect_event(
                news
            )

        )



        historical_prediction = (

            self.history.predict_effect(

                economic_event.get(
                    "event_type",
                    "unknown"
                )

            )

        )



        result = {


            "news":

                normalized,


            "impact":

                impact,


            "sentiment":

                sentiment,


            "economic_event":

                economic_event,


            "market_effect":

                market_effect,


            "historical_prediction":

                historical_prediction,


            "analysis_time":

                datetime.utcnow().isoformat()

        }



        # حفظ التعلم

        self.history.save_event(

            news,

            economic_event,

            market_effect

        )



        return result




    # =====================================================
    # MULTIPLE NEWS ANALYSIS
    # =====================================================


    def analyze_batch(
        self,
        news_list: List[NewsItem]
    ) -> List[Dict[str, Any]]:


        results = []



        for news in news_list:


            try:


                results.append(

                    self.analyze_news(
                        news
                    )

                )


            except Exception:


                continue



        return results




    # =====================================================
    # SYSTEM STATUS
    # =====================================================


    def status(
        self
    ) -> Dict[str, Any]:


        return {


            "engine":

                "News Intelligence Engine",


            "status":

                "online",


            "modules":

            [

                "News Analyzer",

                "Sentiment NLP",

                "Economic Events",

                "Market Impact",

                "Historical Learning",

                "API Providers"

            ]


        }
