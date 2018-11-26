from pyparams_validator import types
from pymqr import settings
import hashlib, uuid
from pymqr import query
from . models import users
import exceptions
import datetime
import pymqr
from pymqr import pydocs
from flask import session,Session


@types(
    UserName = (str,True), #Username is require
    Password = (str,True), #Password is require
    Email = (str,True), #Email is requie
    IsSysAdmin=(bool,True),
    IsActive = (bool,True),
    ActivateOn =datetime.datetime,
    Profile = (dict(
        FirstName = (str,True),
        LastName = (str,True),
        BirthDate = datetime.datetime
    ),False)
)
def create_user(data):
    """
    Create a user
    :param data:
    :return:
    """
    Users =users.Users
    qr = query (settings.getdb (), Users)
    user = qr.where(pymqr.filters.UserName == data.UserName).object
    if user.is_empty():
        salt = uuid.uuid4().hex
        hash_object = hashlib.sha1 (data.Password + salt)
        user_data = Users<<{
            Users.UserName:data.UserName,
            Users.HashPassword:hash_object.hexdigest(),
            Users.PasswordSalt: salt,
            Users.Email: data.Email,
            Users.IsSysAdmin:True,
            Users.IsActive:data.IsActive,
            Users.Logins:[]
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
    from pymqr import mobject
    """
    Validate user by username and Password
    :param data:
    :return:
    """
    qr = query(settings.getdb(),users.Users)
    user_data = qr.match(
        pymqr.funcs.expr(
            (pymqr.funcs.strcasecmp(
                users.Users.UserName,
                data.UserName
            )==0) &
            users.Users.IsActive
        )).project(
        "_id",
        users.Users.UserName,
        users.Users.Email,
        users.Users.IsSysAdmin,
        users.Users.PasswordSalt,
        users.Users.HashPassword,
        pymqr.docs.FirstName<<users.Users.Profile.FirstName,
        pymqr.docs.LastName << users.Users.Profile.LastName,
        pymqr.docs.BirthDate << users.Users.Profile.BirthDate
    ).object
    if user_data.is_empty():
        return None
    else:
        hash_object = hashlib.sha1 (data.Password + user_data.PasswordSalt)
        if hash_object.hexdigest() == user_data.HashPassword:
            x = user_data.filter_to_oject(
                users.Users.IsSysAdmin,
                users.Users.UserName,
                users.Users.Email,
                pymqr.docs.FirstName,
                pymqr.docs.LastName,
                pymqr.docs.BirthDate
            )
            return x

        else:
            return None
@types(pydocs.Fields)
def find_user(filter):
    qr = query (settings.getdb (), users.Users)
    return qr.where(filter).object

@types(
    Session = (object,True),
    User = (object,True),
    Language=(str,True)
)
def SignIn(data):
    """
    do sigin with session
    :param data:
    :return:
    """
    data.Session.update({
        "user":data.User.to_dict()
    })
    v = users.Users.create()
    qr = query (settings.getdb (), users.Users)
    login_item = users.Logins<<{
        users.Logins.Language:data.Language,
        users.Logins.TimeUtc:datetime.datetime.utcnow(),
        users.Logins.Time:datetime.datetime.now(),
        users.Logins.SessionID: data.Session.sid
    }
    ret = qr.where(pymqr.filters.UserName==data.User.UserName).push({
        users.Users.Logins:login_item
    }).commit()
    x=ret
@types(str)
def Sigout(sessionId):
    from . models import Sessions as _session
    qr = query(settings.getdb(),_session.Sessions)
    qr.where(pymqr.filters.sid==session.sid)
    


    pass
