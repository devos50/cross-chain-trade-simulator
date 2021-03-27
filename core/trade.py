from core import STELLAR_EXP
from core.assetamount import AssetAmount
from core.assetpair import AssetPair
from core.price_history import PriceHistory
from core.trader import Trader


class Trade:

    def __init__(self, trader_a: Trader, trader_b: Trader, assets: AssetPair, timestamp: str) -> None:
        self.trader_a = trader_a
        self.trader_b = trader_b
        self.assets = assets
        self.timestamp = timestamp

        # Try to calculate/attach the trade value in USD, based on historical price data
        day = self.timestamp[:10]
        self.usd_price = None
        first_asset_price = PriceHistory.get_price(self.assets.first.asset_id, day)
        second_asset_price = PriceHistory.get_price(self.assets.second.asset_id, day)
        if first_asset_price:
            self.usd_price = first_asset_price * (self.assets.first.amount / STELLAR_EXP)
        elif second_asset_price:
            self.usd_price = second_asset_price * (self.assets.second.amount / STELLAR_EXP)

    @staticmethod
    def from_scenario_line(line: str):
        parts = line.strip().split(",")
        trader_a = Trader(parts[5])
        trader_b = Trader(parts[6])
        amount1 = AssetAmount(int(float(parts[2]) * STELLAR_EXP), parts[1])
        amount2 = AssetAmount(int(float(parts[4]) * STELLAR_EXP), parts[3])
        pair = AssetPair(amount1, amount2) if amount1.asset_id < amount2.asset_id else AssetPair(amount2, amount1)
        trade = Trade(trader_a, trader_b, pair, parts[0])
        return trade
