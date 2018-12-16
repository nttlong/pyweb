import pymqr
@pymqr.documents.Collection("sys.appa")
class App(object):
    @pymqr.documents.EmbededDocument()
    class Views(object):
        def __init__(self):
            self.ViewPath = str,True
            self.Url = str,True

    def __init__(self):
        self.AppName=str,True,""
