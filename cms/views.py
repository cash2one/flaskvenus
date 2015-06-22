
from flask import request,render_template, make_response, redirect, jsonify, session
from werkzeug.security import generate_password_hash,check_password_hash
from cms import app, dbs

@app.route('/', methods=['GET'])
def index():
    login = request.args.get('logged_in', False)
    return render_template('index.html', title=__name__, content='hello, flask!!', logged_in = login)

