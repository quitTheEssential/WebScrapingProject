# Import necessary libraries
from urllib import request
from bs4 import BeautifulSoup as BS
from bs4 import Comment
import re
from tqdm import tqdm
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # Ignore FutureWarnings
pd.set_option('display.max_columns', None) # Display all columns

# Base URL of the website that will be scraped
url = 'https://www.basketball-reference.com/players/'

# Get information of the above url
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

############################
#####    SETTINGS    #######
############################
# Two boolean variables.
# Set `limit_to_100` to `True` to limit scraped pages to 100
limit_to_100 = True
# Set 'save_output_to_csv' to 'True' to save output to CSV file
save_output_to_csv = False
############################

# Variable to control number of pages
counter = 0

# Create an empty dataframe
d = pd.DataFrame({'nameAndSurname':[],'games':[], 'points':[],'totalRebounds':[],'assists':[],'fieldGoalPercentage':[],
                  'threeFieldGoal':[],'freeThrowPercentage':[],'effectiveFieldGoal':[],'playerEfficiency':[],'winShares':[]})

# Get a link to each letter of the alphabet
alphabet = bs.find('div',{'id':'all_alphabet'}).find(text=lambda text: isinstance(text, Comment))\
    .findAllNext('a', {'href':re.compile('\/players\/[a-z]+\/$')})

# List comprehension to create concatenated links
letters_href_list = ['https://www.basketball-reference.com' + text['href'] for text in alphabet]

# Create an empty list that will store links to players' profiles
players_href_list = []

# Iterate through each letter (with progress bar)
for letter in tqdm(letters_href_list, desc='Getting list of players'):
    if counter == 100:  # Check if scraper achieve 100 pages
        break
    html = request.urlopen(letter)  # Open precise page
    bs = BS(html.read(), 'html.parser')  # Get the information about HTML of given page
    players_list = bs.find('table',{'id':'players'}).find('tbody').find_all('a',{'href':re.compile('\/players\/[a-z]+\/')})  # Find a link to player
    for link in players_list[:20]: # By design, scrap first 20 players
        if limit_to_100:  # Check if scraping should be stopped after 100 iterations
            if counter < 100:  # Check if already scraped websites exceeds 100
                players_href_list.append('https://www.basketball-reference.com' + link['href'])
                counter += 1  # Track number of scraped websites
            else:
                print("Scraper reached the limit of 100 websites!")
                break
        else:
            players_href_list.append('https://www.basketball-reference.com' + link['href'])  # If there is no limitation, go through each page


# Iterate through each player scraped in the previous step (with progress bar)
for player in tqdm(players_href_list, desc='Getting info about players'):
    html = request.urlopen(player)
    bs = BS(html.read(), 'html.parser')

    # Get Name and Surname of the player
    if len(bs.find('div',{'id':'meta'}).find_all('div')) > 1 :  # Check if player profile includes a photo
        try:
            nameAndSurname = bs.find('div',{'id':'meta'}).find_all('div')[1].h1.span.text
        except:
            nameAndSurname = ''
    else:
        try:
            nameAndSurname = bs.find('div',{'id':'meta'}).find_all('div')[0].h1.span.text
        except:
            nameAndSurname = ''

    # Get number of played Games
    try:
        games = bs.find('div',{'id':'info'}).find('div',{'class':'p1'}).find_all('div')[0].find_all('p')[1].text
    except:
        games = ''

    # Get a number of Points per match
    try:
        points = bs.find('div',{'id':'info'}).find('div',{'class':'p1'}).find_all('div')[1].find_all('p')[1].text
    except:
        points = ''

    # Get a number of Rebounds per match
    try:
        totalRebounds = bs.find('div',{'id':'info'}).find('div',{'class':'p1'}).find_all('div')[2].find_all('p')[1].text
    except:
        totalRebounds = ''

    # Get a number of Assists per match
    try:
        assists = bs.find('div',{'id':'info'}).find('div',{'class':'p1'}).find_all('div')[3].find_all('p')[1].text
    except:
        assists = ''

    if len(bs.find('div',{'id':'info'}).find('div',{'class':'p2'}).find_all('div')) > 2:  # Check if in the table exist two or four columns
        # Get Field Goal Percentage
        try:
            fieldGoalPercentage = \
            bs.find('div', {'id': 'info'}).find('div', {'class': 'p2'}).find_all('div')[0].find_all('p')[1].text
        except:
            fieldGoalPercentage = ''

        # Get 3-Point Field Goal Percentage
        try:
            threeFieldGoal = \
                bs.find('div', {'id': 'info'}).find('div', {'class': 'p2'}).find_all('div')[1].find_all('p')[1].text
        except:
            threeFieldGoal = ''

        # Get Free Throw Percentage
        try:
            freeThrowPercentage = \
            bs.find('div', {'id': 'info'}).find('div', {'class': 'p2'}).find_all('div')[2].find_all('p')[1].text
        except:
            freeThrowPercentage = ''

        # Get Effective Field Goal Percentage
        try:
            effectiveFieldGoal = \
            bs.find('div', {'id': 'info'}).find('div', {'class': 'p2'}).find_all('div')[3].find_all('p')[1].text
        except:
            effectiveFieldGoal = ''
    else:
        try:
            fieldGoalPercentage = \
            bs.find('div', {'id': 'info'}).find('div', {'class': 'p2'}).find_all('div')[0].find_all('p')[1].text
        except:
            fieldGoalPercentage = ''

        threeFieldGoal = ''

        try:
            freeThrowPercentage = \
            bs.find('div', {'id': 'info'}).find('div', {'class': 'p2'}).find_all('div')[1].find_all('p')[1].text
        except:
            freeThrowPercentage = ''

        effectiveFieldGoal = ''

    # Get Player Efficiency Rating
    try:
        playerEfficiency = bs.find('div',{'id':'info'}).find('div',{'class':'p3'}).find_all('div')[0].find_all('p')[1].text
    except:
        playerEfficiency = ''

    # Get Win Shares
    try:
        winShares = bs.find('div',{'id':'info'}).find('div',{'class':'p3'}).find_all('div')[1].find_all('p')[1].text
    except:
        winShares = ''

    # Combine player data into one dictionary
    baller = {'nameAndSurname':nameAndSurname,'games':games, 'points':points,'totalRebounds':totalRebounds,
              'assists':assists,'fieldGoalPercentage':fieldGoalPercentage,'threeFieldGoal':threeFieldGoal,
              'freeThrowPercentage':freeThrowPercentage,'effectiveFieldGoal':effectiveFieldGoal,'playerEfficiency':playerEfficiency,'winShares':winShares}

    # Add player info to the final dataframe
    d = d.append(baller, ignore_index=True)


# If scraper is restrained to 100 webpages and `save_output_to_csv` is set `True`, results are saved to 'ballers_small.csv' file
if limit_to_100 and save_output_to_csv:
    d.to_csv('ballers_small.csv', index = False)
# If scraper is not restrained to 100 webpages and `save_output_to_csv` is set `True`, results are saved to 'ballers_big.csv' file
elif save_output_to_csv:
    d.to_csv('ballers_big.csv', index = False)

