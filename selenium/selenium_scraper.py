from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from tqdm import tqdm
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.set_option('display.max_columns', None)

gecko_path = '/usr/local/bin/geckodriver'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)

url = 'https://www.basketball-reference.com/players/'

limit_to_100 = True
save_output_to_csv = False

counter = 0

d = pd.DataFrame({'nameAndSurname':[],
                  # 'position':[], 'shoots':[], 'height':[], 'weight':[], 'birthYear':[], <---- removed columns
                  'games':[], 'points':[], 'totalRebounds':[], 'assists':[], 'fieldGoalPercentage':[],
                  'threeFieldGoal':[], 'freeThrowPercentage':[],'effectiveFieldGoal':[],'playerEfficiency':[],'winShares':[]})

driver.get(url)

time.sleep(2)

alphabet = driver.find_element(By.XPATH, '//*[@id="div_alphabet"]/ul')
letters = alphabet.find_elements(By.XPATH, './/a[@href]')

letters_href_list = []
for _ in letters:
    letters_href_list.append(_.get_attribute('href'))

players_href_list = []
for letter in tqdm(letters_href_list, desc='Letters'):
    driver.get(letter)
    time.sleep(1)
    players_list = driver.find_element(By.XPATH, '//*[@id="players"]/tbody').find_elements(By.XPATH, './/tr/th/a[@href]')
    for _ in players_list[:20]:
        if limit_to_100:
            if counter < 100:
                players_href_list.append(_.get_attribute('href'))
                counter += 1
            else:
                print("Scraper reached the limit of 100 websites!")
                break
        else:
            players_href_list.append(_.get_attribute('href'))
    else:
        continue
    break

for player_href in tqdm(players_href_list, desc='Players'):
    driver.get(player_href)
    time.sleep(1)

    try:
        nameAndSurname = driver.find_element(By.XPATH, '//*[@itemprop="name"]/span').text
    except:
        nameAndSurname = ''

    #try:
    #position = driver.find_elements(By.XPATH, "//*[contains(.,'Position')]/following-sibling::node()[1]")
    #print(position)
    #except:
        #position = ''

    #try:
    #shoots = driver.find_elements(By.XPATH, "//*[contains(.,'Position')]/following-sibling::node()[2]")
    #print(shoots)
    #except:
        #shoots = ''

    #height =
    #weight =
    #birthYear =

    try:
        games = driver.find_element(By.XPATH, '//*[@data-tip="Games"]/following-sibling::p[2]').text
    except:
        games = ''

    try:
        points = driver.find_element(By.XPATH, '//*[@data-tip="Points"]/following-sibling::p[2]').text
    except:
        points = ''

    try:
        totalRebounds = driver.find_element(By.XPATH, '//*[@data-tip="Total Rebounds"]/following-sibling::p[2]').text
    except:
        totalRebounds = ''

    try:
        assists = driver.find_element(By.XPATH, '//*[@data-tip="Assists"]/following-sibling::p[2]').text
    except:
        assists = ''

    try:
        fieldGoalPercentage = driver.find_element(By.XPATH, '//*[@data-tip="Field Goal Percentage"]/following-sibling::p[2]').text
    except:
        fieldGoalPercentage = ''

    try:
        threeFieldGoal = driver.find_element(By.XPATH, '//*[@data-tip="3-Point Field Goal Percentage"]/following-sibling::p[2]').text
    except:
        threeFieldGoal = ''

    try:
        freeThrowPercentage = driver.find_element(By.XPATH, '//*[@data-tip="Free Throw Percentage"]/following-sibling::p[2]').text
    except:
        freeThrowPercentage = ''

    try:
        effectiveFieldGoal = driver.find_element(By.XPATH, "//*[contains(@data-tip, 'Effective Field Goal Percentage')]/following-sibling::p[2]").text
    except:
        effectiveFieldGoal = ''

    try:
        playerEfficiency = driver.find_element(By.XPATH, "//*[contains(@data-tip, 'Player Efficiency Rating')]/following-sibling::p[2]").text
    except:
        playerEfficiency = ''

    try:
        winShares = driver.find_element(By.XPATH, "//*[contains(@data-tip, 'Win Shares')]/following-sibling::p[2]").text
    except:
        winShares = ''

    baller = {'nameAndSurname': nameAndSurname,
              # 'position': position, 'shoots': shoots, 'height': height, 'weight': weight, 'birthYear': birthYear, <---- removed columns
              'games': games, 'points': points, 'totalRebounds': totalRebounds, 'assists': assists, 'fieldGoalPercentage': fieldGoalPercentage,
              'threeFieldGoal': threeFieldGoal, 'freeThrowPercentage': freeThrowPercentage,
              'effectiveFieldGoal': effectiveFieldGoal, 'playerEfficiency': playerEfficiency, 'winShares': winShares}

    d = d.append(baller, ignore_index=True)

driver.quit()

if limit_to_100 and save_output_to_csv:
    d.to_csv('ballers_small.csv', index=False)
elif save_output_to_csv:
    d.to_csv('ballers_big.csv', index=False)