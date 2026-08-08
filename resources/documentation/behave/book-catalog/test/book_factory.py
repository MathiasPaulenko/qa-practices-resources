# test/book_factory.py
from catalog_service import Catalog


class BookFactory:
    @staticmethod
    def seed(catalog, titles, available=True):
        for title in titles:
            catalog.add(title, available=available)
