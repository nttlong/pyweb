import pymqr
@pymqr.documents.Collection("sys.apps")
class App(object):
    @pymqr.documents.EmbededDocument()
    class Views(object):
        @pymqr.documents.EmbededDocument()
        class API(object):
            def __init__(self):
                self.Name=str,True,None
                self.RequirePrivilege=str,True,None
                self.Description = str,False,None
        def __init__(self):
            self.ViewPath = str,True
            self.Url = str,True
            self.API = [type(self).API],True,[]

    def __init__(self):
        self.AppName=str,True,""
