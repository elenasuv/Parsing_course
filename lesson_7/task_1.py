from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
from pymongo import MongoClient
import time
chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://mail.ru/?from=logout&amp;ref=main")
assert 'Mail.ru' in driver.title

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172')

elem = driver.find_element_by_id('mailbox:submit')
elem.click()

elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)

time.sleep(5)
mails = set()
while len(mails) < 30:
    letters = driver.find_elements_by_xpath(
            "//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']")
    for letter in letters:
        letter_link = letter.get_attribute('href')
        mails.add(letter_link)
    time.sleep(5)
    actions = ActionChains(driver)
    actions.move_to_element(letters[-1])
    actions.perform()
    time.sleep(5)

print(mails)
print(len(mails))


mails_info = []
for mail in mails:
    driver.get(mail)
    mail_info_dict = {}
    title = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//h2[@class='thread__subject thread__subject_pony-mode']"))
).text
    sender = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='letter__author']/span"))
).text
    time = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='letter__date']"))
).text
    text = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='letter-body__body']"))
).text
    mail_info_dict['link'] = mail
    mail_info_dict['title'] = title
    mail_info_dict['sender'] = sender
    mail_info_dict['time'] = time
    mail_info_dict['text'] = text
    mails_info.append(mail_info_dict)



client = MongoClient('localhost', 27017)
db = client['maildata']
mailru = db.mailru
for i in mails_info:
    mailru.update_one({'link': i['link']}, {'$set': i}, upsert = True)

for mail in mailru.find({}):
    pprint(mail)

driver.quit()
