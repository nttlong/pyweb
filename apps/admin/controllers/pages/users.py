from pfc.controllers import controller,Controller,privileges
from libs import memberships
@controller(
    url="/views/users",
    template="pages/users.html"
)
class Users(Controller):
    privileges.View()
    def LoadUsers(self,data):
        ret= memberships.GetListOfUsers()
        return ret




