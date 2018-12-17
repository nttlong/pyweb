import pymqr
@pymqr.documents.Collection("sys.roles")
class Role(object):
    def __init__(self):
        self.Code=str,True
        """Role code"""
        self.Name = str,True
        """Name of role"""
        self.FName = str,True
        self.Users=[str]
        self.Description=str