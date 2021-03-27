import networkx as nx
from networkx.drawing.nx_agraph import write_dot

from core.trade import Trade


class TradeGraph:

    def __init__(self) -> None:
        self.G = nx.Graph()

    def add_trade(self, trade: Trade) -> None:
        self.G.add_node(trade.trader_a.address)
        self.G.add_node(trade.trader_b.address)
        if self.G.has_edge(trade.trader_a.address, trade.trader_b.address):
            self.G[trade.trader_a.address][trade.trader_b.address]["weight"] += trade.usd_price or 0
        else:
            self.G.add_edge(trade.trader_a.address, trade.trader_b.address, trade=trade, weight=trade.usd_price or 0)

    def write_dot(self, output_file_path: str) -> None:
        write_dot(self.G, output_file_path)
