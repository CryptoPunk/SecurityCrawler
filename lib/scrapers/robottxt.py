from bs4 import BeautifulSoup
from urlparse import urljoin
import html,http
import os

from . import Scraper

class RobotTXT(Scraper):
    @staticmethod
    def canparse(request,response):
        if request.path.lower() == "/robots.txt":
                return True
        return False

    def __init__(self,request,response):
        self.request = request
        self.response = response
        #raise NotImplementedError()

    def __iter__(self):
        for line in self.response.body.split('\n'):
            args = line.strip().split(":",1)
            if len(args) == 2:
                if args[0].lower() in ('disallow','allow','sitemap'):
                    yield html.Resource(urljoin(self.request.url, args[1].strip()))
