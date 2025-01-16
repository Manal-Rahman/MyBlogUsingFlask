from flask import Flask,render_template,request,session,redirect
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


import json


with open('config.json','r') as c:
    params=json.load(c)['params']



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/blog"
app.secret_key = 'super secret key'
db = SQLAlchemy(app)            

class Contact(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(120),primary_key=False,nullable=False,unique=False)
    email=db.Column(db.String(120),primary_key=False,nullable=False,unique=True)
    phone_num=db.Column(db.String(120),primary_key=False,nullable=False,unique=True)
    message=db.Column(db.String(120),primary_key=False,nullable=False,unique=False)


class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    slug=db.Column(db.String(120),primary_key=False,nullable=False,unique=False)
    heading=db.Column(db.String(120),primary_key=False,nullable=False,unique=False)
    tagline=db.Column(db.String(120),primary_key=False,nullable=False,unique=False)
    data=db.Column(db.String(120),primary_key=False,nullable=False,unique=False)
    date = db.Column(db.String(12),  nullable=True)
    # date=db.Column(db.String(120),primary_key=False,nullable=False,unique=False)



   



@app.route("/")
def home():
    posts = Post.query.filter_by().all()
    return render_template("index.html",params=params,posts=posts)


@app.route("/contact",methods=["GET","POST"])
def contact():
    if(request.method=="POST"):
        name=request.form.get("name")
        email=request.form.get("email")
        phone_num=request.form.get("phone_num")
        message=request.form.get("message")
        entry = Contact(name=name,email=email,phone_num=phone_num,message=message)
        db.session.add(entry)
        db.session.commit()







    return render_template("contact.html",params=params)


@app.route("/about")
def about():
    return render_template("about.html",params=params)



@app.route("/post/<string:slug>",methods=["GET"])
def post(slug):
    post = Post.query.filter_by(slug=slug).first()
    return render_template("post.html",params=params,slug=slug,post=post)
   


# ===================== Login Page ============


@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
        if ('user' in session and session ['user'] == params['email']):
            posts=Post.query.all()
            return render_template('dashboard.html',params=params,posts=posts)
        
    
        if request.method=='POST':
            username = request.form.get('email')
            userpass = request.form.get('pass')
            if (username == params['email'] and userpass == params['pass']):
                #set the session variable
                session['user']= username
                posts=Post.query.all()
                return render_template('dashboard.html',params=params,posts=posts)
            
            
        
    
        return render_template('login.html',params=params)
        
    

@app.route("/logout")
def logout():
    
    session.pop('user')
    return redirect('/dashboard')



# ========================= Delete Post ===========
@app.route("/delete/<string:id>",methods=['GET',"POST"])
def delete(id):
    if ('user' in session and session ['user'] == params['email']):
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
    
    # session.pop('user')
    return redirect('/dashboard')


# @app.route("/editt")
# def edit():
#     if ('user' in session and session ['user'] == params['email']):
#         post = Post.query.filter_by().first()
#     return render_template("edit.html",params=params,post=post)



@app.route("/edit/<string:id>",  methods = ['GET','POST'])
def edit(id):
    if ('user' in session and session ['user'] == params['email']):
        if request.method=='POST':
            heading = request.form.get('heading')
            tagline = request.form.get('tagline')

            slug = request.form.get('slug')
            data = request.form.get('data')
            date=datetime.now()

            
            # if id == "0":
            #     post= Posts(title=box_title,slug=slug,content=content,tagline=tagline,date=date)
            #     db.session.add(post)
            #     db.session.commit()
                
            if(id==id):
                post=Post.query.filter_by(id=id).first()
                post.heading=heading
                post.tagline=tagline
                post.slug=slug
                post.data=data
                post.date=date
                db.session.commit()
                return redirect('/dashboard')
        post=Post.query.filter_by(id=id).first()
                
        return render_template('edit.html',params=params,post=post)




app.run(debug=True)