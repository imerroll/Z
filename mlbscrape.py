import json
import pandas as pd
import requests
import scipy.stats as stats
from bs4 import BeautifulSoup as bs


URL = 'https://www.mlb.com/stats/at-bats?page={}&playerPool=ALL'


def main():
    #h = scrape_h()
    #rename_headers(h)
    
    #fix_names(h)
    #make_z(h)

    #h = pd.read_json('hitters.json')
    #h = pd.read_json('adj_h.json')
    #sort_z(h)
    h = pd.read_json('temp z.json')
    final_z(h)


def scrape_h():
    df = pd.DataFrame()
    s = requests.Session()
    for i in range(1, 9):
        r = s.get(URL.format(i))
        table = pd.read_html(r.content)
        #t = table[0].to_dict()
        df = df._append(table, ignore_index=True)
        #hitters.update(t)
    hitters = df.to_dict()
    with open('hitters.json', 'w') as f:
        json.dump(hitters, f)
    h = pd.DataFrame.from_dict(hitters)
    return h


def rename_headers(df):
    col_rename = []
    for col in df.columns:
        if col != "caret-upcaret-downABcaret-upcaret-downAB":
            col_len = int(len(col)/2)
            col_rename.append(col[:col_len])
        else:
            col_rename.append('AB')

    df.columns = col_rename
    df = df.to_dict()
    with open('hitters.json', 'w') as f:
        json.dump(df, f)


def fix_names(df):
    for idx, row in df.iterrows():#[0:5].iterrows():
        name = df.at[idx, 'PLAYER']#row[0]
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
        df.at[idx, 'PLAYER'] = f"{last}, {first}"
        #@row[0] = f"{last}, {first}"
    df = df.to_dict()
    with open('hitters.json', 'w') as f:
        json.dump(df, f)


def make_z(df):
    scaling = ['', '', '']
    print(df.head())
    
    for i in range(3, 18):
        stat_max = df.iloc[:,i].max()
        scaling.append(100/stat_max)
    adjust_z = []
    
    # for every row aka player in h
    for idx, row in df.iterrows():
        temp = [df.at[idx, 'PLAYER']]
        for i in range(3, 18):
            temp.append(float("{:.3f}".format(df.iloc[idx, i] * scaling[i])))
        temp.append(float("{:.3f}".format(sum(temp[1:]))))
        adjust_z.append(temp)
        #adjust_z.update({
        #    df.at[idx, 'PLAYER']: temp
            #h.at[idx, 'PLAYER']: h.iloc[idx,i]#[[h.iloc[idx,i]]*scaling[i] for i in range(3, 18)]
        #})
    with open('adj_h.json', 'w') as f:
        json.dump(adjust_z, f)


def sort_z(df):
    #print(df.head())
    df = df.sort_values(16, ascending=False)
    df = df.to_dict()
    with open('temp z.json', 'w') as f:
        json.dump(df, f)


def final_z(df):
    print(type(df))
    z = []
    for idx, row in df.iterrows():
        temp = []
        for stat in row:
            temp.append(stat)
        z.append(temp)
    with open('final z.json', 'w') as f:
        json.dump(z, f)


if __name__ == "__main__":
    main()