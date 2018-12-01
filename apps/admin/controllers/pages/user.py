from pfc import controllers
from pymqr import documents
@documents.FormModel()
class __model_user__(object):
    def __init__(self):
        self.UserName= str,True
        self.Email = str, True
        self.Password = str, True
        self.IsActive = bool,True,False
        self.IsSysAdmin = bool,True,True
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
        ret= None
        from pyparams_validator import exceptions
        if sender.model.data==None:
            return self.Model<<{
                self.Model.message:sender._//"Please enter data",
                self.Model.isError:True
            }
        from libs import memberships
        try:
            ret= memberships.create_user(sender.model.data.__to_dict__())
        except exceptions.MissingFields as ex:
            x=ex.fields
        except memberships.exceptions.UserIsExist as ex:
            return self.Model<<{
                self.Model.isError:True,
                self.Model.message:sender._//"User is existing",
                self.Model.data :sender.model.data
            }
        except Exception as ex:
            raise ex

        return self.Model<<{
            self.Model.isError:False,
            self.Model.message:sender._//"Insert data is successfull",
            self.Model.data:ret
        }

