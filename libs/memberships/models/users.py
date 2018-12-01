from datetime import datetime

import pymqr
import datetime
from pymqr import documents
@documents.EmbededDocument()
class Logins(object):
    def __init__(self):
        self.Time= datetime.datetime,True
        self.TimeUtc =datetime.datetime,True
        self.SessionID= str,True
        self.Language = str,True
@documents.EmbededDocument()
class Signouts(object):
    def __init__(self):
        self.Time = datetime.datetime, True
        self.TimeUtc = datetime.datetime, True
        self.SessionID = str, True
@documents.EmbededDocument ()
class Profile (object):
    def __init__(self):
        self.FirstName = str, True
        self.LastName = str, True
        self.BirthDate = datetime.datetime, True
@documents.Collection("users")
@documents.UniqueIndex([
    "UserName"
],["Email"])
class Users(documents.BaseDocuments):
    def __init__(self):

        self.UserName = str,True # type is text and require
        self.Email = str,True #Email
        self.HashPassword = str,True
        self.PasswordSalt = str,True
        self.CreatedOn = datetime.datetime,True
        self.CreatedBy = str,True
        self.IsSysAdmin =bool,True
        self.Profile = Profile, True
        self.IsActive = bool,True
        self.ActivateOn = datetime
        self.Logins = [Logins]
        self.Signouts = [Signouts]
        self.RoleCode = str,True

