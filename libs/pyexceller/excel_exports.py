#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Định nghĩa entity cho dùng để gi nhận dữ liệu export to excel
"""
from pymqr.documents import Collection,EmbededDocument
import datetime

@EmbededDocument()
class ExcelExportTokensColumnInfoLookup(object):
    def __init__(self):
        self.Source = str,True
        self.FieldValue = str,True
        self.FieldDisplay = str, True

@EmbededDocument()
class ExcelExportTokensColumnInfo(object):
    def __init__(self):
        self.Caption = str,True
        self.Field = str,True
        self.Format = str,True
        self.Lookup = ExcelExportTokensColumnInfoLookup, False
        self.Index = int,True

@Collection("sys_excel_export_tokens")
class ExcelExportTokens(object):
    def __init__(self):
        self.Username = str, True # User thực hiện export
        self.Language  = str, True # Ngôn ngữ lúc chọn export
        self.Filename  = str, True # tên file mà người dùng sẽ download
        self.ViewPath = str, True # Tính năng mà người dùng thực hiện download
        self.AppName = str , True # App mà người dùng thực hiện download
        self.CreatedOn = datetime.datetime, True, datetime.datetime.now # Ngày tạo, giá trị mặc định là ngày hiện tại
        self.IsExprired = bool,True, False # Đã hết hạn download giá trị mặc định là Flase
        self.filter = object,False # Điều kiện lọc
        self.Schema = str, True
        self.Columns = [ExcelExportTokensColumnInfo]
        self.Source = str, True
        self.Pipeline = object,True