# Requires: pip install Appium-Python-Client==4.2.0
from appium import webdriver
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = 'Android'
options.automation_name = 'UiAutomator2'
options.device_name = 'Pixel_7_API_34'
options.app = '/path/to/app.apk'  # placeholder: path to your build artifact

driver = webdriver.Remote('http://localhost:4723', options=options)
driver.find_element(by='accessibility id', value='login-button').click()
assert driver.find_element(by='accessibility id', value='dashboard-welcome').is_displayed()
driver.quit()
