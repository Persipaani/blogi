'''
Created on 17.1.2013

@author: Sampo
'''
#Tells what database looks like

from app import database

type_user=0
type_admin=1

tags = database.Table("tags",
    database.Column("tag_id", database.Integer, database.ForeignKey("tag.id")),
    database.Column("post_id", database.Integer, database.ForeignKey("post.id"))
                     )

class Tag(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    tagname=database.Column(database.String(50),index=True)
    

class User(database.Model):
    id=database.Column(database.Integer,primary_key=True)
    nickname=database.Column(database.String(30),index=True,unique=True)
    email=database.Column(database.String(120),index=True,unique=True)
    type=database.Column(database.SmallInteger,default=0)
    info=database.Column(database.String(140))
    last_seen=database.Column(database.DateTime)
    posts=database.relationship("Post",backref="user",lazy="dynamic") #Tarkoittaa etta post.user viittaa tahan luokkaan
    
    
    def is_authenticated(self):
        #Returns True if authorized to authenticate
        return True
    
    def is_active(self):
        #User inactive if for example banned.
        return True
    
    def is_anonymous(self):
        #True if no login needed
        return False
    
    def get_id(self):
        return unicode(self.id)
    
    def __repr__(self):
        return "<User %r>" % (self.nickname)
    
    @staticmethod
    def create_uniq_nick(nickname):
        if User.query.filter_by(nickname=nickname).first()==None:
            return nickname
        version=2
        while True:
            new_nick=nickname+str(version)
            if len(new_nick)<=30:
                if User.query.filter_by(nickname=new_nick).first()==None:
                    return new_nick
                else:
                    version+=1
            else:
                new_nick=nickname[0:-3]
                return create_uniq_nick(new_nick)     
    
class Post(database.Model):
    id=database.Column(database.Integer,primary_key=True)
    title=database.Column(database.String(100),index=True,unique=False)
    body=database.Column(database.String(2500),index=True,unique=False)
    time=database.Column(database.DateTime)
    tags=database.relationship("Tag",secondary=tags,backref=database.backref("posts", lazy="dynamic"))
    user_id=database.Column(database.Integer,database.ForeignKey("user.id"))
    
    def __repr__(self):
        return "<Post %r>" % (self.body)
    
    def tag_post(self,tag):
        if self.is_tagget_with(tag)==False:
            self.tags.append(tag)
            return True
        return False
    
    def untag_post(self,tag):
        if self.is_tagget_with(tag)==True:
            self.tags.remove(tag)
            return True
        return False
        
    def is_tagget_with(self,tag):
        if self.tags.count(tag)==0:
            return False
        else:
            return True
    
    def create_tagstring(self):
        string=""
        for tag in self.tags:
            string+="," + str(tag.tagname)
        string=string[1:]
        return string
