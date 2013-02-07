'''
Created on 17.1.2013

@author: Sampo
'''
#Creates new database so that you can later migrate it with newer versions.
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_CONT
from app import database
import os.path

class CreateDB(object):
    def __init__(self):
        database.create_all()
        
        if not os.path.exists(SQLALCHEMY_MIGRATE_CONT):
            api.create(SQLALCHEMY_MIGRATE_CONT,"database container")
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_CONT)
        else:
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_CONT, api.version(SQLALCHEMY_MIGRATE_CONT))
