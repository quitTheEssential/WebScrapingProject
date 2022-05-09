# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from tqdm import tqdm
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # Ignore FutureWarnings
pd.set_option('display.max_columns', None) # Display all columns

# Make sure to adjust gecko_path so that geckodriver is within a given subdirectory (set the path for geckodriver)
gecko_path = '/usr/local/bin/geckodriver'

ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)

# Base URL of the website that will be scraped
url = 'https://www.basketball-reference.com/players/'

############################
#####    SETTINGS    #######
############################
# Two boolean variables.
# Set `limit_to_100` to `True` to limit scraped pages to 100
limit_to_100 = True
# Set 'save_output_to_csv' to 'True' to save output to CSV file
save_output_to_csv = False
############################

# Counter that will count the number of already scraped websites
counter = 0

# Create an empty dataframe
d = pd.DataFrame({'nameAndSurname':[], 'games':[], 'points':[], 'totalRebounds':[],
                  'assists':[], 'fieldGoalPercentage':[], 'threeFieldGoal':[], 'freeThrowPercentage':[],
                  'effectiveFieldGoal':[],'playerEfficiency':[],'winShares':[]})

driver.get(url)

time.sleep(2)

# Get a link to each letter of the alphabet
alphabet = driver.find_element(By.XPATH, '//*[@id="div_alphabet"]/ul')
letters = alphabet.find_elements(By.XPATH, './/a[@href]')

# Save letters' links to list
letters_href_list = []
for _ in letters:
    letters_href_list.append(_.get_attribute('href'))

# Create an empty list that will store links to players' profiles
players_href_list = []
# Iterate through each letter (with progress bar)
for letter in tqdm(letters_href_list, desc='Getting list of players'):
    driver.get(letter)
    time.sleep(1)
    # Accessing players list for a given letter
    players_list = driver.find_element(By.XPATH, '//*[@id="players"]/tbody').find_elements(By.XPATH, './/tr/th//a[@href]')
    for _ in players_list[:20]: # By design, scrap first 20 players
        if limit_to_100: # Check if scraping should be stopped after 100 iterations
            if counter < 100: # Check if already scraped websites exceeds 100
                players_href_list.append(_.get_attribute('href'))
                counter += 1 # Track number of scraped websites
            else:
                print("Scraper reached the limit of 100 websites!")
                break
        else:
            players_href_list.append(_.get_attribute('href')) # If there is no limitation, go through each page
    else:
        continue
    break

# Iterate through each player scraped in the previous step (with progress bar)
for player_href in tqdm(players_href_list, desc='Getting info about players'):
    driver.get(player_href)
    time.sleep(1)

    # Get player Name
    try:
        nameAndSurname = driver.find_element(By.XPATH, '//h1/span').text
    except:
        nameAndSurname = ''

    # Get number of Games
    try:
        games = driver.find_element(By.XPATH, '//*[@data-tip="Games"]/following-sibling::p[2]').text
    except:
        games = ''

    # Get number of Points
    try:
        points = driver.find_element(By.XPATH, '//*[@data-tip="Points"]/following-sibling::p[2]').text
    except:
        points = ''

    # Get number of Total Rebounds
    try:
        totalRebounds = driver.find_element(By.XPATH, '//*[@data-tip="Total Rebounds"]/following-sibling::p[2]').text
    except:
        totalRebounds = ''

    # Get number of Assists
    try:
        assists = driver.find_element(By.XPATH, '//*[@data-tip="Assists"]/following-sibling::p[2]').text
    except:
        assists = ''

    # Get Field Goal Percentage
    try:
        fieldGoalPercentage = driver.find_element(By.XPATH, '//*[@data-tip="Field Goal Percentage"]/following-sibling::p[2]').text
    except:
        fieldGoalPercentage = ''

    # Get 3-Point Field Goal Percentage
    try:
        threeFieldGoal = driver.find_element(By.XPATH, '//*[@data-tip="3-Point Field Goal Percentage"]/following-sibling::p[2]').text
    except:
        threeFieldGoal = ''

    # Get Free Throw Percentage
    try:
        freeThrowPercentage = driver.find_element(By.XPATH, '//*[@data-tip="Free Throw Percentage"]/following-sibling::p[2]').text
    except:
        freeThrowPercentage = ''

    # Get Effective Field Goal Percentage
    try:
        effectiveFieldGoal = driver.find_element(By.XPATH, "//*[contains(@data-tip, 'Effective Field Goal Percentage')]/following-sibling::p[2]").text
    except:
        effectiveFieldGoal = ''

    # Get Player Efficiency Rating
    try:
        playerEfficiency = driver.find_element(By.XPATH, "//*[contains(@data-tip, 'Player Efficiency Rating')]/following-sibling::p[2]").text
    except:
        playerEfficiency = ''

    # Get Win Shares
    try:
        winShares = driver.find_element(By.XPATH, "//*[contains(@data-tip, 'Win Shares')]/following-sibling::p[2]").text
    except:
        winShares = ''

    # Combine player data into one dictionary
    baller = {'nameAndSurname': nameAndSurname, 'games': games, 'points': points, 'totalRebounds': totalRebounds,
              'assists': assists, 'fieldGoalPercentage': fieldGoalPercentage, 'threeFieldGoal': threeFieldGoal, 'freeThrowPercentage': freeThrowPercentage,
              'effectiveFieldGoal': effectiveFieldGoal, 'playerEfficiency': playerEfficiency, 'winShares': winShares}

    # Add player info to the final dataframe
    d = d.append(baller, ignore_index=True)

driver.quit()

# If scraper is restrained to 100 webpages and `save_output_to_csv` is set `True`, results are saved to 'ballers_small.csv' file
if limit_to_100 and save_output_to_csv:
    d.to_csv('ballers_small.csv', index=False)
# If scraper is not restrained to 100 webpages and `save_output_to_csv` is set `True`, results are saved to 'ballers_big.csv' file
elif save_output_to_csv:
    d.to_csv('ballers_big.csv', index=False)