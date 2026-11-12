import json
import yaml
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class TestDataLoader:
    _data = None
    _credentials = None

    @classmethod
    def load(cls):
        if cls._data is None:
            with open(DATA_DIR / "test_data.json", "r") as f:
                cls._data = json.load(f)
        return cls._data

    @classmethod
    def get_user(cls, user_type):
        return cls.load()["users"][user_type]

    @classmethod
    def get_product(cls, product_key):
        return cls.load()["products"][product_key]

    @classmethod
    def get_checkout_data(cls):
        return cls.load()["checkout"]

    @classmethod
    def get_url(cls, url_key):
        return cls.load()["urls"][url_key]

    @classmethod
    def get_password(cls, user_type):
        if cls._credentials is None:
            with open(DATA_DIR / "credentials.yaml", "r") as f:
                cls._credentials = yaml.safe_load(f)
        return cls._credentials[user_type]
