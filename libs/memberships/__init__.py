from pyparams_validator import types
from pymqr import settings
import hashlib, uuid
from pymqr import query
from . models import users
salt = uuid.uuid4().hex
import datetime


@types(
    UserName = (str,True), #Username is require
    Password = (str,True), #Password is require
    Email = (str,True), #Email is requie
    Profile = (dict(
        FirstName = (str,True),
        LastName = (str,True),
        BirthDate = datetime.datetime
    ),False)
)
def create_user(data):
    Users =users.Users
    user = query(settings.getdb(),Users).where(Users.UserName == data.UserName).object
    if user.is_empty():
        user_data = Users.create()
        user_data<<{
            (Users.UserName,data.UserName),
            (Users.PasswordSalt, data.Password),
            (Users.Email, data.Email),
        }
        x= user_data



    pass