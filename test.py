import feedparser
import json

url = 'https://www.mlbtraderumors.com/players/pete-alonso/feed.xml'

feed = feedparser.parse(url)
print(feed.feed.title)
#print(feed.feed)
for idx, entry in enumerate(feed.entries):
    with open(f'feed {idx}.json', 'w') as f:
        json.dump(entry, f)