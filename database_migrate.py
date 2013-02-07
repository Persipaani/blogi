'''
Created on 17.1.2013

@author: Sampo
'''
#Updates database
import imp
from migrate.versioning import api
from app import database
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_CONT

migration=SQLALCHEMY_MIGRATE_CONT+"/versions/%03d_migration.py" % (api.db_version(SQLALCHEMY_DATABASE_URI,SQLALCHEMY_MIGRATE_CONT)+1)
tmp_module=imp.new_module("old_model")
old_model=api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_CONT)
exec old_model in tmp_module.__dict__
script=api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_CONT, tmp_module.meta, database.metadata)
open(migration,"wt").write(script)
a=api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_CONT)

print "Saved as"+migration
print "Current vers. "+str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_CONT))