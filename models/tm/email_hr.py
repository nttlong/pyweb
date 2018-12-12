from .. import commons
import pymqr
@pymqr.documents.Collection("tm.emails")
class AttachmentFiles(commons.BaseObject):
    def __init__(self):
        import uuid
        self.EmpCode = str,True,uuid.uuid4
        self.DepCode = str,True
        self.Email =str,True
       