'''
Created on 16.1.2013

@author: Sampo
'''
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import directory

app = Flask(__name__)
app.config.from_object("config")
database=SQLAlchemy(app)

login_mgr=LoginManager()
login_mgr.init_app(app)
login_mgr.login_view="login"
OID=OpenID(app,os.path.join(directory,"tmp"))

from app import views,models

if app.debug==False:
    import logging
    from logging.handlers import RotatingFileHandler
    handler=RotatingFileHandler("tmp/logfile.log","a",1*1024*1024,10)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
    app.logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info("!!!!!Startup!!!!!!")