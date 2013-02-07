'''
Created on 16.1.2013

@author: Sampo
'''
#Configuring database path and etc.

import os
directory=os.path.abspath(os.path.dirname(__file__))
posts_per_page=3

password=""
SQLALCHEMY_DATABASE_URI="postgresql://postgres:"+password+"@localhost:5432/database"
SQLALCHEMY_MIGRATE_CONT=os.path.join(directory,"database_container")

CSRF_ENABLED=True
SECRET_KEY="turvallinen_salasana"

OPENID_PROVIDERS = [{"name":"Google","url":"https://www.google.com/accounts/o8/id"},{"name":"MyOpenID","url":"https://www.myopenid.com"}]