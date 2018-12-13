
from .. import commons
import pymqr
def __init_com_level__():
    return True,docs.ComLevel<<{}
def __competency_type__():
    return True,docs.ComType<<{}
class imps():
    class competency_level(commons.BaseObject):
        def __init__(self):super(imps.competency_level,self).__init__()
    class competency_type(commons.BaseObject):
        def __init__(self):super(imps.competency_type,self).__init__()
    class task(commons.RootObject):
        def __init__(self):
            super(imps.task,self).__init__()
            from uuid import uuid4
            self.RecId = str,True,uuid4
            self.Name = str,True
            self.Weight = float,True,0
    class factor(commons.BaseObject):
        def __init__(self):
            super(imps.factor,self).__init__()
            from uuid import uuid4
            self.RecId = str,True,uuid4
            self.Weight = float,True,0
    class kpi(commons.RootObject):
        def __init__(self):
            super(imps.kpi,self).__init__()
            self.Unit = int,True,0
            self.Cycle = int,True,0
            self.Weight =float,True,0
            self.ScoreFrom = float,True,0
            self.ScoreTo = float,
            self.StandardMark =float
            self.Note = str
    class competency(commons.BaseObject):
        def __init__(self):
            from uuid import uuid4
            self.RecId = str,True,uuid4
            self.Grade = float,True,0
            self.ComLevel=imps.competency_level,True,__init_com_level__
            self.Weight = float,True,0
            self.Note = str
            self.ComType=imps.competency_type,True,__competency_type__
            self.IsRequire=bool,True,False

class docs():
    @pymqr.documents.EmbededDocument()
    class ComLevel(imps.competency_level):pass
    @pymqr.documents.EmbededDocument()
    class ComType(imps.competency_type):pass
    @pymqr.documents.EmbededDocument()
    class Task(imps.task):pass
    @pymqr.documents.EmbededDocument()
    class Factor(imps.factor):pass
    @pymqr.documents.EmbededDocument()
    class KPI(imps.kpi):pass
    @pymqr.documents.EmbededDocument()
    class Competency(imps.competency):pass

@pymqr.documents.Collection("cat.JobWrk")
@pymqr.documents.UniqueIndex([
    "Code"
])
class JobWrk(commons.BaseObject):
    def __init__(self):
        from datetime import datetime

        self.JobWDuty =str,True
        self.GjwCode = str,True
        self.IsLock = bool,True,False
        self.IsJobWMainStaff = bool,True,False
        self.ReportToJobW=str,True,None
        self.InternalProcess = str,True,None
        self.CombineProcess = str,True,None
        self.EffectDate = datetime,True,None
        self.JobPosCode = str,True,None
        self.DeptApply = datetime,True,None
        self.DeptContact = [str],True,[]
        self.JobWNext = [str],True,[]
        self.JobWChange =[str],True,[]
        self.Task=[imps.task],True,[]
        self.Factor=[imps.factor],True,[]
        self.KPI = [imps.kpi],True,[]
        self.Competency =[imps.competency],True,[]



