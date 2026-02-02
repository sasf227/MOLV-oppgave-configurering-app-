from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "your_secret_key"

#Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


#DB Module
class User(db.Model):
    #class Variables
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)



#Routes
@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html", username=session['username'])
    return render_template("welcoming.html")
    
#Login
@app.route("/login", methods=["POST"])
def login():
    #Collect info from the form
    username = request.form["username"]
    password = request.form["password"]
    
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session["username"] = username
        return redirect(url_for("home"))
    else:
        pass
    

    
#Register
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("index.html", error="This user already exist!")
    else:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = username
        return redirect(url_for("dashboard"))
    
#Dashboard
@app.route("/welcoming")
def dashboard():
    if "username" in session:
        return render_template("welcoming.html", username=session['username'])
    return redirect(url_for('home'))


#Logout
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))
    
    
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)