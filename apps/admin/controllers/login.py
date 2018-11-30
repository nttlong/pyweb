from libs.pyfy import controllers
import pymqr.mobject
from flask import session
from libs import memberships
@controllers.controller(
    url="/login",
    template = "login.html"
)
class Login(controllers.Controller):
    def OnPost(self,sender):
        ret = memberships.validate_user (self.request.form.to_dict ())
        if ret != None:
            memberships.SignIn (
                Session=session,
                User=ret,
                Language=sender.language)
            return self.redirect (sender.appUrl)
        else:
            self.data.error = sender.getAppRes ("Login fail!!!")

        data = self.request.data