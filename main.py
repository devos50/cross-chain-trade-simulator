import random

from core.price_history import PriceHistory
from core.scenario import Scenario

if __name__ == '__main__':
    random.seed(44)

    PriceHistory.initialize("data/prices.csv")
    scenario = Scenario("data/trades_1000.csv")
    scenario.run()

    #scenario.trade_graph.write_dot("data/graph.dot")
