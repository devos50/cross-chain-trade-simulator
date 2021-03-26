from core.assetamount import AssetAmount
from core.assetpair import AssetPair
from core.trader import Trader


class Trade:

    def __init__(self, trader_a: Trader, trader_b: Trader, assets: AssetPair) -> None:
        self.trader_a = trader_a
        self.trader_b = trader_b
        self.assets = assets

    @staticmethod
    def from_scenario_line(line: str):
        parts = line.strip().split(",")
        trader_a = Trader(parts[5])
        trader_b = Trader(parts[6])
        amount1 = AssetAmount(1, parts[1])  # TODO hardcoded amount
        amount2 = AssetAmount(1, parts[3])  # TODO hardcoded amount
        pair = AssetPair(amount1, amount2) if amount1.asset_id < amount2.asset_id else AssetPair(amount2, amount1)
        trade = Trade(trader_a, trader_b, pair)
        return trade
