import statistics



class HistoricalLearning:


    def analyze(
        self,
        candles
    ):


        if len(candles) < 300:

            return {

                "trend_probability": 50,

                "bullish": False,

                "bearish": False,

                "volatility": 0,

                "average_move": 0,

                "historical_similarity": 0,

                "confidence": 0

            }



        closes = [

            c["close"]

            for c in candles

        ]



        returns = []



        for i in range(
            1,
            len(closes)
        ):


            move = (

                closes[i] -
                closes[i-1]

            ) / closes[i-1]


            returns.append(move)



        average_move = statistics.mean(
            returns
        )


        volatility = statistics.stdev(
            returns
        )



        bullish_moves = len(

            [

                x for x in returns

                if x > 0

            ]

        )


        bearish_moves = len(

            [

                x for x in returns

                if x < 0

            ]

        )



        total = len(
            returns
        )



        bullish_probability = (

            bullish_moves /
            total

        ) * 100



        bearish_probability = (

            bearish_moves /
            total

        ) * 100



        probability = 50



        if bullish_probability > 55:

            probability += 25


        elif bearish_probability > 55:

            probability -= 25



        similarity = self.compare_recent_pattern(

            returns

        )



        confidence = abs(

            probability - 50

        ) + similarity



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
                4
            ),


            "average_move":

            round(
                average_move,
                5
            ),


            "historical_similarity":

            round(
                similarity,
                2
            ),


            "bullish_probability":

            round(
                bullish_probability,
                2
            ),


            "bearish_probability":

            round(
                bearish_probability,
                2
            ),


            "confidence":

            round(
                confidence,
                2
            )

        }




    def compare_recent_pattern(
        self,
        returns
    ):


        if len(returns) < 100:

            return 0



        recent = returns[-20:]

        matches = 0



        history = returns[:-20]



        for i in range(

            0,

            len(history)-20

        ):


            old = history[i:i+20]



            difference = sum(

                abs(

                    recent[j] -
                    old[j]

                )

                for j in range(20)

            )



            if difference < 0.05:

                matches += 1



        similarity = (

            matches /
            max(
                len(history),
                1
            )

        ) * 100



        return min(

            similarity * 10,

            100

        )
