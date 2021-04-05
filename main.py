from core.price_history import PriceHistory
from core.scenario import Scenario

if __name__ == '__main__':
    PriceHistory.initialize("data/prices.csv")
    scenario = Scenario("data/trades_10000.csv")
    scenario.run()

    scenario.trade_graph.write_dot("data/graph.dot")
