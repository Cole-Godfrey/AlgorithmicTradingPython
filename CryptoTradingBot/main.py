# region imports
from AlgorithmImports import *


# endregion

class CalmRedPig(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2016, 1, 1)
        self.set_end_date(2026, 1, 1)
        self.set_cash(100000)

        self.settings.free_portfolio_value_percentage = 0.05
        self.position_size_USD = 5000
        self.rsi_entry_threshold = 70
        self.rsi_exit_threshold = 60
        self.minimum_volume = 1000000

        universe = ['BTCUSD', 'LTCUSD', 'ETHUSD', 'ETCUSD', 'RRTUSD', 'ZECUSD', 'XMRUSD', 'XRPUSD', 'EOSUSD', 'SANUSD',
                    'OMGUSD', 'NEOUSD', 'ETPUSD', 'BTGUSD', 'SNTUSD', 'BATUSD', 'FUNUSD', 'ZRXUSD', 'TRXUSD', 'REQUSD',
                    'LRCUSD', 'WAXUSD', 'DAIUSD', 'BFTUSD', 'ODEUSD', 'ANTUSD', 'XLMUSD', 'XVGUSD', 'MKRUSD', 'KNCUSD',
                    'LYMUSD', 'UTKUSD', 'VEEUSD', 'ESSUSD', 'IQXUSD', 'ZILUSD', 'BNTUSD', 'XRAUSD', 'VETUSD', 'GOTUSD',
                    'XTZUSD', 'MLNUSD', 'PNKUSD', 'DGBUSD', 'BSVUSD', 'ENJUSD', 'PAXUSD']
        self.pairs = [Pair(self, ticker, self.minimum_volume) for ticker in universe]
        self.set_benchmark("BTCUSD")
        self.set_warm_up(30)

    def on_data(self, data: Slice):
        for pair in self.pairs:
            if not pair.RSI.is_ready:
                return

            symbol = pair.symbol
            rsi = pair.RSI.current.value

            if self.portfolio[symbol].invested:
                if not pair.investable():
                    self.liquidate(symbol, "Not enough volume.")
                elif rsi < self.rsi_exit_threshold:
                    self.liquidate(symbol, "RSI below threshold.")
                continue

            if not pair.investable():
                continue

            if rsi > self.rsi_entry_threshold and self.portfolio.margin_remaining > self.position_size_USD:
                self.buy(symbol, self.position_size_USD / self.securities[symbol].price)


class Pair:
    def __init__(self, algorithm, ticker, minimum_volume):
        self.symbol = algorithm.add_crypto(ticker, Resolution.DAILY,
                                           Market.BITFINEX).symbol
        self.RSI = algorithm.rsi(self.symbol, 14, MovingAverageType.SIMPLE, Resolution.DAILY)
        self.volume = IndicatorExtensions.times(algorithm.sma(self.symbol, 30, Resolution.DAILY, Field.VOLUME),
                                                algorithm.sma(self.symbol, 30, Resolution.DAILY, Field.CLOSE))
        self.minimum_volume = minimum_volume

    def investable(self):
        return (self.volume.current.value > self.minimum_volume)