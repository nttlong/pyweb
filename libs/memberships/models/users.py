import pymqr
class imps():
    class Login(object):
        def __init__(self):
            import datetime
            self.Time = datetime.datetime, True
            self.TimeUtc = datetime.datetime, True
            self.SessionID = str, True
            self.Language = str, True
    class SignOut(object):
        def __init__(self):
            import datetime
            self.Time = datetime.datetime, True
            self.TimeUtc = datetime.datetime, True
            self.SessionID = str, True
    class Profile(object):
        def __init__(self):
            import datetime
            self.FirstName = str, True
            self.LastName = str, True
            self.BirthDate = datetime.datetime, True
class docs():
    @pymqr.documents.EmbededDocument()
    class Login (imps.Login):pass
    @pymqr.documents.EmbededDocument()
    class Signout (imps.SignOut):pass
    @pymqr.documents.EmbededDocument()
    class Profile (object):pass

@pymqr.documents.Collection("users")
@pymqr.documents.UniqueIndex([
    "UserName"
],["Email"])
class Users(object):
    class Logins(imps.Login):pass
    class Signouts(imps.SignOut):pass
    def __init__(self):
        import datetime
        self.UserName = str,True # type is text and require
        self.Email = str,True #Email
        self.HashPassword = str,True
        self.PasswordSalt = str,True
        self.CreatedOn = datetime.datetime,True
        self.CreatedBy = str,True
        self.IsSysAdmin =bool,True
        self.Profile = imps.Profile, True
        self.IsActive = bool,True
        self.ActivateOn = datetime
        self.Logins = [imps.Login],True,[]
        self.Signouts = [imps.SignOut],True,[]
        self.RoleCode = str,True
        self.Description =str,True

