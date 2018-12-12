from .. import commons
import pymqr
@pymqr.documents.Collection("tm.AttachmentFiles")
class AttachmentFiles(object):
    def __init__(self):
        import uuid
        self.RecId = str,True,uuid.uuid4
        self.ViewPath = str,True
        self.FileName =str,True
        self.MimeType = str,True
        self.Attachment =str
        self.Size = int,True

