from pyparams_validator import types
from pymqr import settings
import hashlib, uuid
from pymqr import query
from . models import users
import exceptions
import datetime
import pymqr
from pymqr import pydocs


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
    qr = query (settings.getdb (), Users)
    user = qr.where(Users.UserName == data.UserName).object
    if user.is_empty():
        salt = uuid.uuid4().hex
        hash_object = hashlib.sha1 (data.Password + salt)
        user_data = Users<<{
            Users.UserName:data.UserName,
            Users.HashPassword:hash_object.hexdigest(),
            Users.PasswordSalt: salt,
            Users.Email: data.Email,
            Users.IsSysAdmin:True
        }
        user_data,error, result = qr.insert(user_data.to_dict()).commit()
        if error:
            raise error
        else:
            return user_data
    else:
        raise exceptions.UserIsExist(data.UserName)

@types(
    UserName = (unicode,True),
    Password = (unicode,True)
)
def validate_user(data):
    qr = query(settings.getdb(),users.Users)
    user_data = qr.where(pymqr.filters.UserName == data.UserName).object
    if user_data.is_empty():
        return False
    else:
        hash_object = hashlib.sha1 (data.Password + user_data.PasswordSalt)
        return hash_object.hexdigest() == user_data.HashPassword
@types(pydocs.Fields)
def find_user(filter):
    qr = query (settings.getdb (), users.Users)
    return qr.where(filter).object

