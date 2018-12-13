from ..commons import BaseObject,BaseOrgObject,RootObject
import pymqr
class imps():
    class enums(RootObject):
        def __init__(self):
            super(imps.enums,self).__init__()
            self.Language =str,True,"en"
            self.Name = str,True
            self.Values=[imps.values],True,[]
            self.IsMSel=bool,True,False
    class values(RootObject):
        def __init__(self):
            super(imps.values,self).__init__()
            self.Value=int,True,0
            self.Caption=str,True,None
            self.Custom=str,True,None
class docs():
    @pymqr.documents.EmbededDocument()
    class Values(imps.values):pass
@pymqr.documents.Collection("sys.enums")
@pymqr.documents.UniqueIndex([
    "Language","Name"
])
class Enums(imps.enums):
    class Values(imps.values):pass

