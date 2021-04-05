import os
import random

from core import WITNESSES_PER_PARTY
from core.graph import TradeGraph
from core.trade import Trade, TradeStatus
from core.traders_manager import TradersManager


class Scenario:

    def __init__(self, scenario_file_path: str):
        self.scenario_file_path = scenario_file_path
        self.trade_graph = TradeGraph()
        self.trades = []

    def run(self):
        if not os.path.exists(self.scenario_file_path):
            print("Scenario file %s does not exist!" % self.scenario_file_path)
            exit(1)

        processed_trades = 0
        malicious_trades = 0

        with open(self.scenario_file_path) as scenario_file:
            parsed_header = False
            for line in scenario_file.readlines():
                if not parsed_header:
                    parsed_header = True
                    continue

                trade = Trade.from_scenario_line(line)
                self.trades.append(trade)
                self.trade_graph.add_trade(trade)

        # Execute all trades
        for trade in self.trades:
            # Execute the trade - select witnesses
            trade.witnesses_a = TradersManager.get_random_witnesses(WITNESSES_PER_PARTY, excluded=[trade.trader_a, trade.trader_b])
            trade.witnesses_b = TradersManager.get_random_witnesses(WITNESSES_PER_PARTY, excluded=[trade.trader_a, trade.trader_b] + list(
                trade.witnesses_a))  # All witnesses must be unique
            trade.execute()

            processed_trades += 1
            if trade.status == TradeStatus.ONE_TX_COMPLETED:
                malicious_trades += 1

        print("Processed %d trades (trades where assets are stolen by one party: %d)" % (processed_trades, malicious_trades))
