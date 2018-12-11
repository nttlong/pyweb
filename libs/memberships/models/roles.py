from pymqr import documents
@documents.Collection("roles")
@documents.UniqueIndex([
    "Code"
])
class Roles(documents.BaseDocuments):
    def __init__(self):
        self.Code=str,True
        """Role code"""
        self.Name = str,True
        """Name of role"""
        self.FName = str,True
        self.Users=[str]
        self.Description=str




