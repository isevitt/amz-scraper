from selenium import webdriver
import os

CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")
options = webdriver.ChromeOptions()
options.binary_location = chrome_bin
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument('headless')
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)

driver.get("https://www.google.com")
print(driver.page_source)
