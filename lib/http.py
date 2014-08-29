import urlparse 

class Request():
    method = None
    path = None
    version = None
    headers = None
    body = None
    url = None

    def __init__(self):
        raise NotImplementedError()

        
class Response():
    version = None
    status = None
    reason = None
    headers = None
    body = None
    remainder = None
    
    def __init__(self,**kwargs):
        raise NotImplementedError()


class FORMRequest():
    def __init__(self,action,params,enctype="application/x-www-form-urlencoded",method="GET"):
        pass
        
    

class URLRequest(Request):
    def __init__(self,url):
        self.method = "GET"
        self.version = 1.1
        self.body = ""
        self.url = url
        parsed = urlparse.urlsplit(url)
        self.path = urlparse.urlunsplit([None,None,parsed.path,parsed.query,None])
        self.headers = {"Host":parsed.netloc}


class RawResponse(Response):
    def __init__(self,data):
        pos = self.readStatusLine(data,0)
        pos = self.readHeaders(data,pos)
        content_length = filter(lambda x: x[0].lower() == "content-length", self.headers)
        if len(content_length) == 1:
            length = int(content_length[0][1])
            self.body = data[pos:pos+length]
            pos = pos+length
        if len(content_length) > 1:
            raise ValueError("Too many content-length headers!")

        self.remainder = data[pos:]

    def readStatusLine(self,data,pos):
        # HTTP-Version SP Status-Code SP Reason-Phrase CRLF
        pos = self.readVersion(data,pos)
        pos = self.readStatusCode(data,pos)
        pos = self.readReasonPhrase(data,pos)
        return pos

    def readStatusCode(self,data,pos):
        self.status = int(data[pos:pos+4])
        return pos+4

    def readVersion(self,data,pos):
        if "HTTP/" != data[pos:pos+5]:
            raise ValueError("Not HTTP-Version string at %d" % pos)
        self.version = float(data[pos+5:pos+8])
        return pos+9

    def readReasonPhrase(self,data,pos):
        end = data[pos:].find("\r\n")
        self.reason = data[pos:pos+end]
        return pos+end+2

    def readHeaders(self,data,pos):
        self.headers = []
        cur = pos
        end = data[cur:].find("\r\n")
        while end != 0:
            header = data[cur:cur+end]
            cur = cur+end+2
            end = data[cur:].find("\r\n")
            while data[cur] in (" ","\t"):
                header += self.data[cur:cur+end]
                cur = cur+end+2
                end = data[cur:].find("\r\n")
            self.headers.append(header.split(': ',1))
        return cur+2

import sys
from pprint import pprint
if __name__ == '__main__':
    parsed = RawResponse(sys.stdin.read())
    pprint(parsed.__dict__)
