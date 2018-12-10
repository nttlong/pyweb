from pymqr.documents import  Collection,EmbededDocument,BaseDocuments
class __role__(object):
    def __init__(self):
        self.Role = str,True
        self.IsAllowInsert = bool,True,True
        self.IsAllowUpdate = bool, True, True
        self.IsAllowDelete = bool, True, True
        self.IsAllowExport = bool, True, True
        self.IsAllowImport = bool, True, True
        self.IsAllowPrint = bool, True, True

class View(object):
    class Roles(__role__):pass
    def __init__(self):
        self.ViewPath = str, True
        self.SupportPrivileges = [str], True, ['insert', 'update', 'delete', 'print', 'export', 'import']
        self.Roles = [__role__],True,[]
        self.Description = str
@Collection("views")
class Apps(object):
    class Views(View):pass
    def __init__(self):
        self.AppName=str,True
        self.Views =[View],True,[]
        self.Description = str










