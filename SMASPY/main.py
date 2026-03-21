from collections import deque

# region imports
from AlgorithmImports import *


# endregion

class SMASPY(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2016, 1, 1)
        self.set_end_date(2026, 1, 1)
        self.set_cash(100000)
        self.spy = self.add_equity("SPY", Resolution.DAILY).symbol

        # self.SMA = self.sma(self.spy, 30, Resolution.DAILY)
        # closing_prices = self.history(self.spy, 30, Resolution.DAILY)["close"]
        # for time, price in closing_prices.loc[self.spy].items():
        #     self.SMA.update(time, price)

        self.SMA = CustomSimpleMovingAverage("CustomSMA", 30)
        self.register_indicator(self.spy, self.SMA, Resolution.DAILY)

    def on_data(self, data: Slice):
        if not self.SMA.is_ready:
            return

        hist = self.history(self.spy, timedelta(365), Resolution.DAILY)
        low = min(hist["low"])
        high = max(hist["high"])

        price = self.securities[self.spy].price

        if price * 1.05 >= high and self.SMA.current.value < price:
            if not self.portfolio[self.spy].is_long:
                self.set_holdings(self.spy, 1)

        elif price * 0.95 <= low and self.SMA.current.value > price:
            if not self.portfolio[self.spy].is_short:
                self.set_holdings(self.spy, -1)

        else:
            self.liquidate()

        self.plot("Benchmark", "52w-High", high)
        self.plot("Benchmark", "52w-Low", low)
        self.plot("Benchmark", "SMA", self.SMA.current.value)


class CustomSimpleMovingAverage(PythonIndicator):
    def __init__(self, name, period):
        self.name = name
        self.time = datetime.min
        self.value = 0
        self.queue = deque(maxlen=period)

    def update(self, input):
        self.queue.appendleft(input.close)
        self.time = input.end_time
        count = len(self.queue)
        self.value = sum(self.queue) / count
        return (count == self.queue.maxlen)