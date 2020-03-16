from selenium import webdriver
import os
from configs import local
from google_sheet_helper import get_google_sheets_client, add_asin_to_sheet, get_sheet
from dbhelper import DBHelper
DB = DBHelper()

SELLER_BASE_URL = "https://www.amazon.com/s?i=merchant-items&me="
PROD_BASE_URL = "https://www.amazon.com/dp/"
NUM_PAGES = 1
CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument('window-size=1200x600')

if not local:
    chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")
    options.binary_location = chrome_bin
    options.add_argument('headless')

def get_merchants_from_db():
    DB.connect()
    return DB.get_all_unfinished()




def get_product_list(merchant_id, pages_num):
    all_asins = []
    for page in range(1, pages_num + 1):
        driver.get(f"{SELLER_BASE_URL}{merchant_id}&page={page}")
        product_list = driver.find_elements_by_xpath("//*[@class='a-link-normal a-text-normal']")
        page_asins = [i.get_attribute("href").split("/dp/")[1].split("/")[0] for i in product_list]
        all_asins += page_asins
    return all_asins


def get_product_details(asin):
    driver.get(f"{PROD_BASE_URL}{asin}")
    title = driver.find_element_by_id("productTitle").text
    return [asin, title]


if __name__ == "__main__":
    query_result = get_merchants_from_db()
    gs_client = get_google_sheets_client()
    sheet = get_sheet(gs_client)

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_PATH", CHROMEDRIVER_PATH), chrome_options=options)
    for row in query_result:
        try:
            asins_list = get_product_list(row[1], NUM_PAGES)
            for asin in asins_list:
                asin_data = get_product_details(asin)
                add_asin_to_sheet(sheet, asin_data)
        except Exception as e:
            print(e)
            # TODO: add logging



