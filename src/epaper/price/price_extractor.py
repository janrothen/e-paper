import math


class PriceExtractor:
    def __init__(self, currency: str, symbol: str) -> None:
        self.currency = currency
        self.symbol = symbol

    def formatted_price_from_data(self, data: dict | None) -> str:
        if not data:
            return "N/A"
        currency_data = data.get(self.currency)
        if not currency_data:
            return "N/A"
        price = currency_data.get("last")
        if price is None:
            return "N/A"
        return self.format_price(price)

    def format_price(self, price: float) -> str:
        price_without_cents = self.price_without_cents(price)
        if price_without_cents >= 100_000:
            value = price_without_cents / 1_000_000
            truncated = int(value * 1000) / 1000  # truncate to 3 decimal places, no rounding
            formatted = f"{truncated:.3f}".rstrip("0").rstrip(".")
            return f'{self.symbol}{formatted.lstrip("0")}M'
        elif price_without_cents >= 1_000:
            value = price_without_cents / 1_000
            truncated = int(value * 100) / 100  # truncate to 2 decimal places, no rounding
            formatted = f"{truncated:.2f}".rstrip("0").rstrip(".")
            return f"{self.symbol}{formatted}k"
        else:
            return f"{self.symbol}{int(price_without_cents)}"

    def price_without_cents(self, price: float) -> float:
        return float(math.floor(price))
