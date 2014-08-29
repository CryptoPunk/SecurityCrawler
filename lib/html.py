class Resource():
    url = None

    def __init__(self,url):
        self.url = url

    def __repr__(self):
        contents = "url = %s" % (repr(self.url))
        if len(contents) > 40:
            contents = contents[:37] + "..."
        return "Resource(%s)" % contents

class Form():
    action = None
    params = None
    enctype = None
    method = None

    def __init__(self,action,params,enctype="application/x-www-form-urlencoded",method="GET"):
        self.action = action   
        self.params = params
        self.enctype = enctype
        self.method = method

    def __repr__(self):
        contents = "action = %s, enctype = %s, method = %s" % (repr(self.action),repr(self.enctype),repr(self.method))
        if len(contents) > 40:
            contents = contents[:37] + "..."
        return "Form(%s)" % contents
