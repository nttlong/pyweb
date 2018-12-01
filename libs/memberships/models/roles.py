from pymqr import documents
@documents.Collection("roles")
@documents.UniqueIndex([
    "Code"
])
class Roles(documents.BaseDocuments):
    def __init__(self):
        self.Code=str,True
        self.Name = str,True
        self.FName = str,True
        self.Users=[str]
        self.Description=str




