from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import datetime

gecko_path = '/usr/local/bin/geckodriver'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)

url = 'https://www.basketball-reference.com/players/'

limit_to_100 = False
counter = 0

driver.get(url)

time.sleep(2)

alphabet = driver.find_element(By.XPATH, '//*[@id="div_alphabet"]/ul')
letters = alphabet.find_elements(By.XPATH, './/a[@href]')

letters_href_list = []
for _ in letters:
    letters_href_list.append(_.get_attribute('href'))

players_href_list = []
for letter in letters_href_list:
    driver.get(letter)
    time.sleep(1)
    players_list = driver.find_element(By.XPATH, '//*[@id="players"]/tbody').find_elements(By.XPATH, './/tr/th/a[@href]')
    for _ in players_list[:20]:
        if limit_to_100:
            if counter < 100:
                players_href_list.append(_.get_attribute('href'))
                counter += 1
            else:
                break
        else:
            players_href_list.append(_.get_attribute('href'))
    else:
        continue
    break

#print(len(players_href_list))

driver.quit()