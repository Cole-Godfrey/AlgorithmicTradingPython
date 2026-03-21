# region imports
from AlgorithmImports import *


# endregion

class BuyHoldQQQ(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2016, 1, 1)
        self.set_end_date(2026, 1, 1)
        self.set_cash(100000)

        self.qqq = self.add_equity("QQQ", Resolution.HOUR).symbol

        self.entryTicket = None
        self.stopMarketTicket = None
        self.entryTime = datetime.min
        self.stopMarketFillTime = datetime.min
        self.highestPrice = 0

    def on_data(self, data: Slice):
        # wait 30 days after last exit
        if (self.time - self.stopMarketFillTime).days < 30:
            return

        price = self.securities[self.qqq].price

        # send entry limit order
        if not self.portfolio.invested and not self.transactions.get_open_orders(self.qqq):
            quantity = self.calculate_order_quantity(self.qqq, 0.9)
            self.entryTicket = self.limit_order(self.qqq, quantity, price, tag="Entry Order")
            self.entryTime = self.time

        # move limit price if not filled after 1 day
        if ((self.time - self.entryTime).days > 1 and self.entryTicket.status != OrderStatus.FILLED):
            self.entryTime = self.time
            updateFields = UpdateOrderFields()
            updateFields.limit_price = price
            self.entryTicket.update(updateFields)

        # move up trailing stop price
        if self.stopMarketTicket is not None and self.portfolio.invested:
            if price > self.highestPrice:
                self.highestPrice = price
                updateFields = UpdateOrderFields()
                updateFields.stop_price = price * 0.95
                self.stopMarketTicket.update(updateFields)
                # self.debug(updateFields.stop_price)

    def on_order_event(self, orderEvent):
        if orderEvent.status != OrderStatus.FILLED:
            return

        # send stop loss order if entry limit order is filled
        if self.entryTicket is not None and self.entryTicket.order_id == orderEvent.order_id:
            self.stopMarketTicket = self.stop_market_order(self.qqq, -self.entryTicket.quantity,
                                                           0.95 * self.entryTicket.average_fill_price)

        # save fill time of stop loss order
        if self.stopMarketTicket is not None and self.stopMarketTicket.order_id == orderEvent.order_id:
            self.stopMarketFillTime = self.time
            self.highestPrice = 0