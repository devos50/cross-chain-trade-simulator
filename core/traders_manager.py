import random
from typing import Dict, List, Set, Optional

from core import Trader


class TradersManager:
    traders: List[Trader] = []
    traders_map: Dict[str, Trader] = {}
    collusions: Dict[Trader, List[Trader]] = {}

    @staticmethod
    def get_random_witnesses(amount: int, excluded: list = []) -> Set:
        reduced_list = TradersManager.traders.copy()
        for trader in excluded:
            if trader in reduced_list:
                reduced_list.remove(trader)

        if len(reduced_list) < amount:
            return set()

        return set(random.sample(reduced_list, amount))

    @staticmethod
    def add_trader(trader: Trader) -> None:
        if trader.address not in TradersManager.traders_map:
            TradersManager.traders.append(trader)
            TradersManager.traders_map[trader.address] = trader

    @staticmethod
    def get_trader_by_address(address: str) -> Optional[Trader]:
        if address in TradersManager.traders_map:
            return TradersManager.traders_map[address]
        return None

    @staticmethod
    def add_collusion(trader_a: Trader, trader_b: Trader):
        if trader_a not in TradersManager.collusions:
            TradersManager.collusions[trader_a] = []
        TradersManager.collusions[trader_a].append(trader_b)

        # Collusion is bilateral
        if trader_b not in TradersManager.collusions:
            TradersManager.collusions[trader_b] = []
        TradersManager.collusions[trader_b].append(trader_a)

    @staticmethod
    def are_colluding(trader_a: Trader, trader_b: Trader):
        if trader_a not in TradersManager.collusions:
            return False
        return trader_b in TradersManager.collusions[trader_a]
