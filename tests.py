'''
Created on 28.1.2013

@author: Sampo
'''

#!flask/bin/python
import unittest
import datetime,time

from config import directory
from app import app,database
from app.models import User,Post,Tag
from app.forms import PostEditForm

class TestCase(unittest.TestCase):
    
    def setUp(self):
        app.config["TESTING"]=True
        app.config["CSRF_ENABLED"]=False
        app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:Gravita9.81@localhost:5432/database"
        self.app=app.test_client()
        database.create_all()
        
    def tearDown(self):
        database.session.remove()
        database.drop_all()
    
    def test_unique_nick(self):
        user=User(nickname="sampo",email="sampo@sampomail.org",info="lol")
        database.session.add(user)
        database.session.commit()
        nickname=User.create_uniq_nick("sampo")
        assert nickname!="sampo"
        
        user = User(nickname = nickname, email = 'samuela@supermail.fi',info="lul")
        database.session.add(user)
        database.session.commit()
        nickname2 = User.create_uniq_nick('sampo')
        assert nickname2 != 'sampo'
        assert nickname2 != nickname
    
    def test_post_add(self):
        user=User(nickname="sampo",email="sampo@sampomail.org",info="lol")
        database.session.add(user)
        database.session.commit()
        
        post=Post(title="testiposti",body="olipa kerran kalkkunakeitto",time=datetime.datetime.utcnow(),user=user)
        database.session.add(post)
        database.session.commit()
        
        assert user.posts.all()[0].title == "testiposti"
    
    def test_post_returning(self):
        user=User(nickname="sampo",email="sampo@sampomail.org",info="lol")
        database.session.add(user)
        database.session.commit()
        
        user2=User(nickname="jonne",email="silli@sampomail.org",info="lol")
        database.session.add(user)
        database.session.commit()
        
        post=Post(title="testiposti",body="olipa kerran kalkkunakeitto",time=datetime.datetime.utcnow(),user=user)
        database.session.add(post)
        database.session.commit()
        
        time.sleep(2)
        
        post2=Post(title="testiposti222222222",body="Siilit jyraa liigassa!",time=datetime.datetime.utcnow(),user=user2)
        database.session.add(post2)
        database.session.commit()
        
        assert Post.query.order_by(Post.time.desc()).all()[0].title == "testiposti222222222"
    
    def test_tagging(self):
        user=User(nickname="sampo",email="sampo@sampomail.org",info="lol")
        database.session.add(user)
        database.session.commit()
        
        tag=Tag(tagname="kissoja")
        tag2=Tag(tagname="koiria")
        
        post=Post(title="testiposti",body="olipa kerran kalkkunakeitto",time=datetime.datetime.utcnow(),user=user)
        database.session.add(post)
        database.session.commit()
        
        #Postauksen voi tagata:
        post.tag_post(tag)
        assert Post.query.filter_by(id="1").first().tags[0].tagname=="kissoja"
        
        #Postausta ei voi uudelleentagata samalla tagilla:
        post.tag_post(tag)
        assert len(Post.query.filter_by(id="1").first().tags)==1
        
        #Olematonta tagia ei voi poistaa:
        assert post.untag_post(tag2)==False
        assert len(Post.query.filter_by(id="1").first().tags)==1
        
        #Olevan tagin sensijaan voi:
        assert post.untag_post(tag)==True
        assert len(Post.query.filter_by(id="1").first().tags)==0
        
        
if __name__=="__main__":
    unittest.main()

        