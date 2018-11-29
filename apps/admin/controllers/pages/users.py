from libs.pyfy.controllers import controller,Controller
@controller(
    url="/views/users",
    template="pages/users.html"
)
class Users(Controller):
    def LoadUsers(self,data):
        pass
