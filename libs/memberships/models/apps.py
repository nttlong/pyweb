from pymqr.documents import  Collection,EmbededDocument,BaseDocuments,UniqueIndex

class __Role__(object):
    """
    Define detail of embed Role in View
    """
    def __init__(self):
        self.Role = str,True
        self.IsAllowInsert = bool,True,True
        self.IsAllowUpdate = bool, True, True
        self.IsAllowDelete = bool, True, True
        self.IsAllowExport = bool, True, True
        self.IsAllowImport = bool, True, True
        self.IsAllowPrint = bool, True, True
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
        self.Views =[__View__],True,[]
        self.Description = str










