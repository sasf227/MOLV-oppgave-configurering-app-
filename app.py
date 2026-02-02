from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from main import Textify



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)




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
    flash('Item deleted', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)