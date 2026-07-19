import statistics



class HistoricalLearning:


    def __init__(self):

        self.lookback_window = 20

        self.minimum_history = 300



    # ==================================================
    # Returns Calculation
    # ==================================================


    def calculate_returns(
        self,
        closes
    ):


        returns = []


        for i in range(
            1,
            len(closes)
        ):


            if closes[i-1] == 0:

                continue



            move = (

                closes[i]
                -
                closes[i-1]

            ) / closes[i-1]


            returns.append(move)



        return returns



    # ==================================================
    # Volatility
    # ==================================================


    def calculate_volatility(
        self,
        returns
    ):


        if len(returns) < 2:

            return 0


        return statistics.stdev(
            returns
        )



    # ==================================================
    # Drawdown
    # ==================================================


    def calculate_drawdown(
        self,
        closes
    ):


        peak = closes[0]

        max_drop = 0



        for price in closes:


            if price > peak:

                peak = price



            drop = (

                peak - price

            ) / peak



            if drop > max_drop:

                max_drop = drop



        return max_drop * 100



    # ==================================================
    # Historical Pattern Similarity
    # ==================================================


    def compare_recent_pattern(
        self,
        returns
    ):


        if len(returns) < 100:

            return 0



        recent = returns[
            -self.lookback_window:
        ]



        history = returns[
            :-self.lookback_window
        ]



        matches = 0

        best_similarity = 0



        for i in range(

            0,

            len(history)
            -
            self.lookback_window

        ):


            old = history[

                i:
                i + self.lookback_window

            ]



            difference = sum(

                abs(

                    recent[j]
                    -
                    old[j]

                )

                for j in range(
                    self.lookback_window
                )

            )



            similarity = max(

                0,

                100 -
                (
                    difference * 100
                )

            )



            if similarity > best_similarity:

                best_similarity = similarity



            if difference < 0.05:

                matches += 1



        frequency = (

            matches /
            max(
                len(history),
                1
            )

        ) * 100



        return round(

            min(

                (
                    frequency * 10
                )
                +
                (
                    best_similarity * 0.5
                ),

                100

            ),

            2

        )



    # ==================================================
    # Future Bias From History
    # ==================================================


    def historical_bias(
        self,
        returns
    ):


        if not returns:

            return {

                "bullish_probability":50,

                "bearish_probability":50

            }



        bullish = len(

            [

                x for x in returns

                if x > 0

            ]

        )



        bearish = len(

            [

                x for x in returns

                if x < 0

            ]

        )



        total = bullish + bearish



        if total == 0:

            return {

                "bullish_probability":50,

                "bearish_probability":50

            }



        return {


            "bullish_probability":

            round(

                bullish /
                total
                * 100,

                2

            ),



            "bearish_probability":

            round(

                bearish /
                total
                * 100,

                2

            )

        }



    # ==================================================
    # Main Historical Analysis
    # ==================================================


    def analyze(
        self,
        candles
    ):


        if len(candles) < self.minimum_history:

            return {


                "trend_probability":50,

                "bullish":False,

                "bearish":False,


                "volatility":0,

                "average_move":0,

                "historical_similarity":0,


                "max_drawdown":0,


                "bullish_probability":50,

                "bearish_probability":50,


                "confidence":0

            }



        closes = [

            c["close"]

            for c in candles

        ]



        returns = self.calculate_returns(

            closes

        )



        if not returns:

            return {}



        average_move = statistics.mean(

            returns

        )



        volatility = self.calculate_volatility(

            returns

        )



        bias = self.historical_bias(

            returns

        )



        similarity = self.compare_recent_pattern(

            returns

        )



        drawdown = self.calculate_drawdown(

            closes

        )



        probability = 50



        if bias["bullish_probability"] > 55:

            probability += 25



        elif bias["bearish_probability"] > 55:

            probability -= 25



        if similarity > 50:


            if average_move > 0:

                probability += 10


            elif average_move < 0:

                probability -= 10



        probability = max(

            min(
                probability,
                100
            ),

            0

        )



        confidence = (

            abs(
                probability - 50
            )

            +

            similarity * 0.4

        )



        confidence = min(

            confidence,

            100

        )



        return {


            "trend_probability":

            round(

                probability,

                2

            ),



            "bullish":

            probability > 60,



            "bearish":

            probability < 40,



            "volatility":

            round(

                volatility,

                5

            ),



            "average_move":

            round(

                average_move,

                6

            ),



            "historical_similarity":

            round(

                similarity,

                2

            ),



            "max_drawdown":

            round(

                drawdown,

                2

            ),



            "bullish_probability":

            bias["bullish_probability"],



            "bearish_probability":

            bias["bearish_probability"],



            "confidence":

            round(

                confidence,

                2

            )

        }
