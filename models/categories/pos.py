import pymqr
from ..commons import BaseObject,RootObject,BaseOrgObject
class imps():
    class pos(BaseObject):
        def __init__(self):
            from datetime import datetime
            super(imps.pos,self).__init__()
            self.ManLevel=int,True,0
            self.IsFix=bool,True,False
            self.Coeff = float,True,0
            self.BeginDateCal= datetime,True,None
            self.Details=[imps.details],True,[]
    class details(BaseObject):
        def __init__(self):
            from  uuid import uuid4
            super(imps.details,self).__init__()
            self.RecId=str,True,uuid4
            self.SenionrityFrom=int,True,0
            self.SenionrityTo = int,True,None
            self.Coefficient = float,True,None
            self.Salary = float,True,0

class docs():
    @pymqr.documents.EmbededDocument()
    class Details(imps.details):pass

@pymqr.documents.Collection("cat.pos")
@pymqr.documents.UniqueIndex([
    "Code"
])
class Pos(imps.pos):
    class Details(imps.details):pass
