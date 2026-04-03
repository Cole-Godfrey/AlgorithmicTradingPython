# region imports
from AlgorithmImports import *


# endregion

class FundamentalFactorAlphaModel(AlphaModel):
    def __init__(self):
        self.rebalance_time = datetime.min
        self.sectors = {}  # {technology: set(AAPL, TSLA, ...), healthcare: set(ABC, XYZ, ...)}

    def update(self, algorithm, data):
        if algorithm.time <= self.rebalance_time:
            return []
        self.rebalance_time = Expiry.END_OF_QUARTER(algorithm.time)

        insights = []

        for sector in self.sectors:
            securities = self.sectors[sector]
            sorted_by_roe = sorted(securities,
                                   key=lambda x: x.fundamentals.operation_ratios.roe.value, reverse=True)
            sorted_by_pm = sorted(securities,
                                  key=lambda x: x.fundamentals.operation_ratios.net_margin.value, reverse=True)
            sorted_by_pe = sorted(securities,
                                  key=lambda x: x.fundamentals.valuation_ratios.pe_ratio, reverse=False)

            scores = {}
            for security in securities:
                score = sum([sorted_by_roe.index(security), sorted_by_pm.index(security), sorted_by_pe.index(security)])
                scores[security] = score
            length = max(int(len(scores) / 5), 1)
            for security in sorted(scores.items(), key=lambda x: x[1], reverse=False)[:length]:
                symbol = security[0].symbol
                insights.append(Insight.price(symbol, Expiry.END_OF_QUARTER, InsightDirection.UP))

        return insights

    def on_securities_changed(self, algorithm, changes):
        for security in changes.removed_securities:
            for sector in self.sectors:
                if security in self.sectors[sector]:
                    self.sectors[sector].remove(security)

        for security in changes.added_securities:
            sector = security.fundamentals.asset_classification.morningstar_sector_code
            if sector not in self.sectors:
                self.sectors[sector] = set()
            self.sectors[sector].add(security)

