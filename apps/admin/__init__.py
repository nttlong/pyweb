import routes
from flask import session
def auth():
    user = session.get("user",{})
    if user== {}:
        return False
    else:
        return user.get("IsSysAdmin",False)
