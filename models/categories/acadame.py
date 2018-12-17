# -*- coding: utf-8 -*-
from ..commons import get_user_name,BaseObject,BaseOrgObject,RootObject
import pymqr
@pymqr.documents.Collection("lst.acadame")
@pymqr.documents.UniqueIndex(["Code"])
class Acadame(RootObject):
    @pymqr.documents.EmbededDocument()
    class Details(RootObject):
        def __init__(self):
            super(type(self),self).__init__()
            from datetime import datetime
            import uuid
            self.RecId = str,True,uuid.uuid4
            self.SeniorityFrom = int,True,0
            self.SeniorityTo = int,True,0
            self.Coefficient = float,True,0
            self.Salary = float,True,0
    def __init__(self):
        super(type(self),self).__init__()
        self.Range = int,True,0
        self.Ordinal = int,True,0
        self.Note = str
        self.IsFix =bool,True,False
        self.Coeff =float,True,0
        self.BeginDateCal = float,True,0
        self.IsLock = bool,True,False
        self.Details = [type(self).Details],True,[]
