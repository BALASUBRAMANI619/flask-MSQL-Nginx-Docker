# auth/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timezone, timedelta

from models.user import User
from extensions import db
from flask import current_app

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.cookies.get('jwt_token'):
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid email or password'}), 401

        token = jwt.encode(
            {
                'public_id': user.public_id,
                'exp': datetime.now(timezone.utc) + timedelta(hours=1)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )

        response = make_response(redirect(url_for('main.dashboard')))
        response.set_cookie('jwt_token', token, httponly=True, samesite='Lax')
        return response

    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.cookies.get('jwt_token'):
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'User already exists'}), 400

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/logout')
def logout():
    response = make_response(redirect(url_for('auth.login')))
    response.set_cookie('jwt_token', '', expires=0)
    return response
