'''Wrapper for BeautifulSoup (Satisfy my needs senpai)'''

import urllib.request as request
import re
from bs4 import BeautifulSoup

class SoupBowl:
    '''Helper for the BeautifulSoup library'''
    def __init__(self, url=None, html=None):
        self.url = url if url is not None else ''
        self.html = html if html is not None else ''
        self.soup = None
        self.curr = None

    def serve(self, url=None, html=None):
        '''Use the url for BeautifulSoup and integrate that with the class'''
        if not url and not html:
            raise ValueError('Url or Html must not be empty')

        if not isinstance(url, str) and not html:
            raise AttributeError('Url must be a string')

        if url or self.url:
            _url = self.url if self.url else url
            req = request.Request(url, headers={'User-Agent' : "Magic Browser"})
            page = request.urlopen(req)

            self.soup = BeautifulSoup(page, 'html.parser')

        elif isinstance(self.html, str) and isinstance(html, str):
            _html = self.html if self.html else html
            self.soup = BeautifulSoup(_html, 'html.parser')

        else:
            _html = self.html if self.html else html
            self.soup = _html

        return self

    def _scoop_filter(self, tag, data, recursive):
        '''Identify kind of input if tag, id, or class'''
        curr = None

        # filter by function
        if re.search(r'\w+(\.\w+)?\(\w+\)', data):
            parsed = data[:-1].split('(')
            if parsed[0] == 'tag.name':
                curr = tag.find_all(lambda tag: tag.name == 'b', recursive=recursive)

        # filter by id
        elif re.search(r'\#\w+', data):
            curr = tag.find_all(id=re.compile(data[1:]), recursive=recursive)

        # filter by class
        elif re.search(r'\.\w+', data):
            curr = tag.find_all(class_=re.compile(data[1:]), recursive=recursive)

        # filter by attribute
        elif re.search(r'\[\w+\=\"\w+\"\]', data):
            curr = tag.find_all(attrs={parsed[0]: parsed[1:-1]}, recursive=recursive)

        # filter by tag
        else:
            curr = tag.find_all(data, recursive=recursive)

        return curr

    def scoop(self, target='', recursive=True):
        '''Gets the target from an extracted HTML document'''
        if not target:
            return

        if target == 'tastysoup':
            return self.soup

        curr = None
        if isinstance(self.curr, list):
            curr = []
            for tag in self.curr:
                curr.extend(self._scoop_filter(tag, target, recursive))
        else:
            curr = self._scoop_filter(self.soup, target, recursive)

        self.curr = curr
        return self

    def handpick(self, count=0):
        '''Take certain number of elements filtered'''
        if count == 1:
            self.curr = self.taste()[0]
        else:
            self.curr = self.taste()[:count]
        return self

    def taste(self, mode='raw'):
        '''Get value of last find value of scoop'''
        if mode == 'raw':
            output = self.curr if self.curr is not None else ''
        elif mode == 'fin':
            if isinstance(self.curr, str):
                output.extend(self.curr.string)
            elif isinstance(self.curr, list):
                output = []
                for datum in self.curr:
                    output.append(datum.string if datum.string else datum.contents)

        self.curr = None
        return output

    def is_eaten(self):
        '''Check if bowl result is empty'''
        if isinstance(self.curr, str) and self.curr.strip() != '':
            return True

        if not self.curr:
            return True

        return False
