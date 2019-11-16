from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pesticides.db'

db = SQLAlchemy(app)

farmers = db.Table('farmers', db.metadata, autoload=True, autoload_with=db.engine)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return redirect('/database/')
        pass
    else:
        return render_template('index.html')


@app.route('/database/')
def database():
    results = db.session.query(farmers).all()
    return render_template('database.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
