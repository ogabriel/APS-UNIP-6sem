from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pesticides.db'

db = SQLAlchemy(app)

farmers = db.Table('farmers', db.metadata, autoload=True, autoload_with=db.engine)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/database/')
def database():
    results = db.session.query(farmers).all()
    return render_template('database.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
