from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    session
)
from flask_sqlalchemy import SQLAlchemy
import app as login_user
import os
import re
import secrets


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pesticides.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return redirect('/login', code=302)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = session.get('name')
    level = session.get('level')

    if username and level:
        return redirect('/farmers', code=302)
    else:
        file = request.files['file']
        filename = file.filename

        if re.match(r'.*\.(png|tif|jpg|gif|tiff|jpeg)$', filename):
            image_path = os.path.join('database/uploaded', filename)
            file.save(image_path)

            user = login_user.main(image_path)
            if user:
                session['name'] = user['name']
                session['level'] = user['level']

                return redirect('/farmers')
            else:
                flash('Impressão digital incorreta ou não autorizada!')
                return redirect('/login', code=302)
        else:
            flash('Impressão digital incorreta ou não autorizada!')
            return redirect('/login', code=302)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('name')
    session.pop('level')

    return redirect('/login', code=302)


@app.route('/farmers/')
def farmers():
    username = session.get('name')
    level = session.get('level')
    levels = [*range(1, level + 1)]
    levels_string = str(levels).replace('[','(').replace(']',')')


    if username and level:
        results = db.engine.execute('SELECT * FROM farmers WHERE category in' + levels_string)
        return render_template('farmers.html', results=results, username=username)
    else:
        return redirect('/login', code=302)


if __name__ == "__main__":
    app.secret_key = secrets.token_urlsafe(24)
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)
