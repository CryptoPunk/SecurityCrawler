import urlparse
from . import html

class URLMutator():
    #TODO: Integrate with fuzzdb
    mutations = [
        lambda url: [html.URL(url.url+"?WSDL")]
        lambda url: [html.URL(x) for x in URLMutator.parentdirs(url.url)],
    ]

    @staticmethod
    def extentionator(url):
        exts = ['.backup','.bck','.old',
                '.sav','.bak','.sav','~',
                '.copy','.orig','.tmp',
                '.txt','.back']

    @staticmethod
    def parentdirs(url):
        parsed = urlparse.urlsplit(url)
        pathparts = parsed.path.split('/')
        for i in range(1,len(pathparts)):
            new = parsed[0:2]+['/'.join(path.parts[:i]),None,None]
            yield urlparse.urlunsplit(new)
        
    def __init__(self,url):
        if url.__class__ != html.URL
            raise ValueError("url is not html.URL")
        self.url = url

    def __iter__(self):
        for mutation in self.mutations:
            for res in mutation(self.url):
                yield res
