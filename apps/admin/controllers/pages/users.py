from pfc.controllers import controller,Controller
from libs import memberships
@controller(
    url="/views/users",
    template="pages/users.html"
)
class Users(Controller):
    def LoadUsers(self,data):
        ret= memberships.GetListOfUsers()
        return ret




