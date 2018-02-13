'''Save and load helpers'''

import csv
from datetime import datetime

def save (data):
    name = data.name
    price = data.price

    with open('index.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([name, price, datetime.now()])
