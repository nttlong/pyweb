from pymqr import documents
@documents.Collection("languages")
@documents.UniqueIndex([
    "app","language","key","view"
])
class Languages(documents.BaseDocuments):
    def __init__(self):
        self.app = str,True
        self.language = str,True
        self.key = str,True
        self.view =str,True
        self.value = str, True
        self.view = str,True
