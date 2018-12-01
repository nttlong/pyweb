# import settings
from flask import Flask
import os
from pfc import settings,xml2dict


WORKING_DIR = os.getcwd()
config_path = os.sep.join([WORKING_DIR,'config/config.xml'])
config = xml2dict.load(config_path)
config.update({
    "WORKING_DIR":WORKING_DIR,
    "APP":Flask(__name__)

})

settings.init(config)
from pymqr import settings as st
st.setdb(settings.db)
# import routes
if __name__ == "__main__":

    settings.app.run(debug=True)