from bs4 import BeautifulSoup
from urlparse import urljoin
import html,http
import os

from pprint import pprint

basepath = os.path.dirname(__file__)
html_resources = []
for filename in ['html5.res','xhtml11.res']:
    fh = open(os.path.join(basepath,filename))
    html_resources += filter(lambda x: len(x) > 0 and x[0][0] != "#",[l.strip().split() for l in fh.read().split('\n')])

class Scraper():
    @staticmethod
    def canparse(request,response):
        raise NotImplementedError()

    def __init__(self,request,response):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

class BS4HTML(Scraper):
    callbacks = {
        "URI": lambda scraper,elem,attr: [scraper.foundURL(elem[attr])],
        "URILIST": lambda scraper,elem,attr: [scraper.foundURL(x) for x in elem[attr]],
        "PINGURI": lambda scraper,elem,attr: [scraper.foundURL(x) for x in elem[attr].split()],
        "SRCSET": lambda scraper,elem,attr: [scraper.foundURL(x.strip().split()[0]) for x in elem[attr].split(",")], 
        "FORM": lambda scraper,elem,attr: [scraper.foundFormAction(elem,attr)], #TODO: fix form parser to catch all submit button scenario
        "SCRIPT": lambda scraper,elem,attr: [], #TODO: add in a script parser
        "CSS": lambda scraper,elem,attr: [], #TODO: add in a CSS parser
    }

    @staticmethod
    def canparse(request,response):
        for k,v in response.headers:
            if k.lower() == "content-type" and v.lower() in ('application/xhtml+xml','text/html'):
                return True
        return False

    def __init__(self,request,response,parser=None):
        self.request = request
        self.response = response
        self.doc = BeautifulSoup(response.body,parser)
        
    def foundURL(self,url):
        return html.Resource(urljoin(self.request.url, url))

    def foundFormAction(self,elem,attr):
        def getFormContext(root,elem):
            if elem.name == "form":
                return elem 
            else:
                if elem.has_attr("form"): # http://www.whatwg.org/specs/web-apps/current-work/multipage/forms.html#form-owner
                    return root.find_all('form',id=elem["form"])
                else:
                    cur_elem = elem.parent
                    while cur_elem is not None:
                        if cur_elem.name == 'form':
                            return cur_elem
                    return None

        def getFormElements(root,form):
            # http://www.whatwg.org/specs/web-apps/current-work/multipage/forms.html#form-submission-algorithm
            # TODO: revise this pattern with the above algorithm

            submittable = ("button","input","keygen","object","select","textarea")

            #list1: all child submittable elements with form attribute not set
            for etype in sumbittable:
                for elem in form.find_all(etype,attrs={'name':True}):
                    yield elem
            #list2: all submittable elements with form attrubte set to id of form.
            if form.has_attr('id'):
                for etype in submittable:
                    for elem in root.find_all(etype,attrs={'name':True,form=form['id']}):
                        yield elem

            #list3: all submittable elements with form attrubte set to name of form.
            if form.has_attr('name'):
                for etype in submittable:
                    for elem in root.find_all(etype,attrs={'name':True,form=form['name']}):
                        yield elem

        form_parent = getFormContext(self.doc,elem)

        action = elem[attr] # Guaranteed to exist, and be the current form action currently.

        enctype = "application/x-www-form-urlencoded"
        if elem.name != "form":
            if elem.has_attr("formenctype"):
                enctype = elem["formenctype"]
            elif form_parent.has_attr("enctype"):
                enctype = elem["enctype"]
        elif elem.has_attr("enctype"):
            enctype = elem["enctype"]

        method = "GET"
        if elem.name != "form":
            if elem.has_attr("formmethod"):
                method = elem["formmethod"]
            elif form_parent.has_attr("method"):
                method = elem["method"]
        elif elem.has_attr("method"):
            method = elem["method"]

        #TODO: populate params
        #params = getFormElements()
        params = map(lambda elem: elem["name"], getFormElements())

        return html.Form(action=action,params=params,enctype=enctype,method=method)
        
    def __iter__(self):
        for tag,attr,callback in html_resources:
            if "*" == tag:
                elements = self.doc.find_all(attrs={attr:True})
            else:
                elements = self.doc.find_all(tag,attrs={attr:True})

            for elem in elements:
                for result in self.callbacks[callback].__call__(self,elem,attr):
                    yield result
        
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

