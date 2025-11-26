from flask import Flask,render_template,request,redirect,url_for

from flask_sqlalchemy import SqlAlchemy, SQLAlchemy
from telebot.apihelper import session

from werkzeug.security import generate_password_hash, check_password_hash

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

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            return "Такой логин уже используется"
        hash_password = generate_password_hash(password)

        new_user = User(username=username,password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        return redirect(url_for("task"))
    else:
        return render_template("index.html")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password,password):
            session["user_id"] = user.id
            return redirect(url_for("task"))
        else:
            return "Неверный логин или пароль"
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id",None)
    return redirect(url_for("index"))







