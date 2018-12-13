from .. import commons
import pymqr
class implemnetation(object):
    class ScoreByCoeff(object):
        def __init__(self):
            self.ApproverLevel = int,True
            self.Coeff = float,True
    class SetupApproveLevel(object):
        def __init__(self):
            import uuid
            self.rec_id = str,True,uuid.uuid4
            self.ApproveLevel = int,True
            self.ApproverValue =int
            self.EmailApproveCode = str
            self.EmailApproveName =str
            self.EmailApproveTo =[str],
            self.EmailApproveCC = [str]
            self.EmailApproveMore = str
            self.EmailRejectCode = str
            self.EmailRejectName = str
            self.EmailRejectTo = [str]
            self.EmailRejectCC = [str]
            self.EmailRejectMore =str
            self.EmailApproveCancelCode =str
            self.EmailApproveCancelName =str
            self.EmailApproveCancelTo = str
            self.EmailApproveCancelCC = [str]
            self.EmailApproveCancelMore = str
            self.EmailRejectCancelCode = str
            self.EmailRejectCancelName = str
            self.EmailRejectCancelTo = [str]
            self.EmailRejectCancelCC = [str]
            self.EmailRejectCancelMore = [str]
            self.DefaultApproverCode =str
            self.DefaultApproverFullName = str,
            self.NotReceiveEmail = bool
    class SetupApproverEmp(object):
        def __init__(self):
            import uuid
            self.RecId = str,True,uuid.uuid4
            self.ApproveLevel =int,True
            self.EmpCode = str,True
            self.AppoverCode = str,True
            self.EmpFullName = str
            self.ApproverFullName = str
    class SetupApproverDept(object):
        def __init__(self):
            from uuid import uuid4
            self.RecId = str,uuid4
            self.ApproveLevel = int,True
            self.DeptCode = str,True
            self.AppoverCode = str
            self.DeptName = str
            self.DeptName2 = str
            self.ApproverFullName = str
    class SetupApproverSubstitute(object):
        def __init__(self):
            from uuid import uuid4
            from datetime import datetime
            self.RecId = str,True,uuid4
            self.AppoverCode = int,True
            self.SubstituteCode = str,True
            self.ApproverFullName = str
            self.SubstituteFullName =str
            self.FromDate = datetime
            self.ToDate = datetime
            self.Note = str
    class SetupApplyEmp(object):
        def __init__(self):
            from uuid import uuid4
            self.RecId = str,True,uuid4
            self.EmpCode = str,True
            self.EmpFullName = str

class embeded(object):
    @pymqr.documents.EmbededDocument()
    class ScoreByCoeff(implemnetation.ScoreByCoeff):pass
    @pymqr.documents.EmbededDocument()
    class SetupApproveLevel(implemnetation.SetupApproveLevel):pass
    @pymqr.documents.EmbededDocument()
    class SetupApproverEmp(implemnetation.SetupApproverEmp):pass
    @pymqr.documents.EmbededDocument()
    class SetupApproverSubstitute(implemnetation.SetupApproverSubstitute):pass
    @pymqr.documents.EmbededDocument()
    class SetupApplyEmp(implemnetation.SetupApplyEmp):pass
    @pymqr.documents.EmbededDocument()
    class SetupApproverDept(implemnetation.SetupApproverDept):pass

@pymqr.documents.Collection("tm.SetupProcess")
@pymqr.documents.UniqueIndex([
    "ProcessId"
])
class SetupProcess(object):
    class ScoreByCoeff(embeded.ScoreByCoeff):pass
    class SetupApproveLevel(embeded.SetupApproveLevel):pass
    class SetupApproverDept(embeded.SetupApproverDept):pass
    class SetupApproverSubstitute(embeded.SetupApproverSubstitute):pass
    class SetupApplyEmp(embeded.SetupApplyEmp):pass
    def __init__(self):
        from datetime import datetime
        from .. import commons
        self.ProcessId = str,True
        self.ProcessName = str,True
        self.IsNotApplyProcess =bool,False
        self.ViewPath = str
        self.MaxApproveLevel =int,True,3
        self.IsApproveByDept =bool,True,False
        self.IsRequireReason = bool,True,False
        self.IsRequireWhenApprove = bool,True,False
        self.IsRequireWhenReject = bool,False,False
        self.IsShowListApprover = bool,True,False
        self.IsReselectApprover = bool,True,False
        self.IsRequireAttachFile = bool,True,False
        self.FileSizeLimit = int,True,50*1024*1024
        self.ExcludeFileTypes = str,True,""
        self.IsEmailCancel = bool,True,False
        self.IsEmailDelete = bool,True,False
        self.IsEmailInstead = bool,True,False
        self.EmailSendCode = str,True,""
        self.EmailSendName = str,True,""
        self.EmailSendTo = [str],True,[]
        self.EmailSendCC = [str],True,[]
        self.EmailSendMore = str,True,""
        self.EmailCancelCode = str,True,""
        self.EmailCancelName = str,True,""
        self.EmailCancelTo = [str],True,[]
        self.EmailCancelCC = [str],True,[]
        self.EmailCancelMore = str,True,""
        self.EmailDeleteCode = str,True,""
        self.EmailDeleteName = str,True,""
        self.EmailDeleteTo = [str],True,[]
        self.EmailDeleteCC = [str],True,[]
        self.EmailDeleteMore = str,True,""
        self.EmailInsteadCode = str,True,""
        self.EmailInsteadName = str,True,""
        self.EmailInsteadTo = [str],True,[]
        self.EmailInsteadCC = [str],True,[]
        self.EmailInsteadMore = str,True,""
        self.IsSendEmailPronto =bool,True,False
        self.IsSendEmailOnce = bool,True,False
        self.SendEmailOnceFromHour = str,True,""
        self.SendEmailOnceToHour = str,True,""
        self.ProcessLevelApplyFor = int,True,0
        self.ScoreBy = int,True,0
        self.CreatedOn = datetime,True,datetime.now
        self.CreatedBy = str,True,commons.get_user_name
        self.ModifiedOn = datetime,False
        self.ScoreByCoeff = embeded.ScoreByCoeff,True,embeded.ScoreByCoeff<<{}
        self.modified_by = str,True,""
        self.SetupApproveLevel = [embeded.SetupApproveLevel],True,[]
        self.SetupApproverEmp = [embeded.SetupApplyEmp],True,[]
        self.SetupApproverDept = [embeded.SetupApproverDept],True,[]
        self.SetupApproverSubstitute = [embeded.SetupApproverSubstitute],True,[]
        self.SetupApplyEmp = [embeded.SetupApplyEmp],True,[]
        self.EmpCodes=[str],True,[]
