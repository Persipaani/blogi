'''
Created on 16.1.2013

@author: Sampo
'''

from flask import render_template,flash,redirect,session,url_for,request,g
from flask.ext.login import login_user,logout_user,current_user,login_required
from app import app,database,login_mgr,OID
from forms import LoginForm, EditForm, PostForm,PostEditForm,AdminForm
from models import User,Post,Tag,type_user,type_admin
from datetime import datetime
from config import posts_per_page

# g is place where Flask stores information from request

@login_mgr.user_loader
def load_user(id):
    return User.query.get(int(id))

#This runs always before view
@app.before_request
def before_request():
    g.user=current_user
    if g.user.is_authenticated()==True:
        g.user.last_seen=datetime.utcnow()
        database.session.add(g.user)
        database.session.commit()
 
@app.route("/", methods=["GET","POST"])
@app.route("/index", methods=["GET","POST"])
@app.route("/index/<int:page>", methods=["GET","POST"])
def index(page=1):
    
    form=PostForm()
    
    if form.validate_on_submit():
        
        taglist=form.create_taglist()
        
        post=Post(title=form.title.data,body=form.body.data,tags=taglist,time=datetime.utcnow(),user=g.user)
        database.session.add(post)
        database.session.commit()
                
        flash("Posted!")
        return redirect(url_for("index"))
    
    posts=Post.query.order_by(Post.time.desc())
    posts=posts.paginate(page,posts_per_page,False)
    
    return render_template("index.html", title="Homepage",form=form, posts=posts)

@app.route("/login",methods=['GET','POST'])
@OID.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for("index"))
    
    form=LoginForm()
    
    if form.validate_on_submit()==True:
        session["remember_me"]=form.remember_me.data
        return OID.try_login(form.openid.data,ask_for=["nickname","email"])
    return render_template('login.html', title="Login", form=form,providers=app.config["OPENID_PROVIDERS"])

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@OID.after_login
def after_login(resp):  #OID returns resp argument
    if resp.email==None or resp.email=="":
        flash("Invalid email")
        redirect(url_for("login"))
    
    user=User.query.filter_by(email=resp.email).first()
    if user==None: #If user not found, create new one.
        nickname=resp.nickname
        if nickname==None or nickname=="": #Not all OID providers give email
            nickname=resp.email.split("@")[0]
        nickname=User.create_uniq_nick(nickname)
        user=User(nickname=nickname,email=resp.email,type=type_user)
        database.session.add(user)
        database.session.commit()
    
    remember_user=False
    if "remember_me" in session: #Tosi jos sessionissa on jossain kohdassa sana remember me, tassa tapauksessa kohdassa "remember me"
        remember_user=session["remember_me"] #asettaa remeber:me -arvon True:ksi
        session.pop("remember_me",None)
    
    login_user(user,remember=remember_user)
    return redirect(request.args.get("next") or url_for("index"))#Goes to where user wanted or index


@app.route("/user/<nickname>")
@app.route("/user/<nickname>/<int:page>")
@login_required
def user(nickname,page=1):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash(nickname + ' not found.')
        return redirect(url_for('index'))
    
    posts=Post.query.filter_by(user_id=user.id).order_by(Post.time.desc())
    posts=posts.paginate(page,posts_per_page,False)
    
    return render_template('user.html',user = user,posts = posts)
    
 
@app.route("/message/<id>",methods=["GET","POST"])
def message(id):
    post = Post.query.filter_by(id = id).first()
    if post == None:
        flash("post" + id + ' not found.')
        return redirect(url_for('index'))
    
    return render_template('message.html',post = post)

@app.route("/edit",methods=["GET","POST"])
@login_required
def edit():
    form=EditForm(g.user.nickname)
    if form.validate_on_submit()==True:  #Jos on painettu Save ja formin tiedot toimii!
        g.user.nickname=form.nickname.data
        g.user.info=form.info.data
        database.session.add(g.user)
        database.session.commit()
        flash("Changes saved!")
        #return redirect(url_for("edit"))
        posts=g.user.posts.all()
        return render_template('user.html',title="Edit User Details",user = g.user,posts = posts)

    else:
        form.nickname.data=g.user.nickname
        form.info.data=g.user.info
        if form.not_valid_nick==True:
            form.info.data=form.info.data
        else:
            form.info.data=g.user.info
        
    return render_template("edit.html",form=form)

@app.route("/edit_post/<id>",methods=["GET","POST"])
@login_required
def edit_post(id):
    form=PostEditForm(request.form)
    post = Post.query.filter_by(id = id).first()
    choices=[]
    
    if request.method=="GET" or request.method=="POST":
        tags=Tag.query.all()
        for tag in tags:
            choices.append((tag.tagname,tag.tagname))
        form.tags.choices=choices
        
    if form.validate_on_submit()==True:
        delete_post=form.delete.data
        
        if delete_post==True:
            database.session.delete(post)
            database.session.commit()
            return redirect(url_for("index"))
        
        post.title=form.title.data
        post.body=form.body.data
        taglist=form.create_taglist()
        post.tags=taglist
        database.session.add(post)
        database.session.commit()
        return render_template('message.html',post = post)
    else:
        form.title.data=post.title
        form.body.data=post.body
        tagstring=post.create_tagstring()
        form.tags.data=tagstring
    
    return render_template('edit_post.html',title="Edit Post",form=form,post=post)

@app.route("/admin_page",methods=["GET","POST"])
@login_required
def admin():
    form=AdminForm(request.form)
    users=User.query.all()
    choices=[]
    
    if request.method=="GET" or request.method=="POST":
        tags=Tag.query.all()
        for tag in tags:
            choices.append((tag.tagname,tag.tagname))
        form.tags.choices=choices
    
    if form.validate_on_submit()==True:
        
        if form.add_new_admins()==True:
            flash("Users [" + str(form.newadmins.data) + "] added to admins!")
        
        if form.remove_admins()==True:
            flash("Users [" + str(form.oldadmins.data) + "] removed from admins!")
        
        if form.remove_tags()==True:
            flash("Tags [" + str(form.tags.data) + "] removed!")   
        
        #Nollataan kaikki submitin jalkeen:
        form.oldadmins.data=""
        form.newadmins.data=""
        choices=[]
        tags=Tag.query.all()
        for tag in tags:
            choices.append((tag.tagname,tag.tagname))
        form.tags.choices=choices
    
    return render_template('admin_page.html',title="Admin Options",form=form,users=users)

#Error handlers:

@app.errorhandler(404)
def internal_error(error):
    return render_template("error_404.html",title="!404!",),404

@app.errorhandler(500)
def internal_error(error):
    database.session.rollback()
    return render_template("error_500.html",title="!500!",),500
    
