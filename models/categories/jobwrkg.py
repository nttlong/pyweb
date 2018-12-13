# -*- coding: utf-8 -*-
from .. import commons
import pymqr
class imps():
    class job_working_group(commons.BaseObject):
        def __init__(self):
            super(imps.job_working_group,self).__init__()
            self.LevelCode=[str],True,[]
            self.Parent=str,True,None
            self.Level = int,True,0

@pymqr.documents.Collection("cat.jobwrkg")
class JobWrkG(imps.job_working_group):pass

