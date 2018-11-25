from pyparams_validator import types
from libs.pyfy import settings
import hashlib, uuid
from pymqr import query
from . models import users
salt = uuid.uuid4().hex

@types(
    UserName = (str,True), #Username is require
    Password = (str,True), #Password is require
    Email = (str,True), #Email is requie
)
def create_user(data):
    Users =users.Users
    user = query(settings.db,Users).where(Users.UserName == data.UserName).object
    if user.is_empty():
        user_data = Users.create()
        user_data.UserName = data.UserName



    pass