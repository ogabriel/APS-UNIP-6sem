from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for
)
import app as login_user
import os
import re


app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/login', code=302)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    file = request.files['file']
    filename = file.filename

    if re.match(r'.*\.(png|tif|jpg|gif|tiff|jpeg)$', filename):
        image_path = os.path.join('database/uploaded', filename)
        file.save(image_path)

        return login_user.main(image_path)
    else:
        return "Input not valid"


if __name__ == "__main__":
    app.run(debug=True)
