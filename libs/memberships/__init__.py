from pyparams_validator import types as __types__
from pymqr import settings ,funcs,filters,docs
import hashlib, uuid
from pymqr import query
from . models import User,App
import exceptions
import datetime
import pymqr
from pymqr import pydocs
from flask import session,Session


@__types__(
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

    qr = query (settings.getdb (), User)
    user = qr.where(pymqr.filters.UserName == data.UserName).object
    if user.is_empty():
        salt = uuid.uuid4().hex
        hash_object = hashlib.sha1 (data.Password + salt)
        user_data = User<<{
            User.UserName:data.UserName,
            User.HashPassword:hash_object.hexdigest(),
            User.PasswordSalt: salt,
            User.Email: data.Email,
            User.IsSysAdmin:True,
            User.IsActive:data.IsActive,
            User.Logins:[]
        }
        user_data,error, result = qr.insert(user_data.to_dict()).commit()
        if error:
            from pymqr import errors
            if isinstance(error,errors.DataException):
                if error.error_type == errors.ErrorType.duplicate:
                    if error.fields.count(User.UserName.__name__)>0:
                        raise exceptions.UserIsExist (data.UserName)
                    else:
                        raise error
            raise error
        else:
            return user_data
    else:
        raise exceptions.UserIsExist(data.UserName)

@__types__(
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
    qr = query(settings.getdb(),User)
    user_data = qr.match(
        pymqr.funcs.expr(
            (pymqr.funcs.strcasecmp(
                User.UserName,
                data.UserName
            )==0) &
            User.IsActive
        )).project(
        "_id",
        User.UserName,
        User.Email,
        User.IsSysAdmin,
        User.PasswordSalt,
        User.HashPassword,
        pymqr.docs.FirstName<<User.Profile.FirstName,
        pymqr.docs.LastName << User.Profile.LastName,
        pymqr.docs.BirthDate << User.Profile.BirthDate
    ).object
    if user_data.is_empty():
        return None
    else:
        hash_object = hashlib.sha1 (data.Password + user_data.PasswordSalt)
        if hash_object.hexdigest() == user_data.HashPassword:
            x = user_data.filter_to_oject(
                User.IsSysAdmin,
                User.UserName,
                User.Email,
                pymqr.docs.FirstName,
                pymqr.docs.LastName,
                pymqr.docs.BirthDate
            )
            return x

        else:
            return None
@__types__(
    UserName= (str,True),
    Password = (str,True)
)
def change_password(data):
    from pymqr import settings as st,query,filters
    from .models import User
    salt = uuid.uuid4 ().hex
    hash_object = hashlib.sha1 (data.Password + salt)
    ret,err,result = query(st.getdb(),User).where(filters.UserName==data.UserName).set({
        User.Users.PasswordSalt:salt,
        User.Users.HashPassword:hash_object.hexdigest()
    }).commit()


@__types__(pydocs.Fields)
def find_user(filter):
    qr = query (settings.getdb (), User)
    return qr.where(filter).object

@__types__(
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
    qr = query (settings.getdb (), User)
    login_item = User.Logins<<dict(
        Language=data.Language,
        TimeUtc=datetime.datetime.utcnow(),
        Time=datetime.datetime.now(),
        SessionID=data.Session.sid
    )

    ret = qr.where(pymqr.filters.UserName==data.User.UserName).push({
        User.Logins:login_item
    }).commit()
    x=ret
@__types__(object)
def SignOut(session):

    qr = query(settings.getdb(),models.Session)
    ret,error,result=qr.where(pymqr.filters.sid==session.sid).delete()
    logout_item = models.User.Signouts<<dict(
        SessionID=session.sid,
        Time=datetime.datetime.now(),
        TimeUtc=datetime.datetime.now()
    )
    entity = query(settings.getdb(), User).where(pymqr.filters.UserName == session["user"]["UserName"])
    entity = entity.push({
        User.Signouts: logout_item
    })

    ret,error,redult = entity.commit()
    session.clear()
"""
===================================================
"""
def GetListOfUsers(page_size=50,page_index=0,pagefilter= None,sort=None):
    from . models import Role
    qr = query (settings.getdb (), User).lookup(
        Role,
        User.RoleCode,
        Role.Code,
        "Roles"
    ).unwind("Roles").project(
        pymqr.docs._id<<0,
        pymqr.docs.UserId<<pymqr.docs._id,
        User.UserName,
        pymqr.docs.LoginCount<<pymqr.funcs.size(User.Logins),
        User.Email,
        pymqr.docs.FirstName<< User.Profile.FirstName,
        pymqr.docs.LastName << User.Profile.LastName,
        pymqr.docs.RoleCode<<pymqr.docs.Roles.Code,
        pymqr.docs.RoleName<<pymqr.docs.Roles.Name
    )
    ret = qr.get_page(page_size,page_index)
    return ret


@__types__(
    Code=(str,True),
    Name = (str,True),
    FName = str,
    Description=str
)
def create_role(data):
    from . models import Role
    qr= query(settings.getdb(),Role)
    try:
        ret,error, result = qr.insert(data).commit()
        return ret,error
    except Exception as ex:
        raise ex
"""
===========================================================
"""
@__types__(
    AppName = (str,True),
    Url = (str,True),
    Template =(str,True),
    API =[dict(
        description=(str,False),
        privileges = (object,True)
    )]
)
def register_view(data):
    """
    This method will registe a view in application if app was not found the method will create new app
    :param data:
    :return:
    """
    qr = query(settings.getdb(),App)
    app = qr.match(funcs.expr(App.AppName==data.AppName)).count().object
    """
    If app was not found create new app in mongodb with full fields has been declare
    in Model
    """
    if app.is_empty() or app.ret==0:
        qr_insert = qr.new()
        view =App.Views<<{
            App.Views.Url:data.Url,
            App.Views.ViewPath:data.Template.lower(),
            App.Views.API:[]
        }
        app_data = App<<{
            App.AppName:data.AppName,
            App.Views:[view]
        }
        for api in data.API:
            view.API.append(
                App.Views.API<<{
                    App.Views.API.Name:api.name.lower(),
                    App.Views.API.RequirePrivilege:[k for k,v in  api.privileges.__dict__.items() if k[0:2]!="__" and k[k.__len__()-2:k.__len__()]!="__" and  v==True][0],
                    App.Views.API.Description:api.description
                }
            )
        ret,err,result = qr_insert.insert(app_data).commit()
        if err:
            raise err
    else:
        qr_find_index_of_view=qr.new().match(funcs.expr(App.AppName==data.AppName)).project(
            pymqr.docs.index_of_view<<funcs.indexOfArray(App.Views.ViewPath,data.Template.lower())
        )

        obj=qr_find_index_of_view.object
        if obj.index_of_view==-1 or obj.index_of_view == None:
            view=App.Views<<{
                App.Views.ViewPath:data.Template.lower(),
                App.Views.API:[],
                App.Views.Url:data.Url
            }
            for api in data.API:
                view.API.append(
                    App.Views.API << {
                        App.Views.API.Name: api.name.lower(),
                        App.Views.API.RequirePrivilege: [k for k, v in api.privileges.__dict__.items() if
                                                         k[0:2] != "__" and k[
                                                                            k.__len__() - 2:k.__len__()] != "__" and v == True][
                            0],
                        App.Views.API.Description: api.description
                    }
                )
            qr_push_view=qr.new().where(funcs.expr(App.AppName==data.AppName)).push({
                App.Views:view
            }).commit()
        else:
            for api in data.API:
                qr_find_index_of_view = qr.new().match(filters.AppName == data.AppName).match(
                    filters.Views(obj.index_of_view).ViewPath == data.Template.lower()
                ).project(
                    pymqr.docs.index_of_view << funcs.indexOfArray(App.Views.ViewPath, data.Template.lower()),
                    pymqr.docs.index_of_api<<funcs.indexOfArray(App.Views.API.Name,api.name.lower())
                )
                obj = qr_find_index_of_view.object
                if obj.index_of_api==-1:
                    push_api = App.Views.API << {
                        App.Views.API.Name: api.name.lower(),
                        App.Views.API.RequirePrivilege: [k for k, v in api.privileges.__dict__.items() if
                                                         k[0:2] != "__" and k[
                                                                            k.__len__() - 2:k.__len__()] != "__" and v == True][
                            0],
                        App.Views.API.Description: api.description
                    }
                    qr_push =qr.new().where(funcs.expr(App.AppName == data.AppName)).push({
                        App.Views(obj.index_of_view).API:push_api
                    }).commit()
                else:
                    update_api = App.Views.API << {
                        App.Views.API.Name: api.name.lower(),
                        App.Views.API.RequirePrivilege: [k for k, v in api.privileges.__dict__.items() if
                                                         k[0:2] != "__" and k[
                                                                            k.__len__() - 2:k.__len__()] != "__" and v == True][
                            0],
                        App.Views.API.Description:  api.__dict__.get("description","")
                    }
                    qr_update_api = qr.new().where(funcs.expr(App.AppName == data.AppName)).set({
                        App.Views(obj.index_of_view).API(obj.index_of_api): update_api
                    }).commit()


        # """
        # If app was found but not contains view push view into views of app
        # """
        # find_obj = qr.new().match(filters.AppName==data.AppName).match(
        #     filters.Views.ViewPath==data.Template
        # ).count().object
        # if find_obj.is_empty() or find_obj.ret==0:
        #     qr_update = qr.new().where(
        #         funcs.expr(
        #             App.AppName==data.AppName
        #         )
        #     )
        #     ret,err,result= qr_update.push({
        #         App.Views:App.Views<<dict(
        #             ViewPath=data.Template,
        #             Url=data.Url
        #         )
        #     }).commit()
        #     if err:
        #         raise err
        # else:
        #     pos = qr.new().match(filters.AppName==data.AppName).project(
        #         docs.posOfView<<funcs.indexOfArray(App.Views.ViewPath,data.Template)
        #     ).object
        #     x=pos







