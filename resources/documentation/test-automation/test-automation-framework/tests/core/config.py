# tests/core/config.py
import os


class Config:
    BASE_URL = os.getenv("TEST_BASE_URL", "https://staging.qa.local")
    HEADLESS = os.getenv("TEST_HEADLESS", "true").lower() == "true"
    BROWSER = os.getenv("TEST_BROWSER", "chromium")
