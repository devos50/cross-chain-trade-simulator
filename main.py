import networkx as nx

from core.scenario import Scenario

if __name__ == '__main__':
    scenario = Scenario("data/trades_1000.csv")
    scenario.run()

    print(nx.number_connected_components(scenario.trade_graph.G))

    scenario.trade_graph.write_dot("data/graph.dot")
