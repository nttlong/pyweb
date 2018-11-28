from libs.pyfy import controllers
@controllers(
    url="signout",
    template="signout"
)
class SignOut(controllers.Controller):
    def OnGet(self,sender,model):
        from libs import memberships
        memberships.SignOut (self.session)
        return self.redirect(sender.appUrl)


