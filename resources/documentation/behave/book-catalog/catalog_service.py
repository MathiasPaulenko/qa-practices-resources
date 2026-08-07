# catalog_service.py
from typing import List


class Book:
    def __init__(self, title: str, available: bool = True):
        self.title = title
        self.available = available


class Catalog:
    def __init__(self):
        self.books: List[Book] = []

    def add(self, title: str, available: bool = True) -> Book:
        book = Book(title, available)
        self.books.append(book)
        return book

    def search(self, title: str) -> List[Book]:
        return [b for b in self.books if b.title == title]
