import scrapy
from scrapy.contrib.spiders.crawl import CrawlSpider,Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlParserLinkExtractor
from scrapy.contrib.linkextractors.regex import RegexLinkExtractor
import re
from pprint import pprint

class MySpider(scrapy.Spider):
    name = 'resourcer'

    def genBaseUrls(self,url):
        domain = re.match("^https?://([^/]+)",url).group(0)
        return [
            url,
            domain + "/",
            domain + "/robots.txt",
            domain + "/sitemap.xml",
        ]

    def __init__(self, scope="^https?://seattlenetworks.com/", start_url="https://seattlenetworks.com/", *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)

        self.scope = re.compile(scope)
        self.start_urls = self.genBaseUrls(start_url)

        self.resource_extractors = (
            LxmlParserLinkExtractor(attr="href",      tag="a"),
            LxmlParserLinkExtractor(attr="href",      tag="area"),
            LxmlParserLinkExtractor(attr="href",      tag="base"),
            LxmlParserLinkExtractor(attr="href",      tag="link"),
            LxmlParserLinkExtractor(attr="src",       tag="script"),
            LxmlParserLinkExtractor(attr="src",       tag="source"),
            LxmlParserLinkExtractor(attr="src",       tag="img"),
            LxmlParserLinkExtractor(attr="src",       tag="iframe"),
            LxmlParserLinkExtractor(attr="src",       tag="embed"),
            LxmlParserLinkExtractor(attr="src",       tag="audio"),
            LxmlParserLinkExtractor(attr="src",       tag="track"),
            LxmlParserLinkExtractor(attr="src",       tag="video"),
            LxmlParserLinkExtractor(attr="poster",    tag="video"),
            LxmlParserLinkExtractor(attr="data",      tag="object"),
        )
        self.form_extractors = (
            LxmlParserLinkExtractor(attr="action",    tag="form"),
            LxmlParserLinkExtractor(attr="formaction",tag="input"),
        )

    def parse(self, response):
        #TODO: log to HARpy
        for extractor in self.resource_extractors:
            for resource in extractor.extract_links(response):
                if re.match(self.scope,resource.url) is not None:
                    yield scrapy.http.Request(url=resource.url)
