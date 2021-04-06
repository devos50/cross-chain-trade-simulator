from enum import Enum
from typing import Set, Optional

from core import STELLAR_EXP
from core.assetamount import AssetAmount
from core.assetpair import AssetPair
from core.price_history import PriceHistory
from core.trader import Trader
from core.traders_manager import TradersManager


class TradeStatus(Enum):
    INITIALIZED = 0
    NO_TX_COMPLETED = 1
    ONE_TX_COMPLETED = 2
    COMPLETED = 3


class Trade:

    def __init__(self, trader_a: Trader, trader_b: Trader, assets: AssetPair, timestamp: str) -> None:
        self.trader_a: Trader = trader_a
        self.trader_b: Trader = trader_b
        self.assets: AssetPair = assets
        self.timestamp: str = timestamp
        self.witnesses_a: Set[Trader] = set()
        self.witnesses_b: Set[Trader] = set()

        self.tx_a_completed: bool = False
        self.tx_b_completed: bool = False
        self.status: TradeStatus = TradeStatus.INITIALIZED

        # Try to calculate/attach the trade value in USD, based on historical price data
        day = self.timestamp[:10]
        self.usd_price: Optional[float] = None
        first_asset_price = PriceHistory.get_price(self.assets.first.asset_id, day)
        second_asset_price = PriceHistory.get_price(self.assets.second.asset_id, day)
        if first_asset_price:
            self.usd_price = first_asset_price * (self.assets.first.amount / STELLAR_EXP)
        elif second_asset_price:
            self.usd_price = second_asset_price * (self.assets.second.amount / STELLAR_EXP)

    def execute(self) -> None:
        """
        Evaluate the trade and set the status, given the assigned witnesses.
        """

        # If there are not witnesses available, assume a trusted witness that mediates in the trade
        if not self.witnesses_a and not self.witnesses_b:
            self.status = TradeStatus.COMPLETED
            return

        # If both traders are colluding, the trade always completes
        if TradersManager.are_colluding(self.trader_a, self.trader_b):
            self.status = TradeStatus.COMPLETED
            return

        num_sig_tx_a = 0
        num_sig_tx_b = 0

        for witness in self.witnesses_a.union(self.witnesses_b):
            if not TradersManager.are_colluding(witness, self.trader_a) and not witness.offline:
                num_sig_tx_a += 1
            if not TradersManager.are_colluding(witness, self.trader_b) and not witness.offline:
                num_sig_tx_b += 1

        sigs_required = 1 # (len(self.witnesses_a) + len(self.witnesses_b)) // 2 + 1
        if num_sig_tx_a >= sigs_required and num_sig_tx_b >= sigs_required:
            self.status = TradeStatus.COMPLETED
        elif num_sig_tx_a < sigs_required or num_sig_tx_b < sigs_required:
            self.status = TradeStatus.ONE_TX_COMPLETED
        elif num_sig_tx_a < sigs_required and num_sig_tx_b < sigs_required:
            self.status = TradeStatus.NO_TX_COMPLETED

    @staticmethod
    def from_scenario_line(line: str) -> "Trade":
        parts = line.strip().split(",")

        address_trader_a = parts[5]
        address_trader_b = parts[6]
        if TradersManager.get_trader_by_address(address_trader_a):
            trader_a = TradersManager.get_trader_by_address(address_trader_a)
        else:
            trader_a = Trader(address_trader_a)
            TradersManager.add_trader(trader_a)

        if TradersManager.get_trader_by_address(address_trader_b):
            trader_b = TradersManager.get_trader_by_address(address_trader_b)
        else:
            trader_b = Trader(address_trader_b)
            TradersManager.add_trader(trader_b)

        amount1 = AssetAmount(int(float(parts[2]) * STELLAR_EXP), parts[1])
        amount2 = AssetAmount(int(float(parts[4]) * STELLAR_EXP), parts[3])
        pair = AssetPair(amount1, amount2) if amount1.asset_id < amount2.asset_id else AssetPair(amount2, amount1)
        trade = Trade(trader_a, trader_b, pair, parts[0])
        return trade
