# import settings
from flask import Flask
import os
from libs.pyfy import settings
import libs.pyxml_dict
WORKING_DIR = os.getcwd()
config_path = os.sep.join([WORKING_DIR,'config/config.xml'])
config = libs.pyxml_dict.load(config_path)
config.update({
    "WORKING_DIR":WORKING_DIR
})

settings.init(config)
from pymqr import settings as st
st.setdb(settings.db)
# import routes
if __name__ == "__main__":

    settings.app.run(debug=True)