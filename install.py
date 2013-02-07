'''
Created on Feb 7, 2013

@author: Sampo
'''
from create_db import CreateDB
try:
    new_db=CreateDB()
except:
    print "Database Already created."

from app import app
debug=0
if debug==1:
    app.run(debug = True) #Eli nayttaa debugviestit selaimessa, jos kaatuu
else:
    app.run(debug = False)