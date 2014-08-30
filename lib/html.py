class URL():
    url = None

    def __init__(self,url):
        self.url = url

    def __repr__(self):
        contents = "url = %s" % (repr(self.url))
        if len(contents) > 40:
            contents = contents[:37] + "..."
        return "Resource(%s)" % contents

    def __eq__(self,other):
        return self.url == other.url

    def __ne__(self,other):
        return False == self.__eq__(other)

class Form():
    action = None # should be URL type.
    params = None # should be a set object, keys only
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

    def __eq__(self,other):
        return (     self.action  == other.action 
                 and self.params  == other.params
                 and self.enctype == other.enctype
                 and self.method  == other.method)

    def __ne__(self,other):
        return False == self.__eq__(other)
