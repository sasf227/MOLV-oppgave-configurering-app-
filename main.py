from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

# Opprett Flask-applikasjon
app = Flask(__name__)
app.secret_key = "din_hemmelige_nøkkel"

# Konfigurer SQLAlchemy database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Bruker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Database modeller
class Bruker(db.Model):
    """Brukermodell for autentisering"""
    id = db.Column(db.Integer, primary_key=True)
    brukernavn = db.Column(db.String(25), unique=True, nullable=False)
    passord = db.Column(db.String(200), nullable=False)

class Oppgave(db.Model):
    """Modell for oppgaver/notater"""
    id = db.Column(db.Integer, unique=True, primary_key=True)
    tekst = db.Column(db.String(25), nullable=False)
    

# Ruter
@app.route("/")
def hjem():
    """Hjemmeside - viser oppgaver hvis bruker er logget inn"""
    if "brukernavn" in session:
        oppgaver = Oppgave.query.all()
        return render_template("hjem.html", brukernavn=session['brukernavn'], oppgaver=oppgaver)
    return render_template("velkommen.html")
    
# Innlogging
@app.route("/login", methods=["POST", "GET"])
def login():
    """Håndter brukerinnlogging"""
    if request.method == "GET":
        return render_template("login.html")
    
    # Hent data fra skjema
    brukernavn = request.form["brukernavn"]
    passord = request.form["passord"]
    
    # Valider bruker
    bruker = Bruker.query.filter_by(brukernavn=brukernavn).first()
    if bruker and bruker.passord == passord:
        session["brukernavn"] = brukernavn
        return redirect(url_for("hjem"))
    else:
        return render_template("login.html", feil_meldning="Ugyldig brukernavn eller passord!")
    
    
# Registrering
@app.route("/registrer", methods=["POST", "GET"])
def registrer():
    """Håndter brukerregistrering"""
    if request.method == "GET":
        return render_template("registrer.html")
    
    brukernavn = request.form["brukernavn"]
    passord = request.form["passord"]
    
    # Sjekk om bruker allerede eksisterer
    bruker = Bruker.query.filter_by(brukernavn=brukernavn).first()
    if bruker:
        return render_template("registrer.html", feil_meldning="Brukernavnet finnes allerede!")
    else:
        # Opprett ny bruker
        ny_bruker = Bruker(brukernavn=brukernavn, passord=passord)
        db.session.add(ny_bruker)
        db.session.commit()
        session["brukernavn"] = brukernavn
        return redirect(url_for("hjem"))

# Logg ut
@app.route("/loggut")
def loggut():
    """Logg ut brukeren fra sesjonen"""
    session.pop('brukernavn', None)
    return redirect(url_for('hjem'))
    
    
# Opprett ny oppgave
@app.route('/lagre', methods=['GET', 'POST'])
def lagre():
    """Opprett ny oppgave/notat"""
    if request.method == 'GET':
        return render_template('lagre.html')
    
    # Lagre ny oppgave i databasen
    tekst = request.form['tekst']
    ny_oppgave = Oppgave(tekst=tekst)
    db.session.add(ny_oppgave)
    db.session.commit()
    return redirect(url_for('hjem'))

# Slett oppgave
@app.route('/slett/<int:id>', methods=['POST'])
def slett(id):
    """Slett en oppgave fra databasen"""
    oppgave = Oppgave.query.get_or_404(id)
    db.session.delete(oppgave)
    db.session.commit()
    return redirect(url_for('hjem'))
    
    
if __name__ == "__main__":
    # Opprett alle databasetabeller
    with app.app_context():
        db.create_all()
    # Start Flask-serveren
    app.run(debug=True, port=5000, host="0.0.0.0")