# import settings
from flask import Flask
import os
from pfc import settings,xml2dict

app = Flask(__name__)
WORKING_DIR = os.getcwd()
config_path = os.sep.join([WORKING_DIR,'config/config.xml'])
config = xml2dict.load(config_path)
config.update({
    "WORKING_DIR":WORKING_DIR,
    "APP":app

})


settings.init(config)
from pymqr import settings as st,query
st.setdb(settings.db)
from pfc.controllers import get_list_of_controllers
from libs import memberships
lst = get_list_of_controllers()
for item in lst:
    memberships.register_view(
        AppName=item.app_name,
        Url = item.url,
        Template = item.template,
        API = item.methods
    )
from pfc import settings
from models.hr import emps
import libs.memberships.models_delete as FX
c=FX.Test.A.C<<{}
ret,err,result=emp = query(settings.db,emps.Emps).insert(
    emps.Emps<<{
        emps.Emps.Code:"A001",
        emps.Emps.FirstName:"Julia",
        emps.Emps.LastName:"Nguyen"
    }
).commit()

x=ret
# import routes
if __name__ == "__main__":

    settings.app.run(debug=True)