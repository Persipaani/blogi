'''
Created on 16.1.2013

@author: Sampo
'''

#!flask/bin/python
from app import app
debug=0
if debug==1:
    app.run(debug = True) #Eli nayttaa debugviestit selaimessa, jos kaatuu
else:
    app.run(debug = False)