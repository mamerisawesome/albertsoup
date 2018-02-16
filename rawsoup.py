'''Wrapper for BeautifulSoup (Satisfy my needs senpai)'''
# https://stackoverflow.com/questions/38028384/beautifulsoup-is-there-a-difference-between-find-and-select-python-3-x
import re
import json

from helpers import filter_message, parse_data, soupify

soup = soupify('https://bitcointalk.org/index.php?topic=2889704.0;all')

containers = soup.find(id=re.compile('quickModForm')).table.find_all(filter_message)
rows = []
for row in containers:
    data = parse_data(row)

    if data is not None:
        rows.append(data)

print(rows)
