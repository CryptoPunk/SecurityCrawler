from bs4 import BeautifulSoup
from urlparse import urljoin
import html,http
import os

class Scraper():
    @staticmethod
    def canparse(request,response):
        raise NotImplementedError()

    def __init__(self,request,response):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

from .bs4html import BS4HTML
from .robottxt import RobotTXT
from .sitemapxml import SitemapXML
from .xml import XML

__all__ = ['BS4HTML','RobotTXT','SitemapXML','XML']
