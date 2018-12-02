from pfc import controllers
from pymqr import  documents
from pymqr import settings as st, query, funcs, docs,filters
from libs.memberships.models import roles
@documents.FormModel()
class ClientDataModel(object):
    def __init__(self):
        self.RoleId = str,True,None
        self.Code= str,True,"NA"
        self.Name = str,True
        self.FName =str,True
        self.Description = str

@documents.FormModel()
class ClientModel(object):
    def __init__(self):
        self.message = str
        self.isError = bool,True
        self.data = ClientDataModel,True

@controllers.controller(
    url="/views/role",
    template = "pages/role.html"
)
class role(controllers.Controller):
    def __init__(self):
        self.Model = ClientModel
    def OnGet(self,sender):
        sender.initModel =sender.toJSON((self.Model<<{
            self.Model.data:(ClientDataModel<<{}).to_dict()
        }).to_dict())
    def DoLoad(self,sender):

        if sender.model.code=="*":
            ret = ClientDataModel<<{

            }
            return ret
        else:
            qr = query(st.getdb(),roles.Roles)
            qr = qr.match(funcs.expr(roles.Roles.Code==sender.model.code))
            qr = qr.project(
                docs._id<<0,
                docs.RoleId<<docs._id,
                roles.Roles.Code,
                roles.Roles.FName,
                roles.Roles.Name,
                roles.Roles.Description
            )
            return qr.object

    def DoSave(self,sender):
        from libs import memberships
        if sender.model.RoleId=="":
            ret, err = memberships.create_role(sender.model.__to_dict__())
            sender.model.RoleId = ret["_id"]
            return sender.model
        else:
            ret,err,result =query(st.getdb(),roles.Roles).where(filters.Code==sender.model.Code).set({
                roles.Roles.Description: sender.model.Description,
                roles.Roles.Name: sender.model.Name,
                roles.Roles.FName: sender.model.FName
            }).commit()
            return sender.model

