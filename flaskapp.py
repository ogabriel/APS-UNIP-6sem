from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import app as fingerprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pesticides.db'

db = SQLAlchemy(app)

farmers = db.Table('farmers', db.metadata, autoload=True, autoload_with=db.engine)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        login_content = request.form['user']
        print(login_content)
        user = fingerprint.main(login_content)
        if user:
            session["user"] = user
            return redirect(url_for('database'))
        else:
            flash('Impressão digital incorreta ou não autorizada!')
    else:
        return render_template('index.html')


@app.route('/database/')
def database():
    user = session.get("user")
    results = db.engine.execute('SELECT * FROM farmers')
    return render_template('database.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
