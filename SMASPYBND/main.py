# region imports
from AlgorithmImports import *


# endregion

class AdaptableFluorescentOrangeManatee(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2016, 1, 1)
        self.set_end_date(2026, 1, 1)
        self.set_cash(100000)
        self.spy = self.add_equity("SPY", Resolution.DAILY).symbol
        self.bnd = self.add_equity("BND", Resolution.DAILY).symbol

        sma_param = self.get_parameter("sma_length")
        length = 30 if sma_param is None else int(sma_param)

        self.SMA = self.sma(self.spy, length, Resolution.DAILY)
        self.rebalanceTime = datetime.min
        self.uptrend = True

    def on_data(self, data: Slice):
        if not self.SMA.is_ready or self.spy not in data or self.bnd not in data:
            return

        if data[self.spy].price >= self.SMA.current.value:
            if self.time >= self.rebalanceTime or not self.uptrend:
                self.set_holdings(self.spy, 0.8)
                self.set_holdings(self.bnd, 0.2)
                self.uptrend = True
                self.rebalanceTime = self.time + timedelta(30)
        elif self.time >= self.rebalanceTime or not self.uptrend:
            self.set_holdings(self.spy, 0.2)
            self.set_holdings(self.bnd, 0.8)
            self.uptrend = False
            self.rebalanceTime = self.time + timedelta(30)
        self.plot("Benchmark", "SMA", self.SMA.current.value)