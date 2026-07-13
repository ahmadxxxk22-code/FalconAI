from app.ai.trend_engine import TrendEngine


class MultiTimeframeEngine:

    def __init__(self):

        self.trend = TrendEngine()

        # الفريمات المستخدمة للتحليل
        self.timeframes = {

            "15m": 1,

            "1h": 2,

            "4h": 3,

            "1d": 4,

            "1w": 5,

            "1M": 6

        }


    def analyze(

        self,

        symbol="BTCUSDT",

        market="crypto"

    ):

        results = []

        total_score = 0

        total_weight = 0


        bullish_count = 0

        bearish_count = 0

        sideways_count = 0


        for interval, weight in self.timeframes.items():

            try:

                analysis = self.trend.analyze(

                    symbol=symbol,

                    interval=interval,

                    market=market

                )


                score = analysis.get(

                    "score",

                    0

                )


                weighted_score = score * weight


                total_score += weighted_score

                total_weight += weight


                trend = analysis.get(

                    "trend",

                    "SIDEWAYS"

                )


                if "BULL" in trend:

                    bullish_count += 1


                elif "BEAR" in trend:

                    bearish_count += 1


                else:

                    sideways_count += 1



                results.append({

                    "interval": interval,

                    "weight": weight,

                    "score": score,

                    "weighted_score": weighted_score,

                    "trend": trend,

                    "rsi": analysis.get("rsi"),

                    "macd": analysis.get("macd"),

                    "momentum": analysis.get("momentum"),

                    "reasons": analysis.get("reasons", [])

                })


            except Exception as e:


                results.append({

                    "interval": interval,

                    "error": str(e)

                })



        if total_weight == 0:

            average_score = 0

        else:

            average_score = round(

                total_score / total_weight,

                2

            )



        signal = self.calculate_signal(

            average_score

        )


        confidence = self.calculate_confidence(

            average_score,

            bullish_count,

            bearish_count,

            len(self.timeframes)

        )


        investor_view = self.investor_summary(

            signal,

            confidence,

            bullish_count,

            bearish_count

        )


        return {

            "symbol": symbol,

            "market": market,

            "signal": signal,

            "confidence": confidence,

            "average_score": average_score,

            "bullish_timeframes": bullish_count,

            "bearish_timeframes": bearish_count,

            "sideways_timeframes": sideways_count,

            "investor_summary": investor_view,

            "timeframes": results

        }



    def calculate_signal(

        self,

        score

    ):


        if score >= 70:

            return "STRONG_BUY"


        if score >= 35:

            return "BUY"


        if score <= -70:

            return "STRONG_SELL"


        if score <= -35:

            return "SELL"


        return "WAIT"



    def calculate_confidence(

        self,

        score,

        bullish,

        bearish,

        total

    ):


        agreement = max(

            bullish,

            bearish

        ) / total * 100


        score_power = abs(score)


        confidence = (

            agreement * 0.6

            +

            score_power * 0.4

        )


        return round(

            min(confidence, 100),

            2

        )



    def investor_summary(

        self,

        signal,

        confidence,

        bullish,

        bearish

    ):


        if signal in [

            "STRONG_BUY",

            "BUY"

        ]:

            return (

                f"الاتجاه العام إيجابي. "

                f"توافق {bullish} أطر زمنية "

                f"مع ثقة {confidence}%."

                " مناسب لدراسة فرص الشراء "

                "مع إدارة المخاطر."

            )


        if signal in [

            "STRONG_SELL",

            "SELL"

        ]:

            return (

                f"الاتجاه العام سلبي. "

                f"توافق {bearish} أطر زمنية "

                f"مع ثقة {confidence}%."

                " يفضل الحذر وإدارة المراكز."

            )


        return (

            "السوق غير واضح حاليًا. "

            "يوجد تضارب بين الأطر الزمنية، "

            "ويفضل انتظار إشارة أقوى."

                )
