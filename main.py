from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

GOOGLE_DOC_URL = GOOGLE_DOC_URL
ZILLOW = ZILLOW_URL

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

response = requests.get(ZILLOW, headers=req_headers)
web_page = response.content

soup = BeautifulSoup(web_page, "html.parser")
links_list = soup.find_all(name="a", class_="list-card-img")
links = [link["href"] if 'http' in link["href"] else f'https://www.zillow.com{link["href"]}' for link in links_list]
address_list = soup.find_all(class_="list-card-addr")
addresses = [address.getText().split("|")[0] for address in address_list]
prices = soup.find_all(class_="list-card-price")
price = [price.getText().replace("/mo", "").split("+")[0] for price in prices]


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(GOOGLE_DOC_URL)
for i in range(len(links) - 1):
    time.sleep(2)
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(addresses[i])
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(price[i])
    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(links[i])
    submit_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_btn.click()
    new_submit = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')))
    new_submit.click()

driver.quit()