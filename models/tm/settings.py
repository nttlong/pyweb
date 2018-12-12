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

@pymqr.documents.Collection("tm.SetupProcess")
@pymqr.documents.UniqueIndex([
    "ProcessId"
])
class SetupProcess(object):
    def __init__(self):
        self.ProcessId = str,True
        self.ProcessName = str,True
        self.IsNotApplyProcess =bool,False
        self.ViewPath = str
        self.MaxApproveLevel =int,True,3
        self.IsApproveByDept =bool,True,False
        self.IsRequireReason = bool,True,False
        self.IsRequireWhenApprove = bool,True,False
        self.IsRequireWhenReject = ("bool"),
        self.IsShowListApprover = ("bool"),
        self.IsReselectApprover = ("bool"),
        self.IsRequireAttachFile = ("bool"),
        self.FileSizeLimit = ("numeric"),
        self.ExcludeFileTypes = ("text"),
        self.IsEmailCancel = ("bool"),
        self.IsEmailDelete = ("bool"),
        self.IsEmailInstead = ("bool"),
        self.EmailSendCode = ("text"),
        self.EmailSendName = ("text"),
        self.EmailSendTo = ("list"),
        self.EmailSendCC = ("list"),
        self.EmailSendMore = ("text"),
        self.EmailCancelCode = ("text"),
        self.EmailCancelName = ("text"),
        self.EmailCancelTo = ("list"),
        self.EmailCancelCC = ("list"),
        self.EmailCancelMore = ("text"),
        self.EmailDeleteCode = ("text"),
        self.EmailDeleteName = ("text"),
        self.EmailDeleteTo = ("list"),
        self.EmailDeleteCC = ("list"),
        self.EmailDeleteMore = ("text"),
        self.EmailInsteadCode = ("text"),
        self.EmailInsteadName = ("text"),
        self.EmailInsteadTo = ("list"),
        self.email_instead_cc = ("list"),
        self.email_instead_more = ("text"),
        self.is_send_email_pronto = ("bool"),
        self.is_send_email_once = ("bool"),
        self.send_email_once_from_hour = ("text"),
        self.send_email_once_to_hour = ("text"),
        self.process_level_apply_for = ("numeric"),
        self.score_by = ("numeric"),
        self.created_on = ("date", True),
        self.created_by = ("text", True),
        self.modified_on = ("date"),
        self.score_by_coeff = ("list", False, dict(
            approver_level=("numeric", True),
            Coeff=("numeric")
        )),
        self.modified_by = ("text"),
        self.setup_approve_level = ("list", False, dict(
            rec_id=("text", True),
            approve_level=("numeric", True),
            approver_value=("numeric"),
            email_approve_code=("text"),
            email_approve_name=("text"),
            email_approve_to=("list"),
            email_approve_cc=("list"),
            email_approve_more=("text"),
            email_reject_code=("text"),
            email_reject_name=("text"),
            email_reject_to=("list"),
            email_reject_cc=("list"),
            email_reject_more=("text"),
            email_approve_cancel_code=("text"),
            email_approve_cancel_name=("text"),
            email_approve_cancel_to=("list"),
            email_approve_cancel_cc=("list"),
            email_approve_cancel_more=("text"),
            email_reject_cancel_code=("text"),
            email_reject_cancel_name=("text"),
            email_reject_cancel_to=("list"),
            email_reject_cancel_cc=("list"),
            email_reject_cancel_more=("list"),
            default_approver_code=("text"),
            default_approver_full_name=("text"),
            not_receive_email=("bool"),
        )),
        self.setup_approver_emp = ("list", False, dict(
            rec_id=("text", True),
            approve_level=("numeric", True),
            employee_code=("text", True),
            appover_code=("text"),
            emp_full_name=("text"),
            approver_full_name=("text")
        )),
        self.setup_approver_dept = ("list", False, dict(
            rec_id=("text", True),
            approve_level=("int", True),
            department_code=("text", True),
            appover_code=("text"),
            department_name=("text"),
            department_name2=("text"),
            approver_full_name=("text")
        )),
        self.setup_approver_substitute = ("list", False, dict(
            rec_id=("text", True),
            appover_code=("numeric", True),
            substitute_code=("text", True),
            approver_full_name=("text"),
            substitute_full_name=("text"),
            from_date=("date"),
            to_date=("date"),
            note=("text")
        )),
        self.setup_apply_emp = ("list", False, dict(
            rec_id=("text", True),
            employee_code=("text", True),
            emp_full_name=("text")
        ))



