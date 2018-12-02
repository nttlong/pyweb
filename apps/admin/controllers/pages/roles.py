from pymqr import documents
from pfc import controllers
@controllers.controller(
    url="/views/roles",
    template = "pages/roles.html"
)
class role_controller(controllers.Controller):
    def GetListOfRoles(self,sender):
        from pymqr import settings as st, query
        from libs.memberships.models import roles
        qr = query(st.getdb(),roles.Roles)
        return list(qr.items)
    pass