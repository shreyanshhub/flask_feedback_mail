from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message


app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mail.sqlite3"
app.secret_key = "new"

db = SQLAlchemy(app)

mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
app.config['MAIL_PASSWORD'] = 'yourpassword'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


class User(db.Model):

    id = db.Column("id",db.Integer,primary_key=True)
    username = db.Column("username",db.String(100))
    password = db.Column("password",db.String(100))
    contents = db.relationship("Content",backref="content")

class Content(db.Model):

    id = db.Column("id",db.Integer,primary_key=True)
    content_id = db.Column("content_id",db.ForeignKey("user.id"))
    first_name = db.Column("first_name",db.String(100))
    last_name = db.Column("last_name",db.String(100))
    email = db.Column("email",db.String(100))
    t_shirt_color = db.Column("color",db.String(100))

@app.route('/',methods=["GET","POST"])
def home():
    return render_template("index.html")

@app.route("/register",methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user:

            flash("Username already exists")
            return render_template("register.html")

        else:

            user = User(username=username,password=password)

            session["username"] = username
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("dashboard"))

    if "username" in session:
        flash("User is already registered and logged in")
        return redirect(url_for("dashboard"))

    return render_template("register.html")


@app.route("/login",methods=["GET","POST"])
def login():

    if request.method == 'POST':

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username,password=password).first()

        if user:
            flash("user already logged in ")

            session["username"] = username

        else:
            flash("Incorrect username or password")
            return render_template("login.html")

    if "username" in session:
        flash("User is already logged in")
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/logout",methods=["GET","POST"])
def logout():

    if "username" in session:

        session.pop("username",None)
        return redirect(url_for("login"))

    return redirect(url_for("login"))

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():

    if request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        t_shirt_color = request.form["t_shirt_color"]

        username = session["username"]
        user = User.query.filter_by(username=username).first()
        content = Content(first_name=first_name,last_name=last_name,email=email,t_shirt_color=t_shirt_color)

        db.session.add(content)
        db.session.commit()


        msg = Message(
                'Hello',
                sender ='paramguy18@gmail.com',
                recipients = [str(email)]
               )
        msg.body = "Hi " + str(first_name) +","+'Your response has been recorded.' + " Your feedback is: \n" +str(t_shirt_color)+" \n We will keep you updated on your feedback.Thank you"
        mail.send(msg)

        return render_template("logout.html")

    if "username" in session:
        user = User.query.filter_by(username=session["username"]).first()
        return render_template("dashboard.html",user=user)

    else:
        return redirect(url_for("login"))

if __name__ == "__main__":

    with app.app_context():

        db.create_all()
        app.run(debug=True)
