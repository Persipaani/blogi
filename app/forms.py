'''
Created on 16.1.2013

@author: Sampo
'''
from flask import request
from flask.ext.wtf import Form, TextField, BooleanField,TextAreaField,SelectMultipleField,widgets
from flask.ext.wtf import Required,Length #Asettaa kentan maaritteet
from app.models import User,Tag
from app import database

class LoginForm(Form):
    openid=TextField("openid",validators=[Required()])
    remember_me=BooleanField("remember_me",default=False)

class EditForm(Form):
    nickname=TextField("nickname",validators=[Required(),Length(min=0,max=30)])
    info=TextAreaField("info",validators=[Length(min=0,max=140)])
    not_valid_nick=False
    
    def __init__(self,original_nick,*args,**kwargs):
        Form.__init__(self,*args,**kwargs)
        self.original_nick=original_nick
    
    def validate(self):
        not_valid_nick=False
        if Form.validate(self)==False:
            return False
        if self.nickname.data==self.original_nick:
            return True
        user=User.query.filter_by(nickname=self.nickname.data).first()
        if user!=None:
            self.nickname.errors.append("Nickname you typed is already taken! Choose another.")
            self.not_valid_nick=True
            return False
        
        return True
class PostForm(Form):
    body=TextAreaField("body",validators=[Length(min=0,max=2500)])
    title=TextField("title",validators=[Required(),Length(min=1,max=100)])
    tags=TextField("tags",validators=[Length(min=0,max=100)])
    delete=BooleanField("delete",default=False)
    
    def create_taglist(self):
        #Create new tags from names if not already there.
        #If tag already exists, add to list.
        #Tag is not created if it's name is empty,for example too many ","
        taglist=[]
        tagnames=self.tags.data.split(",")
        for name in tagnames:
            if Tag.query.filter_by(tagname=name).first()==None:
                name=name.replace(" ","")
                if name!="" and len(name)<=100:
                    newtag=Tag(tagname=name)
                    taglist.append(newtag)
            else:
                taglist.append(Tag.query.filter_by(tagname=name).first())
        return taglist

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PostEditForm(Form):
    tags=MultiCheckboxField("Tags",choices=[])
    body=TextAreaField("body",validators=[Length(min=0,max=2500)])
    title=TextField("title",validators=[Required(),Length(min=1,max=100)])
    delete=BooleanField("delete",default=False)
    newtags=TextField("title",validators=[Length(min=0,max=100)])
    
    def create_taglist(self):
        #If tag already exists, add to list.
        taglist=[]
        tagnames=self.tags.data
        for name in tagnames:
            taglist.append(Tag.query.filter_by(tagname=name).first())
            
        #Create new tags from names:
        #Tag is not created if it's name is empty,for example too many ","
        #If user types existing tag, do not duplicate.
        if self.newtags!="":
            tagnames=self.newtags.data.split(",")
            for name in tagnames:
                if Tag.query.filter_by(tagname=name).first()==None:
                    name=name.replace(" ","")
                    if name!="":
                        newtag=Tag(tagname=name)
                        taglist.append(newtag)
                else:
                    taglist.append(Tag.query.filter_by(tagname=name).first())

        return taglist

class AdminForm(Form):
    tags=MultiCheckboxField("Tags",choices=[])
    newadmins=TextField("newadmins")
    oldadmins=TextField("oldadmins")
    
    def add_new_admins(self):
        value=False
        if self.newadmins.data!="":
            newadmins=self.newadmins.data.split(",")
            for number in newadmins:
                number=number.replace(" ","")
                if self.is_number(number)!=False:
                    number=int(number)
                    user=User.query.filter_by(id=number).first()
                    if user!=None and user.type!=1:
                        user.type=1
                        database.session.add(user)
                        database.session.commit()
                        value=True
        return value
    
    def remove_admins(self):
        value=False
        if self.oldadmins.data!="":
            oldadmins=self.oldadmins.data.split(",")
            for number in oldadmins:
                number=number.replace(" ","")
                if self.is_number(number)!=False:
                    number=int(number)
                    user=User.query.filter_by(id=number).first()
                    if user!=None and user.type!=0:
                        user.type=0
                        database.session.add(user)
                        database.session.commit()
                        value=True
        return value
    
    def remove_tags(self):
        value=False
        for tag in self.tags.data:
            removed_tag=Tag.query.filter_by(tagname=tag).first()
            if removed_tag!=None:
                database.session.delete(removed_tag)
                database.session.commit()
                value=True
        return value
    
    def is_number(self,number):
        try:
            float(number)
            return True
        except ValueError:
            return False
            
