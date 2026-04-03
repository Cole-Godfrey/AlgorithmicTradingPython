# region imports
from AlgorithmImports import *
# endregion

from alpha_model import FundamentalFactorAlphaModel


class PensiveBlackDogfish(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2016, 1, 1)
        self.set_end_date(2026, 1, 1)
        self.set_cash(100000)

        self.month = 0
        self.num_coarse = 500

        self.universe_settings.resolution = Resolution.DAILY
        self.add_universe(self.coarse_selection_function, self.fine_selection_function)

        self.add_alpha(FundamentalFactorAlphaModel())

        self.set_portfolio_construction(EqualWeightingPortfolioConstructionModel(self.is_rebalance_due))

        self.set_risk_management(NullRiskManagementModel())

        self.set_execution(ImmediateExecutionModel())

    def is_rebalance_due(self, time):
        if time.month == self.month or time.month not in [1, 4, 7, 10]:
            return None

        self.month = time.month
        return time

    def coarse_selection_function(self, coarse):
        if not self.is_rebalance_due(self.time):
            return Universe.UNCHANGED
        selected = sorted([x for x in coarse if x.has_fundamental_data and x.price > 5],
                          key=lambda x: x.dollar_volume, reverse=True)
        return [x.symbol for x in selected[:self.num_coarse]]

    def fine_selection_function(self, fine):
        sectors = [
            MorningstarSectorCode.FINANCIAL_SERVICES,
            MorningstarSectorCode.REAL_ESTATE,
            MorningstarSectorCode.HEALTHCARE,
            MorningstarSectorCode.UTILITIES,
            MorningstarSectorCode.TECHNOLOGY
        ]

        filtered_fine = [x.symbol for x in fine
                         if x.security_reference.ipo_date + timedelta(5 * 365) < self.time
                         and x.asset_classification.morningstar_sector_code in sectors
                         and x.operation_ratios.roe.value > 0
                         and x.operation_ratios.net_margin.value > 0
                         and x.valuation_ratios.pe_ratio > 0]
        return filtered_fine
    