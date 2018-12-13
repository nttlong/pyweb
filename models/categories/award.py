# -*- coding: utf-8 -*-
from ..commons import RootObject,BaseOrgObject,BaseObject,get_user_name
class imps():
    class award(BaseObject):
        def __init__(self):
            super(imps.award,self).__init__()
            self.Levels=[imps.level],True,[]
            self.Places = [imps.place],True,[]
            self.Type = int,True,bool
            self.IsTeam = bool,True,False
    class level(BaseObject):
        def __init__(self):
            super(imps.level,self).__init__()
            import uuid
            self.RecId=str,True,uuid.uuid4
            self.MaxTimePerYear = int,False
    class place(BaseObject):
        def __init__(self):
            super(imps.place,self).__init__()


import pymqr
@pymqr.documents.Collection("cat.award")
@pymqr.documents.UniqueIndex([
    "Code"
])
class Award(imps.award):
    @pymqr.documents.EmbededDocument()
    class Levels(imps.level):pass
    @pymqr.documents.EmbededDocument()
    class Places(imps.place):pass



