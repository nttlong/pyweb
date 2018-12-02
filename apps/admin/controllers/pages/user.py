from pfc import controllers
from pymqr import documents,errors

@documents.FormModel()
class __model_user__(object):
    def __init__(self):
        self.UserId = str,True,""
        self.UserName= str,True
        self.Email = str, True
        self.Password = str, True
        self.IsActive = bool,True,True
        self.IsSysAdmin = bool,True,False
        self.FirstName = str,True
        self.LastName = str, True
        self.Description =str
@documents.FormModel()
class __model__(object):
    def __init__(self):
        self.message=str,True
        self.data = __model_user__,True
        self.isError = bool,True


@controllers.controller(
    url="/views/user",
    template="pages/user.html"
)
class user(controllers.Controller):
    def __init__(self):
        self.Model = __model__
    def DoSaveUser(self,sender):
        from pymqr import query,filters,settings as st
        from pfc.models import model
        from libs import memberships
        from libs.memberships.models import users
        if isinstance(sender,model):
            if sender.model.data.UserId=="":
                try:
                    ret_user = memberships.create_user(
                        UserName = sender.model.UserName,
                        Email =sender.model.Email,
                        Password = sender.model.Password
                    )
                    return self.Model<<{
                        self.Model.isError:False,
                        self.Model.data:__model_user__<<{
                            __model_user__.UserId: ret_user.UserId,
                            __model_user__.Description:ret_user.Description,
                            __model_user__.LastName:ret_user.LastName,
                            __model_user__.FirstName:ret_user.FirstName,
                            __model_user__.IsActive:ret_user.IsActive,
                            __model_user__.IsSysAdmin:ret_user.IsSysAdmin,
                            __model_user__.Email:ret_user.Email
                        }
                    }
                except memberships.exceptions.UserIsExist as ex:
                    return self.Model<<{
                        self.Model.isError:True,
                        self.Model.message:sender._//"User is existing"
                    }
                except errors.DataException as ex:
                    if ex.error_type == errors.ErrorType.duplicate:
                        return self.Model << {
                            self.Model.isError: True,
                            self.Model.message: (sender._ // "The value of field '{0}' is existion").format (
                                ex.fields[0]
                            )
                        }
                except Exception as ex:
                    return self.Model << {
                        self.Model.isError: True,
                        self.Model.message: ex.message
                    }
            else:
                if sender.model.data.Password!="":
                    memberships.change_password(
                        Password=sender.model.data.Password,
                        UserName = sender.model.data.UserName
                    )
                ret,err,result =query(st.getdb(),users.Users)\
                    .where(filters.UserName==sender.model.data.UserName)\
                    .set({
                    users.Users.Description:sender.model.data.Description,
                    users.Users.Profile:{
                        users.Profile.FirstName:sender.model.data.FirstName,
                        users.Profile.LastName:sender.model.data.LastName
                    }
                }).commit()
                return self.Model<<{
                    self.Model.message:sender._//"Update is successfull",
                    self.Model.data:sender.model.data
                }

    def DoLoadItem(self,sender):
        from pfc.models import model
        from pymqr import query,settings as st,filters
        from libs.memberships.models import users
        if isinstance(sender,model):
            if sender.model.UserName=='*':
                return __model_user__<<{}
            else:
                qr =query(st.getdb(),users.Users)
                ret = qr.where(filters.UserName==sender.model.UserName).object
                return __model_user__<<{
                    __model_user__.UserId:ret._id,
                    __model_user__.UserName:ret.UserName,
                    __model_user__.Email:ret.Email,
                    __model_user__.IsSysAdmin:ret.IsSysAdmin,
                    __model_user__.IsActive:ret.IsActive,
                    __model_user__.Password:"",
                    __model_user__.FirstName:ret.Profile.FirstName,
                    __model_user__.LastName:ret.Profile.LastName,
                    __model_user__.Description: (lambda : ret.Description if hasattr(ret,"Description") else "")()

                }


