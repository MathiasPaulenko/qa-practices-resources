class InventoryService:
    def __init__(self):
        self._stock = {}

    def set_stock(self, sku: str, qty: int) -> None:
        self._stock[sku] = qty

    def get_stock(self, sku: str) -> int:
        return self._stock.get(sku, 0)

    def increase(self, sku: str, qty: int) -> None:
        self._stock[sku] = self._stock.get(sku, 0) + qty

    def decrease(self, sku: str, qty: int) -> None:
        if sku not in self._stock:
            raise ValueError(f"Unknown SKU: {sku}")
        if qty > self._stock[sku]:
            raise ValueError(f"Insufficient stock for {sku}: {self._stock[sku]} < {qty}")
        self._stock[sku] -= qty
