from pfc import controllers
from pymqr import  documents
from pymqr import settings as st, query, funcs, docs,filters
from libs.memberships.models import roles,users
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
        """
        Init controller
        """
        self.Model = ClientModel
    def OnGet(self,sender):
        """
        On Get
        :param sender:
        :return:
        """
        sender.initModel =sender.toJSON((self.Model<<{
            self.Model.data:(ClientDataModel<<{}).to_dict()
        }).to_dict())
    def DoLoad(self,sender):
        """
        Load user
        :param sender:
        :return:
        """

        if sender.model.code=="*":
            ret = ClientDataModel<<{

            }
            return ret
        else:
            qrUser =query(st.getdb(),users.Users)
            qr = query(st.getdb(),roles.Roles)

            qr = qr.match(funcs.expr(roles.Roles.Code==sender.model.code))
            qr = qr.project(
                docs._id<<0,
                docs.RoleId<<docs._id,
                roles.Roles.Code,
                roles.Roles.FName,
                roles.Roles.Name,
                roles.Roles.Description,
                roles.Roles.Users
            ).lookup(
                users.Users,
                roles.Roles.Users,
                users.Users.UserName,
                docs.Users

            ).project(
                docs.RoleId,
                roles.Roles.Code,
                roles.Roles.FName,
                roles.Roles.Name,
                roles.Roles.Description,
                roles.Roles.Users<<funcs.map(
                    docs.Users,(
                        users.Users.UserName<<docs.userItem.var().UserName,
                        users.Users.Email<<docs.userItem.var().Email,
                        users.Users.IsSysAdmin<<docs.userItem.var().IsSysAdmin,
                        users.Profile.FirstName<<docs.userItem.var().Profile.FirstName,
                        users.Profile.LastName << docs.userItem.var ().Profile.LastName,

                    ),docs.userItem)
            )

            return qr.object

    def DoSave(self,sender):
        """

        :param sender:
        :return:
        """
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
    def DoAddUsers(self,sender):
        entity = query(st.getdb(),roles.Roles).where(filters.Code==sender.model.code)
        for item in sender.model.users:
            ret,err,reult= entity.push({
                roles.Roles.Users: item.UserName
            }).commit()
            print item
        return {}

