'''
Created on 17.1.2013

@author: Sampo
'''
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_CONT
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_CONT)
print "Current vers. " + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_CONT))