from pfc import controllers
from pymqr import documents
class __model__(documents.BaseDocuments):
    def __init__(self):
        self.message=str,True
        self.data = object,True
        self.isError = bool,True


@controllers.controller(
    url="/views/user",
    template="pages/user.html"
)
class user(controllers.Controller):
    def __init__(self):
        self.Model = __model__
    def DoSaveUser(self,sender):
        from pyparams_validator import exceptions
        if sender.params.__is_emty__():
            return dict(
                message=sender._//"Please enter data"
            )
        from libs import memberships
        try:
            ret= memberships.create_user(sender.params.__to_dict__())
        except exceptions.MissingFields as ex:
            x=ex.fields
        except Exception as ex:
            raise ex

        return self.Model<<{
            self.Model.isError:False,
            self.Model.message:sender._//"Insert data is successfull",
            self.Model.data:ret
        }

