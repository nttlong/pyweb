import pymqr
import datetime
from pymqr import documents
@documents.Collection("users")
class Users(documents.BaseDocuments):
    @documents.EmbededDocument ()
    class Profile (object):
        def __init__(self):
            self.FirstName = str, True
            self.LastName = str, True
            self.BirthDate = datetime.datetime, True

    def __init__(self):
        self.UserName = str,True # type is text and require
        self.Email = str,True #Email
        self.HasPassword = str,True
        self.PasswordSalt = str,True
        self.CreatedOn = datetime.datetime,True
        self.CreatedBy = str,True
        self.IsSysAdmin =bool,True
        self.Profile = dict
