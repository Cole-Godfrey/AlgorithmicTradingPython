# region imports
from AlgorithmImports import *


# endregion

class SizeEffect(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2016, 1, 1)
        self.set_end_date(2026, 1, 1)
        self.set_cash(100000)

        self.rebalanceTime = datetime.min
        self.activeStocks = set()

        self.add_universe(self.coarseFilter, self.fineFilter)
        self.universe_settings.resolution = Resolution.HOUR

        self.portfolioTargets = []

    def on_data(self, data: Slice):
        if self.portfolioTargets == []:
            return

        for symbol in self.activeStocks:
            if symbol not in data:
                return

        self.set_holdings(self.portfolioTargets)
        self.portfolioTargets = []

    def coarseFilter(self, coarse):
        if self.time <= self.rebalanceTime:
            return self.universe.unchanged
        self.rebalanceTime = self.time + timedelta(30)
        sortedByDollarVolume = sorted(coarse, key=lambda x: x.dollar_volume, reverse=True)
        return [x.symbol for x in sortedByDollarVolume if x.price > 10 and x.has_fundamental_data][:200]

    def fineFilter(self, fine):
        sortedByMarketCap = sorted(fine, key=lambda x: x.market_cap)
        return [x.symbol for x in sortedByMarketCap if x.market_cap > 0][:10]

    def on_securities_changed(self, changes):
        for x in changes.removed_securities:
            self.liquidate(x.symbol)
            self.activeStocks.remove(x.symbol)

        for x in changes.added_securities:
            self.activeStocks.add(x.symbol)

        self.portfolioTargets = [PortfolioTarget(symbol, 1 / len(self.activeStocks)) for symbol in self.activeStocks]
