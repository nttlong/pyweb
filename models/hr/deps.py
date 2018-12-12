# -*- coding: utf-8 -*-
import pymqr
from . import emps
from .. import commons
pymqr.documents.Collection("depts")
pymqr.documents.UniqueIndex([
    "Code"
])
class Depts(commons.BaseOrgObject):
    def __init__(self):
        self.Code = str,True
        self.Name =str,True
        self.FName=str,True
        self.Parent =str,True


# extends(
#             "HCSSYS_Departments",
#             "base",
#             [["department_code"]],
#             #id=("numeric",True),
#             department_code=("text", True),
#             department_name=("text", True),
#             department_name2=("text"),
#             department_alias=("text"),
#             #parent_id=("numeric"),
#             parent_code=("text"),
#             level=("numeric"),
#             level_code=("list"),
#             #level_code2=("text"),
#             department_tel=("text"),
#             department_fax=("text"),
#             department_email=("text"),
#             department_address=("text"),
#             #Xem lại kiểu dữ liệu
#             nation_code=("text"),
#             province_code=("text"),
#             district_code=("text"),
#             is_company=("bool"),
#             is_fund=("bool"),
#             is_fund_bonus=("bool"),
#             decision_no=("text"),
#             decision_date=("date"),
#             effect_date=("date"),
#             license_no=("text"),
#             tax_code=("text"),
#             lock_date=("date"),
#             logo_image=("text"),
#             manager_code=("text"),
#             secretary_code=("text"),
#             ordinal=("text"),
#             lock=("bool"),
#             note=("text"),
#             region_code=("text"),
#             domain_code=("text"),
#             signed_by=("text"),
#             created_on=("date"),
#             created_by=("text"),
#             modified_on=("date"),
#             modified_by=("text")
#         )
