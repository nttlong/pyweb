from datetime import datetime
class BaseObject(object):
    def __init__(self):
        self.Code = str,True
        self.Name = str,True
        self.FName = str,True,""
        self.CreatedBy = str,True
        self.CreatedOn = datetime,True,datetime.now
        self.CreatedOnUtc = datetime,True,datetime.utcnow
        self.Description = str,True
        self.ModifiedBy = str,True
        self.ModifiedOn = datetime,True,datetime.now
        self.ModifiedOnUtc=datetime,True,datetime.utcnow

class BaseOrgObject(BaseObject):
    def __init__(self):
        self.Parent = str,True
        self.LevelCodes = [str],True
        self.Level = int,True
