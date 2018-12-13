from .. import commons
class implements():
    class cer(commons.BaseObject):
        def __init__(self):
            super(implements.cer,self).__init__()
            self.ExpiredTime= int,True,0
            self.GroupCode = str,False,None
    class group(commons.BaseObject):
        def __init__(self):
            super(implements.group,self).__init__()
            self.Type = str,True,None
            self.By = str,False,None
import pymqr
@pymqr.documents.Collection("cat.cers")
class Cers(implements.cer):pass
@pymqr.documents.Collection("cat.cers_groups")
class Group(implements.group):pass


