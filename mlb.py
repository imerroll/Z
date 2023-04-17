import json
import pandas as pd
import requests
import scipy.stats as stats
from bs4 import BeautifulSoup as bs

URL = 'https://www.mlb.com/stats/at-bats?page={}&playerPool=ALL'

mlb_scrape = {}
#for i in range(1, 9):
#    print(URL.format(i))

page_content = requests.get(URL.format(1)).text
soup_content = bs(page_content, 'html5lib')
tbody = soup_content.find('tbody')

# get stat headers/categories
thead = soup_content.find('thead')
cats = thead.findChildren(['th'])
for th in cats:
    cat = th.find('abbr')
    print(cat.contents[0])

'''
# testing
for i in range(1, 2):
    url = URL.format(i)
    page = requests.get(url).text
    soup = bs(page, 'html5lib')
    tbody = soup.find('tbody')
    players = tbody.findChildren(['tr'])
    print(players)
    for player in players:
        name_cell = player.find('a')
        id = name_cell['href'][8:]
        name = f"{name_cell.contents[2].contents[0]}, {name_cell.contents[0].contents[0]}"
        print(name)
'''

'''
df = pd.DataFrame()
s = requests.Session()
for i in range(1, 9):
    r = s.get(URL.format(i))
    table = pd.read_html(r.content)
    #t = table[0].to_dict()
    df = df._append(table, ignore_index=True)
    #t = table[0].to_dict()
    #hitters.update(t)
hitters = df.to_dict()
with open('hitters.json', 'w') as f:
    json.dump(hitters, f)
'''




r = s.get(URL.format(1))
#print(r.status_code)
table = pd.read_html(r.content)
t = table[0].to_dict()
#with open('table.json', 'w') as f:
#    json.dump(t, f)
d = pd.read_json('table.json')
for idx, row in d.iterrows():#[0:5].iterrows():
    name = row[0]
    #print(idx, row[0])
    for i, ch in enumerate(name):
        if ch.isupper():
            name = name[i:]
            #print(name)
            break
    for i, ch in enumerate(name[1:]):
        if ch.isupper():
            first = name[:i+1].strip()
            name = name[i+1:]
            #print(f"First: |{first}|, rem: |{name}|")
            break
    space = name.find(' ')
    name = name[space+1:]
    for i, ch in enumerate(name[1:]):
        if ch.isupper():
            last = name[:i+1].strip()
            #print(f"Last: |{last}|")
            break

col_rename = []
for col in d.columns:
    if col != "caret-upcaret-downABcaret-upcaret-downAB":
        col_len = int(len(col)/2)
        print(col[:col_len])
        #col_rename.update({col: col[:col_len]})
        col_rename.append(col[:col_len])
    else:
        #col_rename.update({"caret-upcaret-downABcaret-upcaret-downAB": "AB"})
        col_rename.append('AB')
print(col_rename)

d.columns = col_rename
#d.rename(col_rename, inplace=True)
print(d.head())

'''
players = tbody.findChildren(['tr'])
bichette = players[0]
name = bichette.find('a')
tds = bichette.findChildren(['td'])
for td in tds:
    if td.find('a') == None:
        print(td.contents[0])
    else:
        a = td.find('a')
        print(a.contents[0])
    #a = td.find('a')
    #print(a)
    #print(td.contents[0])
#print(name['href'][8:])
#print(name.contents[0].contents[0], name.contents[2].contents[0])
'''