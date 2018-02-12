from urllib.request import urlopen
from bs4 import BeautifulSoup

# Setup
target = 'http://www.bloomberg.com/quote/SPX:IND'
page = urlopen(target)
soup = BeautifulSoup(page, 'html.parser')

# Extract
name_container = soup.find('h1', attrs={'class': 'name'})
name = name_container.text.strip()

price_container = soup.find('div', attrs={'class':'price'})
price = price_container.text

import csv
from datetime import datetime

with open('index.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([name, price, datetime.now()])

# @TODO enable modularity
# @TODO make a general case for function