from selenium import webdriver
import os
from google_sheet_helper import get_google_sheets_client, add_asin_to_sheet, get_sheet
local = os.environ.get("LOCAL", False)
from datetime import datetime


SELLER_BASE_URL = "https://www.amazon.com/s?i=merchant-items&me="
PROD_BASE_URL = "https://www.amazon.com/dp/"
CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument('window-size=1200x600')

if not local:
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")
    options.binary_location = chrome_bin
    options.add_argument('headless')



def get_product_list(merchant_id, pages_num, driver):
    all_asins = []
    pages_num = int(pages_num)
    for page in range(1, pages_num + 1):
        driver.get(f"{SELLER_BASE_URL}{merchant_id}&page={page}")
        product_list = driver.find_elements_by_xpath("//*[@class='a-link-normal a-text-normal']")
        page_asins = [i.get_attribute("href").split("/dp/")[1].split("/")[0] for i in product_list]
        all_asins += page_asins
    return all_asins


def get_product_details(asin, driver):
    driver.get(f"{PROD_BASE_URL}{asin}")
    title = driver.find_element_by_id("productTitle").text
    try:
        price = driver.find_element_by_id("price").text
    except:
        price = ' '
    try:
        count_reviews = driver.find_element_by_id("acrCustomerReviewText").text
    except:
        count_reviews = ' '
    try:
        amz_choice = driver.find_element_by_class_name("ac-badge-rectangle").text
    except:
        amz_choice = ' '


    return [asin, title, price, count_reviews, amz_choice]


def run(merchant_id, num_pages):
    try:
        print("starting proccess")
        gs_client = get_google_sheets_client()
        sheet = get_sheet(gs_client)
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_PATH", CHROMEDRIVER_PATH), chrome_options=options)
        print("created google sheets and selenium clients")
        print("getting product list")
        asins_list = get_product_list(merchant_id, num_pages, driver)
        print(f"found {len(asins_list)} asins")
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        add_asin_to_sheet(sheet, ["time:" +  now])
        for asin in asins_list:
            asin_data = get_product_details(asin, driver)
            add_asin_to_sheet(sheet, asin_data)

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        add_asin_to_sheet(sheet, ["Finished. Time: " + now])
    except Exception as e:
        add_asin_to_sheet(sheet, ["Error " + str(e)])
        print(e)
    finally:
        driver.close()





