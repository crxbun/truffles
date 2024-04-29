from flask import render_template, request, redirect, url_for, jsonify, flash
from flask import session as login_session
## from truffles.models import .. import models here
from truffles import app, db 
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    pw = request.form.get('password')

    # create User model in models.
    #user = User.query.filter_by(username=username).first()

    # if user is None:
    #     return render_template('login.html', error='User does not exist.')

    return render_template('login.html')
    

