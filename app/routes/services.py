from functools import wraps
from flask import redirect, session, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('You need to log in first.', 'danger')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function