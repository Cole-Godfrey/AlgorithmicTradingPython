# region imports
from AlgorithmImports import *


# endregion

class SimpleTradingBot(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2020, 1, 1)
        self.set_end_date(2021, 1, 1)
        self.set_cash(100000)

        spy = self.add_equity("SPY", Resolution.DAILY)
        # self.add_forex, self.add_future...

        spy.set_data_normalization_mode(DataNormalizationMode.RAW)

        self.spy = spy.symbol

        self.set_benchmark("SPY")
        self.set_brokerage_model(BrokerageName.INTERACTIVE_BROKERS_BROKERAGE, AccountType.MARGIN)

        self.entryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime = self.time

    def on_data(self, data: Slice):
        if not self.spy in data:
            return
        bar = data[self.spy]
        if bar is None:
            return

        # price = data.bars[self.spy].close
        price = bar.close
        # price = self.securities[self.spy].close

        if not self.portfolio.invested:
            if self.nextEntryTime <= self.time:
                self.set_holdings(self.spy, 1)
                # self.market_order(self.spy, int(self.portfolio.cash / price))
                self.log("BUY SPY @ " + str(price))
                self.entryPrice = price
        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price:
            self.liquidate()
            self.log("SELL SPY @ " + str(price))
            self.nextEntryTime = self.time + self.period
