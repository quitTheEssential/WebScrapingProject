from urllib import request
from bs4 import BeautifulSoup as BS
from bs4 import Comment
import re
import pandas as pd

url = 'https://www.basketball-reference.com/players/'
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

limit_to_100 = True
counter = 0

d = pd.DataFrame({'nameAndSurname':[], 'position':[], 'shoots':[], 'height':[],
                  'weight':[], 'birthYear':[], 'games':[], 'points':[],
                  'totalRebounds':[],'assists':[],'fieldGoalPercentage':[],'threeFieldGoal':[],
                  'freeThrowPercentage':[],'effectiveFieldGoal':[]})

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
    print(player)
    html = request.urlopen(player)
    bs = BS(html.read(), 'html.parser')
    try:
        nameAndSurname = bs.find('div',{'id':'meta'}).find_all('div').find('h1',{'itemprop':'name'}).find('span').text
    except:
        nameAndSurname = ''

    print(nameAndSurname)
    # baller = {'nameAndSurname':nameAndSurname, 'position':position, 'shoots':shoots, 'height':height,
    #           'weight':weight, 'birthYear':birthYear, 'games':games, 'points':points,
    #           'totalRebounds':totalRebounds,'assists':assists,'fieldGoalPercentage':fieldGoalPercentage,
    #           'threeFieldGoal':threeFieldGoal,'freeThrowPercentage':freeThrowPercentage,'effectiveFieldGoal':effectiveFieldGoal}
    #
    # d = d.append(baller, ignore_index=True)

