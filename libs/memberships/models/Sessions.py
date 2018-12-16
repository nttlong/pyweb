import pymqr
@pymqr.documents.Collection("sessions")
class Session(object):
    def __init__(self):
        from  datetime import datetime
        self.expiration = datetime
        self.sid = str