from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

# Opprett Flask-applikasjon
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Konfigurer SQLAlchemy database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Database modeller
class User(db.Model):
    """Brukermodell for autentisering"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Textify(db.Model):
    """Modell for oppgaver/notater"""
    id = db.Column(db.Integer, unique=True, primary_key=True)
    text = db.Column(db.String(25), nullable=False)

# Ruter
@app.route("/")
def home():
    """Hjemmeside - viser oppgaver hvis bruker er logget inn"""
    if "username" in session:
        tasks = Textify.query.all()
        return render_template("home.html", username=session['username'], tasks=tasks)
    return render_template("welcoming.html")
    
# Innlogging
@app.route("/login", methods=["POST", "GET"])
def login():
    """Håndter brukerinnlogging"""
    if request.method == "GET":
        return render_template("login.html")
    
    # Hent data fra skjema
    username = request.form["username"]
    password = request.form["password"]
    
    # Valider bruker
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session["username"] = username
        return redirect(url_for("home"))
    else:
        return render_template("login.html", error="Invalid username or password!")
    
    
# Registrering
@app.route("/register", methods=["POST", "GET"])
def register():
    """Håndter brukerregistrering"""
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form["username"]
    password = request.form["password"]
    
    # Sjekk om bruker allerede eksisterer
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("register.html", error="Username already exists!")
    else:
        # Opprett ny bruker
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = username
        return redirect(url_for("home"))


# Logg ut
@app.route("/logout")
def logout():
    """Logg ut brukeren fra sesjonen"""
    session.pop('username', None)
    return redirect(url_for('home'))
    
    
# Opprett ny oppgave
@app.route('/create', methods=['GET', 'POST'])
def create():
    """Opprett ny oppgave/notat"""
    if request.method == 'GET':
        return render_template('create.html')
    
    # Lagre ny oppgave i databasen
    text = request.form['text']
    new_item = Textify(text=text)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('home'))


# Slett oppgave
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Slett en oppgave fra databasen"""
    item = Textify.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('home'))
    
    
if __name__ == "__main__":
    # Opprett alle databasetabeller
    with app.app_context():
        db.create_all()
    # Start Flask-serveren
    app.run(debug=True, port=5000, host="0.0.0.0")