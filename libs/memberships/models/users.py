import pymqr
@pymqr.documents.Collection("sys.users")
class User(object):
    @pymqr.documents.EmbededDocument()
    class Profile(object):
        """

        """
        def __init__(self):
            import datetime
            self.FirstName = str, True
            self.LastName = str, True
            self.BirthDate = datetime.datetime, True
    @pymqr.documents.EmbededDocument()
    class Logins(object):
        """

        """
        def __init__(self):
            import datetime
            self.Time = datetime.datetime, True
            self.TimeUtc = datetime.datetime, True
            self.SessionID = str, True
            self.Language = str, True
    """================================"""
    @pymqr.documents.EmbededDocument()
    class Signouts(object):
        def __init__(self):
            import datetime
            self.Time = datetime.datetime, True
            self.TimeUtc = datetime.datetime, True
            self.SessionID = str, True
    def __init__(self):
        """

        """
        import datetime
        self.UserName = str,True # type is text and require
        self.Email = str,True #Email
        self.HashPassword = str,True
        self.PasswordSalt = str,True
        self.CreatedOn = datetime.datetime,True
        self.CreatedBy = str,True
        self.IsSysAdmin =bool,True
        self.Profile = type(self).Profile,True,type(self).Profile<<{}
        self.IsActive = bool,True
        self.ActivateOn = datetime
        self.Logins = [type(self).Logins],True,[]
        self.Signouts = [type(self).Signouts],True,[]
        self.RoleCode = str,True
        self.Description =str,True
