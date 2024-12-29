from flask import Flask,render_template,request,session
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy



import json


with open('config.json','r') as c:
    params=json.load(c)['params']



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/blog"

db = SQLAlchemy(app)

class Contact(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(120),primary_key=False,nullable=False,unique=False)
    email=db.Column(db.String(120),primary_key=False,nullable=False,unique=True)
    phone_num=db.Column(db.String(120),primary_key=False,nullable=False,unique=True)
    message=db.Column(db.String(120),primary_key=False,nullable=False,unique=False)



   



@app.route("/")
def home():
    return render_template("index.html",params=params)


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



@app.route("/post")
def post():
    return render_template("post.html",params=params)



app.run(debug=True)