from functools import wraps
from flask import redirect, url_for, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in', None) is None:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
