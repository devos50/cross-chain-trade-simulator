import os
from typing import Optional


class PriceHistory:
    prices = {}

    @staticmethod
    def initialize(price_file_path: str) -> None:
        if not os.path.exists(price_file_path):
            print("Pricing information not available!")

        with open(price_file_path) as price_file:
            parsed_header = False
            for line in price_file.readlines():
                if not parsed_header:
                    parsed_header = True
                    continue

                parts = line.strip().split(",")
                asset = parts[0]
                if asset not in PriceHistory.prices:
                    PriceHistory.prices[asset] = {}

                PriceHistory.prices[asset][parts[1]] = float(parts[3])

    @staticmethod
    def get_price(asset: str, day: str) -> Optional[float]:
        if asset not in PriceHistory.prices:
            return None
        if day not in PriceHistory.prices[asset]:
            return None
        return PriceHistory.prices[asset][day]
