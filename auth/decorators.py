# auth/decorators.py

from functools import wraps
from flask import request, redirect, url_for
import jwt
from models.user import User
from flask import current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')

        if not token:
            return redirect(url_for('auth.login'))

        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except jwt.ExpiredSignatureError:
            return redirect(url_for('auth.login'))
        except jwt.InvalidTokenError:
            return redirect(url_for('auth.login'))

        return f(current_user, *args, **kwargs)

    return decorated
