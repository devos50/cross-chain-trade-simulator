import os

from core.graph import TradeGraph
from core.trade import Trade


class Scenario:

    def __init__(self, scenario_file_path: str):
        self.scenario_file_path = scenario_file_path
        self.trade_graph = TradeGraph()

    def run(self):
        if not os.path.exists(self.scenario_file_path):
            print("Scenario file %s does not exist!" % self.scenario_file_path)
            exit(1)

        with open(self.scenario_file_path) as scenario_file:
            parsed_header = False
            for line in scenario_file.readlines():
                if not parsed_header:
                    parsed_header = True
                    continue

                trade = Trade.from_scenario_line(line)
                self.trade_graph.add_trade(trade)
