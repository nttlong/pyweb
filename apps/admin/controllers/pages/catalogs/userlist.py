from pfc.controllers import Controller,controller,privileges
from pfc.models import model

from libs.memberships.models import User
from pymqr import filters,query, settings as st,docs
from pymqr.documents import FormModel
@FormModel()
class __form__(object):
    def __init__(self):
        self.pageSize = int,True,50
        self.pageIndex = int,True,0
        self.totalPages = int,True,0
        self.totalItems = int,True,0
        self.items = [object],True,[]
@controller(
    url="/views/catalogs/users",
    template="pages/catalogs/users.html"
)

class UsersController(Controller):
    def __init__(self):
        self.Model = __form__

    @privileges.View()
    def LoadItems(self,sender):
        """Get lis of employee including: UserName,Email,FirstName and LastName"""

        if isinstance(sender,model):
            params = self.Model<<sender.model.__dict__
            ret = query(st.getdb(),users.Users).match(
                filters.IsActive==True
            ).project(
                users.Users.UserName,
                users.Users.Email,
                docs.FirstName<<users.Users.Profile.FirstName,
                docs.LasName<<users.Users.Profile.LastName
            ).sort(
                users.Users.UserName.asc()
            ).get_page(params.pageSize,params.pageIndex)
            return self.Model<<{
                self.Model.pageSize:ret.page_size,
                self.Model.pageIndex:ret.page_index,
                self.Model.totalItems:ret.total_items,
                self.Model.totalPages:ret.total_pages,
                self.Model.items:ret.items
            }





