from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key"

#Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


#DB Module
class User(db.Model):
    #class Variables
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Textify(db.Model):
    id=db.Column(db.Integer,unique=True,primary_key=True)
    text=db.Column(db.String(25),nullable=False)

#Routes
@app.route("/")
def home():
    if "username" in session:
        tasks = Textify.query.all()
        return render_template("home.html", username=session['username'], tasks=tasks)
    return render_template("welcoming.html")
    
#Login
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    #Collect info from the form
    username = request.form["username"]
    password = request.form["password"]
    
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session["username"] = username
        return redirect(url_for("home"))
    else:
        return render_template("login.html", error="Invalid username or password!")
    
    
#Register
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("register.html", error="Username already exists!")
    else:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = username
        return redirect(url_for("home"))


#Logout
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))
    
    
    
    
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    text=request.form['text']
    new_item = Textify(text=text)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/')
def update():
    return render_template('update.html')


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    item = Textify.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('home'))
    
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000, host="0.0.0.0")