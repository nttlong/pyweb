from pymqr.documents import  Collection,EmbededDocument,BaseDocuments,UniqueIndex

class __Role__(object):
    """
    Define detail of embed Role in View
    """
    def __init__(self):
        self.Role = str,True
        """Role which refer to roles.Code"""
        self.IsAllowInsert = bool,True,False
        """Allow insert with default value is False"""
        self.IsAllowUpdate = bool, True, False
        """Allow update with default value is False"""
        self.IsAllowDelete = bool, True, False
        """Allow delete with default value is False"""
        self.IsAllowExport = bool, True, False
        """Allow export to excel with default value is False"""
        self.IsAllowImport = bool, True, False
        """Allow import to excel with default value is False"""
        self.IsAllowPrint = bool, True, False
        """Allow import to print with default value is False"""

@EmbededDocument()
class RoleDoc(__Role__):
    """
    Embed doc for query or create instance Ex: myInstance=RoleDoc<<{
    RoleDoc.Role:"Admin"
    }
    """
    pass
class __View__(object):
    class Roles(__Role__):pass
    def __init__(self):
        self.ViewPath = str, True
        """ViewPath hold value of controller template path"""
        self.Url  =str,True
        self.SupportPrivileges = [str], True, ['insert', 'update', 'delete', 'print', 'export', 'import']
        self.Roles = [__Role__],True,[]
        self.Description = str
@EmbededDocument()
class ViewDoc(__View__): pass
@Collection("apps")
@UniqueIndex(["AppName"])
class Apps(object):
    class Views(__View__):pass
    def __init__(self):

        self.AppName=str,True
        """Application name"""
        self.Views =[__View__],True,[]
        """Description of application"""
        self.Description = str










