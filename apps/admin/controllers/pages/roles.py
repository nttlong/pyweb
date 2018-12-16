from pymqr import documents
from pfc import controllers
@controllers.controller(
    url="/views/roles",
    template = "pages/roles.html"
)
class role_controller(controllers.Controller):
    controllers.privileges.View()
    def GetListOfRoles(self,sender):
        from pymqr import settings as st, query
        from libs.memberships import models
        qr = query(st.getdb(),models.Role)
        return list(qr.items)
    pass