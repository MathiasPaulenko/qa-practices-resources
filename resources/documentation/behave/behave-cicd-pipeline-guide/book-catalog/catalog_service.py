class Catalog:
    def __init__(self):
        self.books = []

    def add(self, title: str):
        self.books.append(title)

    def search(self, title: str):
        return [book for book in self.books if title.lower() in book.lower()]
