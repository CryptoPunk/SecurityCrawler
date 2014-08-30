from bs4 import BeautifulSoup
from urlparse import urljoin
import html,http
import os

from . import Scraper

class SitemapXML(Scraper):
    @staticmethod
    def canparse(request,response):
        if response.body.find("http://www.sitemaps.org/schemas/sitemap/0.9") > -1:
            return True
        return False

    def __init__(self,request,response):
        self.request = request
        self.response = response
        self.doc = BeautifulSoup(response.body, "xml")

    def __iter__(self):
        print self.response.body
        for location in self.doc.find_all('loc'):
            yield html.Resource(urljoin(self.request.url, location.get_text()))

