from pyparams_validator import types
from pymqr import settings,funcs
import hashlib, uuid
from pymqr import query
from . models import users,apps
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
            from pymqr import errors
            if isinstance(error,errors.DataException):
                if error.error_type == errors.ErrorType.duplicate:
                    if error.fields.count(users.Users.UserName.__name__)>0:
                        raise exceptions.UserIsExist (data.UserName)
                    else:
                        raise error
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
@types(
    UserName= (str,True),
    Password = (str,True)
)
def change_password(data):
    from pymqr import settings as st,query,filters
    from .models import users
    salt = uuid.uuid4 ().hex
    hash_object = hashlib.sha1 (data.Password + salt)
    ret,err,result = query(st.getdb(),users.Users).where(filters.UserName==data.UserName).set({
        users.Users.PasswordSalt:salt,
        users.Users.HashPassword:hash_object.hexdigest()
    }).commit()


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
@types(object)
def SignOut(session):
    from . models import Sessions as _session
    qr = query(settings.getdb(),_session.Sessions)
    ret,error,result=qr.where(pymqr.filters.sid==session.sid).delete()
    logout_item = users.Signouts<<{
        users.Signouts.SessionID:session.sid,
        users.Signouts.Time:datetime.datetime.now(),
        users.Signouts.TimeUtc:datetime.datetime.utcnow()
    }
    entity = query(settings.getdb(), users.Users).where(pymqr.filters.UserName == session["user"]["UserName"])
    entity = entity.push({
        users.Users.Signouts: logout_item
    })

    ret,error,redult = entity.commit()
    session.clear()

def GetListOfUsers(page_size=50,page_index=0,pagefilter= None,sort=None):
    from . models import roles
    qr = query (settings.getdb (), users.Users).lookup(
        roles.Roles,
        users.Users.RoleCode,
        roles.Roles.Code,
        "Roles"
    ).unwind("Roles").project(
        pymqr.docs._id<<0,
        pymqr.docs.UserId<<pymqr.docs._id,
        users.Users.UserName,
        pymqr.docs.LoginCount<<pymqr.funcs.size(users.Users.Logins),
        users.Users.Email,
        pymqr.docs.FirstName<< users.Users.Profile.FirstName,
        pymqr.docs.LastName << users.Users.Profile.LastName,
        pymqr.docs.RoleCode<<pymqr.docs.Roles.Code,
        pymqr.docs.RoleName<<pymqr.docs.Roles.Name
    )
    ret = qr.get_page(page_size,page_index)
    return ret


@types(
    Code=(str,True),
    Name = (str,True),
    FName = str,
    Description=str
)
def create_role(data):
    from . models import roles
    qr= query(settings.getdb(),roles.Roles)
    try:
        ret,error, result = qr.insert(data).commit()
        return ret,error
    except Exception as ex:
        raise ex
@types(
    AppName = (str,True),
    Url = (str,True),
    Template =(str,True)
)
def register_view(data):
    qr = query(settings.getdb(),apps.Apps)
    app = qr.match(funcs.expr(apps.Apps.AppName==data.AppName)).count().object

    if app.is_empty() or app.ret==0:
        qr_insert = qr.new()
        data = apps.Apps<<{
            apps.Apps.AppName:data.AppName,
            apps.Apps.Views:[
                apps.ViewDoc<<{
                    apps.ViewDoc.ViewPath : data.Template,
                    apps.ViewDoc.Url : data.Url
                }
            ]
        }
        ret,err,result = qr_insert.insert(data).commit()
        if err:
            raise err
    else:
        qr_update = qr.new().where(
            funcs.expr(
                apps.Apps.AppName==data.AppName
            )
        )
        ret,err,result= qr_update.push({
            apps.Apps.Views:apps.ViewDoc<<{
                apps.ViewDoc.ViewPath: data.Template,
                apps.ViewDoc.Url: data.Url
            }
        }).commit()
        if err:
            raise err






