# region imports
from AlgorithmImports import *
# endregion

from nltk.sentiment import SentimentIntensityAnalyzer


class XTradingBot(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2022, 7, 5)
        self.set_end_date(2023, 6, 13)
        self.set_cash(100000)

        self.tsla = self.add_equity("TSLA", Resolution.MINUTE).symbol
        self.musk = self.add_data(MuskTweet, "MUSKTWTS", Resolution.MINUTE).symbol
        self.schedule.on(self.date_rules.every_day(self.tsla),
                         self.time_rules.before_market_close(self.tsla, 15),
                         self.exit_positions)

    def on_data(self, data: Slice):
        if self.musk in data:
            score = data[self.musk].value
            content = data[self.musk].tweet

            if score > 0.5:
                self.set_holdings(self.tsla, 1)
            elif score < -0.5:
                self.set_holdings(self.tsla, -1)

            if abs(score) > 0.5:
                self.log("Score: " + str(score) + ", Tweet: " + content)

    def exit_positions(self):
        self.liquidate()


class MuskTweet(PythonData):
    sia = SentimentIntensityAnalyzer()

    def get_source(self, config, date, isLive):
        source = "https://www.dropbox.com/scl/fi/fcmh0d6s2fyd7gaprs6nc/MuskTweetsPreProcessed.csv?rlkey=k5ghcihljt573fgnz4jjwiguk&e=1&st=lozo0lxm&dl=1"
        return SubscriptionDataSource(source, SubscriptionTransportMedium.REMOTE_FILE)

    def reader(self, config, line, date, isLive):
        if not (line.strip() and line[0].isdigit()):
            return None
        data = line.split(",", 1)
        tweet = MuskTweet()
        try:
            tweet.symbol = config.symbol
            tweet.time = datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S%z") + timedelta(minutes=1)
            content = data[1].lower()

            if "tsla" in content or "tesla" in content:
                tweet.value = self.sia.polarity_scores(content)["compound"]
            else:
                tweet.value = 0

            tweet["Tweet"] = str(content)
        except ValueError:
            return None

        return tweet