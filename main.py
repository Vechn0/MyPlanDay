from flask import Flask,render_template,request,redirect,url_for

from flask_sqlalchemy import SqlAlchemy, SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "YArikMasharskiAlexandrNeberoArtemFedoseev"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.integer,primary_key=True)
    username = db.Column(db.String(25),nullable=False,unique=True)
    password = db.Column(db.String(25),nullable=False,unique=True)
    tasks = db.relationship("Task",backref="user",lazy=True)


class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String,nullable=False)
    completed = db.Column(db.Boolean,default=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    def __repr__(self):
        return f"<Task {self.title}>"

with app.app_context():
    db.create_all()




