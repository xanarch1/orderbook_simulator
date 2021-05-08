import unittest
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orderbook import next_id
from market import Market
from trader import Trader

TRADER_ID = next_id()
ORDER_ID = next_id()
PRICE = 100


class TestMarket(unittest.TestCase):
    def test_can_create_initial_state(self):
        trader_1 = Trader(TRADER_ID, 400)
        market = Market([trader_1])
        orders = []
        for i in range(5):
            orders.append(trader_1.create_order(ORDER_ID, 300 + i, "LIMIT", 100))
        market.construct_initial_state(orders)
        self.assertEqual(len(market.orderbook.bids), len(orders))
        self.assertEqual(len(market.orderbook.asks), 0)

    def test_submit_order_no_liquidity_market(self):
        trader_1 = Trader(TRADER_ID, 400)
        market = Market([trader_1])
        order = trader_1.create_order(ORDER_ID, None, "MARKET", 100)
        self.assertRaises(Exception, market.submit_order, trader_1, order)

    def test_submit_order_no_liquidity_limit(self):
        trader_1 = Trader(TRADER_ID, 400)
        market = Market([trader_1])
        order = trader_1.create_order(ORDER_ID, 300, "LIMIT", 100)
        market.submit_order(trader_1, order)
        self.assertEqual(market.orderbook.bids, [order])

    def test_submit_order_not_market_maker(self):
        trader_1 = Trader(TRADER_ID, 400)
        market = Market([trader_1])
        order = trader_1.create_order(ORDER_ID, 300, "LIMIT", 100)
        market.submit_order(trader_1, order)
        self.assertEqual(market.orderbook.bids, [order])
        order_2 = trader_1.create_order(ORDER_ID, 305, "LIMIT", 100)
        market.submit_order(trader_1, order_2)
        self.assertEqual(market.orderbook.bids, [order_2])
        self.assertEqual(order.order_state, "CANCELLED")

    def test_submit_order_market_maker(self):
        pass

    def test_shuffle_and_call_tick_on_run(self):
        pass
