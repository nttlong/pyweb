from pymqr import documents
import datetime
@documents.Collection("sessions")
class Sessions(object):
    def __init__(self):
        self.expiration = datetime.datetime
        self.sid = str
