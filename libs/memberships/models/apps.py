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
class __method_privilege_require__(object):
    def __init__(self):
        self.Insert = bool,True,False
        self.Update = bool, True, False
        self.Delete = bool, True, False
        self.View = bool, True, False
        self.Import = bool, True, False
        self.Export = bool, True, False
        self.Print = bool, True, False
        self.Custom = str, True, ""
@EmbededDocument()
class MethodPrivilegeRequire(__method_privilege_require__): pass
class __view_method__(object):
    class Requires(__method_privilege_require__):pass
    def __init__(self):
        self.Name = str,True
        self.Description = str,False
@EmbededDocument()
class ViewMethod(__view_method__):pass
class __View__(object):
    class Roles(__Role__):pass
    class API(__view_method__):pass
    def __init__(self):
        self.ViewPath = str, True
        """ViewPath hold value of controller template path"""
        self.Url  =str,True
        self.SupportPrivileges = [str], True, ['insert', 'update', 'delete', 'print', 'export', 'import']
        self.Roles = [__Role__],True,[]
        self.API = [ViewMethod],True,[]
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










