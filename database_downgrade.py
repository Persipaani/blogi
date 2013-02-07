'''
Created on 17.1.2013

@author: Sampo
'''
#Deupdates database
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_CONT

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_CONT)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_CONT, v - 1)
print "Current vers. " + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_CONT))