# from qmongo import define, extends, helpers
# extends(
#             "TM_SetupProcess",
#             "base",
#             [["process_id"]],
#             process_id= ("text", True),
#             process_name= ("text", True),
#             is_not_apply_process= ("bool"),
#             function_id= ("text"),
#             max_approve_level= ("numeric"),
#             is_approve_by_dept= ("bool"),
#             is_require_reason= ("bool"),
#             is_require_when_approve= ("bool"),
#             is_require_when_reject= ("bool"),
#             is_show_list_approver= ("bool"),
#             is_reselect_approver= ("bool"),
#             is_require_attach_file= ("bool"),
#             file_size_limit= ("numeric"),
#             exclude_file_types= ("text"),
#             is_email_cancel= ("bool"),
#             is_email_delete= ("bool"),
#             is_email_instead= ("bool"),
#             email_send_code= ("text"),
#             email_send_name=("text"),
#             email_send_to= ("list"),
#             email_send_cc= ("list"),
#             email_send_more= ("text"),
#             email_cancel_code= ("text"),
#             email_cancel_name= ("text"),
#             email_cancel_to= ("list"),
#             email_cancel_cc= ("list"),
#             email_cancel_more= ("text"),
#             email_delete_code= ("text"),
#             email_delete_name= ("text"),
#             email_delete_to= ("list"),
#             email_delete_cc= ("list"),
#             email_delete_more= ("text"),
#             email_instead_code= ("text"),
#             email_instead_name= ("text"),
#             email_instead_to= ("list"),
#             email_instead_cc= ("list"),
#             email_instead_more= ("text"),
#             is_send_email_pronto= ("bool"),
#             is_send_email_once= ("bool"),
#             send_email_once_from_hour= ("text"),
#             send_email_once_to_hour= ("text"),
#             process_level_apply_for= ("numeric"),
#             score_by= ("numeric"),
#             created_on=("date", True),
#             created_by=("text", True),
#             modified_on=("date"),
#             modified_by=("text"),
#             score_by_coeff= ("list",False,dict(
#                 approver_level=("numeric",True),
#                 Coeff=("numeric")
#             )),
#             setup_approve_level = ("list",False,dict(
#                 rec_id=("text",True),
#                 approve_level=("numeric",True),
#                 approver_value = ("numeric"),
#                 email_approve_code = ("text"),
#                 email_approve_name = ("text"),
#                 email_approve_to = ("list"),
#                 email_approve_cc = ("list"),
#                 email_approve_more = ("text"),
#                 email_reject_code = ("text"),
#                 email_reject_name = ("text"),
#                 email_reject_to = ("list"),
#                 email_reject_cc = ("list"),
#                 email_reject_more = ("text"),
#                 email_approve_cancel_code = ("text"),
#                 email_approve_cancel_name = ("text"),
#                 email_approve_cancel_to = ("list"),
#                 email_approve_cancel_cc = ("list"),
#                 email_approve_cancel_more = ("text"),
#                 email_reject_cancel_code = ("text"),
#                 email_reject_cancel_name = ("text"),
#                 email_reject_cancel_to = ("list"),
#                 email_reject_cancel_cc = ("list"),
#                 email_reject_cancel_more = ("list"),
#                 default_approver_code = ("text"),
#                 default_approver_full_name = ("text"),
#                 not_receive_email = ("bool"),
#             )),
#             setup_approver_emp = ("list",False,dict(
#                 rec_id=("text",True),
#                 approve_level=("numeric",True),
#                 employee_code=("text",True),
#                 appover_code=("text"),
#                 emp_full_name=("text"),
#                 approver_full_name=("text")
#             )),
#             setup_approver_dept = ("list",False,dict(
#                 rec_id=("text",True),
#                 approve_level = ("int",True),
#                 department_code = ("text",True),
#                 appover_code = ("text"),
#                 department_name = ("text"),
#                 department_name2 = ("text"),
#                 approver_full_name = ("text")
#             )),
#             setup_approver_substitute = ("list",False,dict(
#                 rec_id=("text",True),
#                 appover_code = ("numeric",True),
#                 substitute_code = ("text",True),
#                 approver_full_name = ("text"),
#                 substitute_full_name = ("text"),
#                 from_date = ("date"),
#                 to_date = ("date"),
#                 note = ("text")
#             )),
#             setup_apply_emp = ("list",False,dict(
#                 rec_id=("text",True),
#                 employee_code = ("text",True),
#                 emp_full_name = ("text")
#             ))
#         )
