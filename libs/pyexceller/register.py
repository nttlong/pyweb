#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
from pyparams_validator import types
from .excel_exports import ExcelExportTokens # Model excel export
from pymqr import query,docs, filters
from django_db import getdb
#yêu cầu đầu vào của tham số như sau:
@types(
    Username = (str,True), # username bắt buộc
    Language = (str,True), # username bắt buộc
    Filename = (str,True),
    ViewPath = (str,True),
    AppName = (str,True),
    Schema = (str,True),
    Filter = (object,False)
)
def approve(data):
    """
    Hàm này dùng để xác nhận việc download dữ liệu

    :return:
    """
    insert_data = ExcelExportTokens<<data.__to_dict__() # Cắt bỏ dữ liệu dư thừa nếu người dùng cố ý thêm
    qr =query(getdb(),ExcelExportTokens)
    ret,err,result = qr.insert(insert_data).commit()
    return "excel/"+result.inserted_id.__str__()



