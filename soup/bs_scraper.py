from urllib import request
from bs4 import BeautifulSoup as BS
from bs4 import Comment
import re
import pandas as pd

url = 'https://www.basketball-reference.com/players/'
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

limit_to_100 = True
save_output_to_csv = True
counter = 0

d = pd.DataFrame({'nameAndSurname':[],
                  # 'position':[], 'shoots':[], 'height':[],'weight':[], 'birthYear':[], <----- removed columns
                  'games':[], 'points':[],'totalRebounds':[],'assists':[],'fieldGoalPercentage':[],'threeFieldGoal':[],
                  'freeThrowPercentage':[],'effectiveFieldGoal':[],'playerEfficiency':[],'winShares':[]})

alphabet = bs.find('div',{'id':'all_alphabet'}).find(text=lambda text: isinstance(text, Comment)).findAllNext('a', {'href':
    re.compile('\/players\/[a-z]+\/$')})

letters_href_list = ['https://www.basketball-reference.com' + text['href'] for text in alphabet]

players_href_list = []
for letter in letters_href_list:
    html = request.urlopen(letter)
    bs = BS(html.read(), 'html.parser')
    players_list = bs.find('table',{'id':'players'}).find('tbody').find_all('a',{'href':re.compile('\/players\/[a-z]+\/')})
    for link in players_list[:20]:
        if limit_to_100:
            if counter < 100:
                players_href_list.append('https://www.basketball-reference.com' + link['href'])
                counter += 1
            else:
                break
        else:
            players_href_list.append('https://www.basketball-reference.com' + link['href'])

for player in players_href_list:
    html = request.urlopen(player)
    bs = BS(html.read(), 'html.parser')
    try:
        nameAndSurname = bs.find('div',{'id':'meta'}).find('div',{'itemtype':'https://schema.org/Person'}).h1.span.text
    except:
        nameAndSurname = ''

    # try:
    #     position = bs.find('div',{'id':'meta'}).find('div',{'itemtype':'https://schema.org/Person'}).find_all('p')[5].text.strip()
    # except:
    #     position = ''

    try:
        games = bs.find('div',{'id':'info'}).find('div',{'class':'p1'}).find_all('div')[0].find_all('p')[1].text
    except:
        games = ''

    try:
        points = bs.find('div',{'id':'info'}).find('div',{'class':'p1'}).find_all('div')[1].find_all('p')[1].text
    except:
        points = ''

    try:
        totalRebounds = bs.find('div',{'id':'info'}).find('div',{'class':'p1'}).find_all('div')[2].find_all('p')[1].text
    except:
        totalRebounds = ''

    try:
        assists = bs.find('div',{'id':'info'}).find('div',{'class':'p1'}).find_all('div')[3].find_all('p')[1].text
    except:
        assists = ''

    try:
        fieldGoalPercentage = bs.find('div',{'id':'info'}).find('div',{'class':'p2'}).find_all('div')[0].find_all('p')[1].text
    except:
        fieldGoalPercentage = ''

    try:
        threeFieldGoal = bs.find('div',{'id':'info'}).find('div',{'class':'p2'}).find_all('div')[1].find_all('p')[1].text
    except:
        threeFieldGoal = ''

    try:
        freeThrowPercentage = bs.find('div',{'id':'info'}).find('div',{'class':'p2'}).find_all('div')[2].find_all('p')[1].text
    except:
        freeThrowPercentage = ''

    try:
        effectiveFieldGoal = bs.find('div',{'id':'info'}).find('div',{'class':'p2'}).find_all('div')[3].find_all('p')[1].text
    except:
        effectiveFieldGoal = ''

    try:
        playerEfficiency = bs.find('div',{'id':'info'}).find('div',{'class':'p3'}).find_all('div')[0].find_all('p')[1].text
    except:
        playerEfficiency = ''

    try:
        winShares = bs.find('div',{'id':'info'}).find('div',{'class':'p3'}).find_all('div')[1].find_all('p')[1].text
    except:
        winShares = ''


    baller = {'nameAndSurname':nameAndSurname,
            # 'position':position,'shoots': shoots, 'height': height,'weight': weight, 'birthYear': birthYear, <----- removed columns
              'games':games, 'points':points,'totalRebounds':totalRebounds,'assists':assists,'fieldGoalPercentage':fieldGoalPercentage,
              'threeFieldGoal':threeFieldGoal,'freeThrowPercentage':freeThrowPercentage,
              'effectiveFieldGoal':effectiveFieldGoal,'playerEfficiency':playerEfficiency,'winShares':winShares}

    d = d.append(baller, ignore_index=True)

if limit_to_100 and save_output_to_csv:
    d.to_csv('ballers_small.csv', index = False)
elif save_output_to_csv:
    d.to_csv('ballers_big.csv', index = False)

