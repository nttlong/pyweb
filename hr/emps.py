from pymqr import documents
class implementation():

    class EmpExperience(object):
        def __init__(self):
            from datetime import datetime
            self.BeginDate= datetime,True
            self.EndDate = datetime,True
            self.Salary = float,True
            self.CurrencyCode = str,False




class docs():
    @documents.EmbededDocument()
    class EmpExperience(implementation.EmpExperience):pass


@documents.Collection("emps")
@documents.UniqueIndex([
    "Code"
])
class Emps(object):
    class Experience(implementation.EmpExperience):pass
    def __init__(self):
        from datetime import datetime
        from . import deps
        self.Code = str,True
        self.FirstName = str,True
        self.LastName = str,True
        self.Experience = [implementation.EmpExperience],True,[]
        self.Dept=deps.Depts,True
        self.CreatedBy = str, True
        self.CreatedOn = datetime, True, datetime.now
        self.CreatedOnUtc = datetime, True, datetime.utcnow
        self.Description = str, True
        self.ModifiedBy = str, True
        self.ModifiedOn = datetime, True, datetime.now
        self.ModifiedOnUtc = datetime, True, datetime.utcnow

# extends(
#             "HCSEM_Employees",
#             "base",
#             [["employee_code"]],
#             photo_id=("text"),
#             employee_code=("text", True),
#             last_name=("text", True),
#             first_name=("text", True),
#             extra_name=("text"),
#             gender=("numeric"),
#             birthday=("date"),
#             b_province_code=("text"),
#             nation_code=("text"),
#             ethnic_code=("text"),
#             religion_code=("text"),
#             culture_id=("numeric"),
#             is_retrain=("numeric"),
#             train_level_code=("text"),
#             marital_code=("text"),
#             id_card_no=("text"),
#             issued_date=("date"),
#             issued_place_code=("text"),
#             mobile=("text"),
#             p_phone=("text"),
#             email=("text"),
#             personal_email=("text"),
#             document_no=("text"),
#             join_date=("date", True),
#             official_date=("date"),
#             career_date=("date"),
#             personnel_date=("date"),
#             emp_type_code=("text"),
#             labour_type=("numeric"),
#             department_code=("text", True),
#             job_pos_code=("text"),
#             job_pos_date=("date"),
#             job_w_code=("text", True),
#             job_w_date=("date"),
#             profession_code=("text"),
#             level_management=("numeric"),
#             is_cbcc=("bool"),
#             is_expert_recruit=("bool"),
#             is_expert_train=("bool"),
#             manager_code=("text"),
#             manager_sub_code=("text"),
#             user_id=("text"),
#             job_pos_hold_code=("text"),
#             job_w_hold_code=("text"),
#             department_code_hold=("text"),
#             job_pos_hold_from_date=("date"),
#             job_pos_hold_to_date=("date"),
#             end_date=("date"),
#             retire_ref_no=("text"),
#             signed_date=("date"),
#             signed_person=("text"),
#             active=("bool"),
#             note=("text"),
#             p_address=("text"),
#             p_province_code=("text"),
#             p_district_code=("text"),
#             p_ward_code=("text"),
#             p_hamlet_code=("text"),
#             t_address=("text"),
#             t_province_code=("text"),
#             t_district_code=("text"),
#             t_ward_code=("text"),
#             t_hamlet_code=("text"),
#             foreigner=("bool"),
#             vn_foreigner=("bool"),
#             is_not_reside=("bool"),
#             fo_working=("numeric"),
#             fo_permiss=("text"),
#             fo_begin_date=("date"),
#             fo_end_date=("date"),
#             created_on=("date"),
#             created_by=("text"),
#             modified_on=("date"),
#             modified_by=("text"),
#             emp_working=("list",False,dict(
#                 rec_id=("text", True),
#                 appoint=("numeric", True),
#                 effect_date=("date", True),
#                 begin_date=("date", True),
#                 end_date=("date"),
#                 decision_no=("text", True),
#                 signed_date=("date"),
#                 signer_code=("text"),
#                 note=("text"),
#                 task=("text"),
#                 reason=("text"),
#                 department_code=("text"),
#                 job_pos_code=("text"),
#                 job_w_code=("text"),
#                 emp_type_code=("text"),
#                 region_code=("text"),
#                 department_code_old=("text"),
#                 job_pos_code_old=("text"),
#                 job_w_code_old=("text"),
#                 emp_type_code_old=("text"),
#                 region_code_old=("text"),
#                 province_code=("text"),
#                 created_on=("date"),
#                 created_by=("text"),
#                 modified_on=("date"),
#                 modified_by=("text")
#                 )),
#                 emp_experience=("list",False,dict(
#                     rec_id=("text", True),
#                     begin_date=("date", True),
#                     end_date=("date"),
#                     salary=("numeric", True),
#                     currency_code=("text"),
#                     emp_type_code=("text"),
#                     job_pos_code=("text"),
#                     job_w_code=("text"),
#                     working_on=("text"),
#                     working_location=("text", True),
#                     address=("text"),
#                     profession_code=("text"),
#                     quit_job_code=("text"),
#                     reason=("text"),
#                     ref_info=("text"),
#                     note=("text"),
#                     is_na_company=("bool"),
#                     is_in_section=("bool"),
#                     created_on=("date"),
#                     created_by=("text"),
#                     modified_on=("date"),
#                     modified_by=("text")
#                     )),
#         )
#
#


# from qmongo import define, extends, helpers
# ## # from ...api import common
#
# import datetime
# _hasCreated=False
# extends(
#             "HCSEM_EmpExperience",
#             "base",
#             [['rec_id']],
#             rec_id =("text", True),
#             employee_code=("text"),
#             begin_date=("date", True),
#             end_date=("date"),
#             salary=("numeric", True),
#             currency_code=("text"),
#             emp_type_code=("text"),
#             job_pos_code=("text"),
#             job_w_code=("text"),
#             working_on=("text"),
#             working_location=("text", True),
#             address=("text"),
#             profession_code=("text"),
#             quit_job_code=("text"),
#             reason=("text"),
#             ref_info=("text"),
#             note=("text"),
#             is_na_company=("bool"),
#             is_in_section=("bool"),
#             created_on=("date"),
#             created_by=("text"),
#             modified_on=("date"),
#             modified_by=("text")
#         )
# def on_before_insert(data):
#     data.update({
#         "rec_id": common.generate_guid()
#         })
#
# def on_before_update(data):
#     pass
#
# helpers.events("HCSEM_EmpExperience").on_before_insert(on_before_insert).on_before_update(on_before_update)
