from libs.pyfy import controllers
@controllers.controller(
    url="/signout",
    template="signout"
)
class SignOut(controllers.Controller):
    def OnGet(self,sender):
        from libs import memberships
        memberships.SignOut (self.session)
        return self.redirect(sender.appUrl)


