'''Crawler'''
import re
import json
import scrapy

from helpers import filter_message, parse_data, soupify

class BitcoinTalkSpider(scrapy.Spider):
    name = 'Crawler for bitcointalk.org Filipino section'
    start_urls = ['https://bitcointalk.org/index.php?topic=1358010.0']
    secret = hash('Almer is so awesome')

    def parse(self, response):
        soup = soupify(html=response.css('#bodyarea').extract_first())
        containers = soup.find(id=re.compile('quickModForm')).table.find_all(filter_message)

        rows = []
        for row in containers:
            data = parse_data(row)

            if data is not None:
                rows.append(data)

        self.secret = hash(self.secret+100)
        open('out/bitcointalk.' + str(abs(self.secret)) + '.json', 'w+')
        with open('out/bitcointalk.' + str(abs(self.secret)) + '.json', 'w') as outfile:
            json.dump(rows, outfile)

        next_page = response.css('table .prevnext:nth-child(n+2) a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
