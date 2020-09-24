import functools
import json 
from bson import ObjectId
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import auth_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Registering a new user if it already doesn't exist.
    Taking the data through a HTML form.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = auth_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif list(db.find({"username": username})):
            error = 'User {} is already registered.'.format(username)
        
        if error is None:
            count = 1
            try:
                count = max(db.distinct('_id', {}, {})) + count
            except:
                pass
            db.insert_one({"_id": count, "username":username, "password": generate_password_hash(password)})
            return redirect(url_for('auth.login'))
        
        flash(error)
    
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Validating the username and password of already an existing user.
    session : is a dict that stores data across requests. The data stored is a cookie.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = auth_db()
        error = None
        user = list(db.find({"username": username}))

        if not user:
            error = 'Incorrect username'
        elif not check_password_hash(user[0]['password'], password):
            error = 'Incorrect password'
        if error is None:
            session.clear()
            session['user_id'] = json.dumps(user[0]['_id'], cls=JSONEncoder)
            return redirect(url_for('select_operation'))
        
        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    """
    Logged in user information should be available to other views.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = auth_db().find({"_id": user_id})

@bp.route('/logout')
def logout():
    """
    Removing the user id from the session.
    """
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    """
    CURD operations on the data will require a user to be logged in.
    Decorator is used to check this for each view it's applied to.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view