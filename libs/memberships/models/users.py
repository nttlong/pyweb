import pymqr
import datetime
from pymqr import documents
@documents.Collection("users")
class Users(documents.BaseDocuments):
    def __init__(self):
        self.UserName = str,True # type is text and require
        self.Email = str,True #Email
        self.HasPassword = str,True
        self.PasswordSalt = str,True
        self.CreatedOn = datetime.datetime,True
        self.CreatedBy = str,True
        self.IsSysAdmin =bool,True
