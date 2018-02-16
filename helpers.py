'''Helper functions for user-defined lambdas'''
import urllib.request as request
from bs4 import BeautifulSoup

def soupify(url):
    '''Init soup dish'''
    req = request.Request(url, headers={'User-Agent' : "Magic Browser"})
    page = request.urlopen(req)

    return BeautifulSoup(page, 'html.parser')

def filter_message(tag):
    '''Filters containers that have messages on the bitcoin forum'''
    if tag.name != 'tr' or not tag.has_attr('class'):
        return False

    if isinstance(tag.attrs['class'], str) and len(tag.attrs['class']) == 22:
        return True

    if isinstance(tag.attrs['class'], list):
        for data in tag.attrs['class']:
            if len(data) == 22:
                return True

            return False

    return False

def _clean_message(msg):
    '''Will clean unnecessary data in extracted data'''
    text = ''
    for tag in msg:
        if tag.name == 'br' or tag.name == 'img' or tag.name == 'div':
            continue
        else:
            text += tag.string

    return text


def _handle_quoteheader(quote):
    '''Will handle author and date in quote header'''
    data = {}

    parse_data = quote[11:].split(' on ')
    data['author'] = parse_data[0]
    data['timestamp'] = parse_data[1]

    return data

def _handle_nest(msg):
    '''Will handle nested messages in data'''
    data = {}

    data['quote'] = []

    quotes = msg.find_all(class_='quote')
    quote_headers = msg.find_all(class_='quoteheader')
    for i in range(0, len(quotes)):
        data['quote'].append({
            'header': _handle_quoteheader(quote_headers[i].string),
            'content': _clean_message(quotes[i].contents)
        })

    data['body'] = _clean_message(msg.contents)

    return(data)

def parse_data(soup):
    data = {}
    try:
        # author
        data['author'] = {}
        data['author']['name'] = soup.select('.poster_info')[0].b.a.string
        data['author']['title'] = soup.select('.poster_info')[0].div.contents[0].strip()

        if data['author']['title'] == 'Hero Member':
            return None

        # content
        data['content'] = {}
        data['content']['header'] = soup.select('.td_headerandpost')[0].select('.subject')[0].a.string
        data['content']['timestamp'] = soup.select('.td_headerandpost')[0].select('.smalltext')[0].string.strip()
        data['content']['message'] = _handle_nest(soup.select('.td_headerandpost')[0].select('.post')[0]) # @TODO handle nested quotes

        return data

    except Exception as e:
        return None
