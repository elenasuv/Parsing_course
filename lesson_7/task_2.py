from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import json
import time
from pprint import pprint

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')

assert 'М.Видео' in driver.title

hits_block = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@data-init='ajax-category-carousel'][2]"))
)
pages = 0
time.sleep(5)
while True:
    button = WebDriverWait(hits_block, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sel-hits-button-next"))
                )
    pages += 1
    print(f'Всего страниц = {pages}')
    if button.get_attribute('class') == "next-btn sel-hits-button-next disabled":
        break
    button.click()
    time.sleep(5)
time.sleep(5)

products = WebDriverWait(hits_block, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, ".//a[@class='sel-product-tile-title']"))
)
hits_info = []
for product in products:
    product_info_js = product.get_attribute("data-product-info").replace('\n\t\t\t\t\t', '')
    product_info = json.loads(product_info_js)
    hits_info.append(product_info)

client = MongoClient('localhost', 27017)
db = client['mvideodata']
hits = db.hits
for i in hits_info:
    hits.update_one({'productId': i['productId']}, {'$set': i}, upsert = True)

for hit in hits.find({}):
    pprint(hit)


driver.quit()




