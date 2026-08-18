"""Small domain layer for the shop BDD example."""


class Catalog:
    def __init__(self):
        self.items = {}

    def add(self, title, price, stock=0):
        self.items[title] = {"price": price, "stock": stock}

    def price(self, title):
        return self.items[title]["price"]

    def stock(self, title):
        return self.items[title]["stock"]


class Cart:
    def __init__(self, catalog):
        self.catalog = catalog
        self.items = []
        self.discount = 0

    def add(self, title):
        self.items.append(title)

    def total(self):
        return sum(self.catalog.price(item) for item in self.items)

    def apply_discount(self, percent):
        self.discount = percent

    def discounted_total(self):
        total = self.total()
        if self.discount:
            return round(total * (1 - self.discount / 100), 2)
        return total
