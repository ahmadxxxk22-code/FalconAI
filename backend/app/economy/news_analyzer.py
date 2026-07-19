from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod


# =====================================================
# News Data Model
# =====================================================

class NewsItem:

    """
    Standard FalconAI News Object

    يمثل خبر موحد مهما كان مصدره
    """


    def __init__(
        self,
        title: str,
        source: str,
        published_at: Optional[str] = None,
        content: Optional[str] = None,
        url: Optional[str] = None
    ):

        self.title = title

        self.source = source

        self.published_at = (
            published_at
            or datetime.utcnow().isoformat()
        )

        self.content = content or ""

        self.url = url



    def to_dict(self) -> Dict[str, Any]:

        return {

            "title": self.title,

            "source": self.source,

            "published_at": self.published_at,

            "content": self.content,

            "url": self.url

        }



# =====================================================
# News Provider Interface
# =====================================================

class BaseNewsProvider(ABC):

    """
    واجهة موحدة لجميع مصادر الأخبار

    لاحقاً يمكن إضافة:
    - Bloomberg API
    - Reuters API
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
# FalconAI News Analyzer
# =====================================================

class NewsAnalyzer:


    def __init__(self):

        self.providers: List[
            BaseNewsProvider
        ] = []


        self.supported_markets = [

            "crypto",

            "forex",

            "gold",

            "stocks",

            "oil",

            "indices"

        ]


        self.high_impact_keywords = [

            "fed",

            "interest rate",

            "inflation",

            "cpi",

            "nfp",

            "gdp",

            "unemployment",

            "central bank",

            "bond yield"

        ]



    # =================================================
    # Provider Management
    # =================================================


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
