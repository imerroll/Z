import json
import numpy as np
import pandas as pd
import requests
import scipy.stats as stats
from bs4 import BeautifulSoup as bs

'''
SOUP_URL = 'https://www.fantasypros.com/mlb/stats/hitters.php'#'https://www.fangraphs.com/projections?pos=all&stats=bat&type=rthebatx'

page_content = requests.get(SOUP_URL).text
soup_content = bs(page_content, 'html5lib')
temp = soup_content.find('tbody')#, {'class': 'table-scroll'})
players = temp.findChildren(['tr'])
tds = players[0].findChildren(['td'])
name = str(tds[1].contents[0])[str(tds[1].contents[0]).find('>')+1:str(tds[1].contents[0]).rfind('<')]
temp = soup_content.find('thead')
cats = temp.find(['tr'])
cat_tds = cats.findChildren(['th'])
stats = []
temp = []
for cat in cat_tds[1:]:
    temp.append(cat.contents[0])
stats.append(temp)


for player in players:
    temp = []
    tds = player.findChildren(['td'])
    name = str(tds[1].contents[0])[str(tds[1].contents[0]).find('>')+1:str(tds[1].contents[0]).rfind('<')]
    temp.append(name)
    for td in tds[2:]:
        #try:
        #    temp.append(int(td.contents[0]))
        #except:
        #    try:
        #        temp.append(float(td.contents[0]))
        #    except:
        temp.append(td.contents[0])
    stats.append(temp)
with open('fpros.json', 'w') as f:
    json.dump(stats, f)
'''
# ["Player", "AB", "R", "HR", "RBI", "SB", "AVG", "OBP", "H", "2B", "3B", "BB", "K", "SLG", "OPS", "Rost%"], 

#df = pd.read_json('fpros.json')
#print(df.head())

#slugging = stats.zscore(df[13])
#print(slugging)

zscores = pd.read_json('z.json')
#print(zscores.head())
#zscores = stats.zscore(df.iloc[:,1:15])
#zscores.insert(0, "Name", value=df.iloc[:, 0])
#print(zscores.head())
#print(zscores.iloc[0,:])
#print(zscores[13].max())
# print(zscores.max(axis=0))
#zscores.to_json('z.json')
#with open('z.json', 'w') as f:
#    json.dump(zscores, f)
f = ['']
cats = ['', 'AB', 'R', 'HR', 'RBI', 'SB', 'AVG', 'OBP', 'H', '2B', '3B', 'BB', 'K', 'SLG', 'OPS']
for i in range(1, 15):
    #print(100/zscores[i].max())
    f.append(100/zscores[f"{i}"].max())
print(f)

#print(zscores["1"].max())
adjusted_z = {}
for idx, row in zscores.iterrows():
    #print(idx, row)
    adjusted_z.update({
        row['Name']: [row[f'{i}']*f[i] for i in range(1, 15)]
    })
with open('adj_z.json', 'w') as f:
    json.dump(adjusted_z, f)