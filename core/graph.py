import networkx as nx
from networkx.drawing.nx_agraph import write_dot

from core.trade import Trade


class TradeGraph:

    def __init__(self) -> None:
        self.G = nx.Graph()

    def add_trade(self, trade: Trade) -> None:
        self.G.add_node(trade.trader_a.address)
        self.G.add_node(trade.trader_b.address)
        self.G.add_edge(trade.trader_a.address, trade.trader_b.address, trade=trade, capacity=1)

    def write_dot(self, output_file_path: str):
        write_dot(self.G, output_file_path)
