# region imports
from AlgorithmImports import *
# endregion

from System.Drawing import Color

class FatRedOrangeOwl(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2016, 1, 1)
        self.set_end_date(2026, 1, 1)
        self.set_cash(100000)
        self.pair = self.add_forex("EURUSD", Resolution.DAILY, Market.OANDA).symbol
        self.BB = self.bb(self.pair, 20, 2)

        stockPlot = Chart("Trade Plot")
        stockPlot.add_series(Series("Buy", SeriesType.SCATTER, "$", Color.GREEN, ScatterMarkerSymbol.TRIANGLE))
        stockPlot.add_series(Series("Sell", SeriesType.SCATTER, "$", Color.RED, ScatterMarkerSymbol.TRIANGLE_DOWN))
        stockPlot.add_series(Series("Liquidate", SeriesType.SCATTER, "$", Color.BLUE, ScatterMarkerSymbol.DIAMOND))

        self.add_chart(stockPlot)

    def on_data(self, data: Slice):
        if not self.BB.is_ready:
            return
        price = data[self.pair].price

        self.plot("Trade Plot", "Price", price)
        self.plot("Trade Plot", "MiddleBand", self.BB.middle_band.current.value)
        self.plot("Trade Plot", "UpperBand", self.BB.upper_band.current.value)
        self.plot("Trade Plot", "LowerBand", self.BB.lower_band.current.value)

        if not self.portfolio.invested:
            if self.BB.lower_band.current.value > price:
                self.set_holdings(self.pair, 1)
                self.plot("Trade Plot", "Buy", price)
            elif self.BB.upper_band.current.value < price:
                self.set_holdings(self.pair, -1)
                self.plot("Trade Plot", "Sell", price)
        else:
            if self.portfolio[self.pair].is_long:
                if self.BB.middle_band.current.value < price:
                    self.liquidate()
                    self.plot("Trade Plot", "Liquidate", price)
            elif self.BB.middle_band.current.value > price:
                self.liquidate()