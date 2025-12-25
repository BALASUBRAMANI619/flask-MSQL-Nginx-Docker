# main/routes.py

from flask import Blueprint, redirect, url_for, request, render_template
from auth.decorators import token_required

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if request.cookies.get('jwt_token'):
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@main.route('/dashboard')
@token_required
def dashboard(current_user):
    return render_template('home.html', current_user=current_user)
