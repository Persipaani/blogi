'''
Created on 18.1.2013

@author: Sampo
'''
from app import database,models
import datetime

class UseDatabase(object):
    
    def __init__(self):
        print "initialized"
    
    def add_user(self,nick,email,type):
        user=models.User(nick=nick,email=email,type=type)
        database.session.add(user)
        database.session.commit()
        
    def add_post(self,title,msg,user):
        post=models.Post(title=title,body=msg,time=datetime.datetime.utcnow(),user=user)
        database.session.add(post)
        database.session.commit()
        
    def return_posts_from(self,user):
        return user.posts.all()
    
    def return_posts(self):
        return models.Post.query.all()
    
    def return_users(self):
        return models.User.query.all()
    
    def print_userdata(self):
        users= models.User.query.all()
        for user in users:
            print "id: " + str(user.id) + " nick: " + str(user.nick)
    
    def remove_users(self):
        users=models.User.query.all()
        for user in users:
            database.session.delete(user)
            database.session.commit()
    
    def remove_posts(self):
        posts=models.Post.query.all()
        for post in posts:
            database.session.delete(post)
            database.session.commit()
            
    

DB=UseDatabase()
#change.add_user("Sampo", "sampo.sampo@sampo.sampo", 0)
#database.add_user("Eric", "eric@hotmale.eric", 0)

#users = DB.return_users()
DB.print_userdata()

#DB.add_post("Hello World","Tama on ensimmainen postaus",users[0])

#DB.remove_users()
#DB.remove_posts()

print DB.return_users()

print DB.return_posts()
