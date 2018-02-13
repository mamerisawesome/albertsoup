'''Wrapper for BeautifulSoup (Satisfy my needs senpai)'''

import urllib.request as request
import re
from bs4 import BeautifulSoup

class SoupBowl:
    '''Helper for the BeautifulSoup library'''
    def __init__(self, url=None):
        self.url = url if url is not None else ''
        self.soup = None

    def serve(self, url=None):
        '''Use the url for BeautifulSoup and integrate that with the class'''
        if not url:
            raise ValueError('Url must not be empty')

        if not isinstance(url, str):
            raise AttributeError('Url must be a string')

        _url = self.url if self.url else url
        req = request.Request(url, headers={'User-Agent' : "Magic Browser"})
        page = request.urlopen(req)

        self.soup = BeautifulSoup(page, 'html.parser')

        return self

    def get(self, target=''):
        '''Gets the target from an extracted HTML document'''
        if not target:
            return

        if target == 'tastysoup':
            return self.soup

        cur = None
        if re.search(r'\#\w+', target):
            cur = self.soup.find(id=re.compile(target[1:]))

        elif re.search(r'\.\w+', target):
            cur = self.soup.find_all(class_=re.compile(target[1:]))

        else:
            cur = self.soup.find_all(re.compile(target))

        return cur
