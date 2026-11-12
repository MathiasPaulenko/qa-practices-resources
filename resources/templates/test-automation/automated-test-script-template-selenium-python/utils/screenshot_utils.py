import os
from datetime import datetime

class ScreenshotUtils:
    SCREENSHOT_DIR = "reports/screenshots"
    MAX_HEIGHT = 15000  # Chrome caps window height; taller pages need stitching

    @classmethod
    def capture(cls, driver, test_name, status="failure"):
        os.makedirs(cls.SCREENSHOT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{status}_{timestamp}.png"
        path = os.path.join(cls.SCREENSHOT_DIR, filename)
        driver.save_screenshot(path)
        return path

    @classmethod
    def capture_full_page(cls, driver, test_name):
        original_size = driver.get_window_size()
        total_height = driver.execute_script(
            "return document.body.parentNode.scrollHeight"
        )
        height = min(total_height, cls.MAX_HEIGHT)
        driver.set_window_size(original_size["width"], height)
        path = cls.capture(driver, test_name, "fullpage")
        driver.set_window_size(original_size["width"], original_size["height"])
        return path
