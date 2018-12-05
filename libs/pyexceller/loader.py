from pymqr import query,filters,docs
from bson import ObjectId
from . excel_exports import ExcelExportTokens
from django_db import getdb
def get(token):
    qr = query(getdb(),ExcelExportTokens)
    qr.where(filters._id== ObjectId(token))
    ret = qr.object
    return ret
