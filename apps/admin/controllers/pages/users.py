from pfc.controllers import controller,Controller
from pfc import JSON
@controller(
    url="/views/users",
    template="pages/users.html"
)
class Users(Controller):
    def LoadUsers(self,data):
        import datetime
        return dict(
            name = datetime.datetime.now()
        )

