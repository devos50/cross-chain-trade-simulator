import networkx as nx

from core.price_history import PriceHistory
from core.scenario import Scenario

if __name__ == '__main__':
    PriceHistory.initialize("data/prices.csv")
    scenario = Scenario("data/trades_1000.csv")
    scenario.run()

    print(nx.number_connected_components(scenario.trade_graph.G))

    scenario.trade_graph.write_dot("data/graph.dot")
