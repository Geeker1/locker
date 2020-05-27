from flask import (
    request, render_template, session, redirect, url_for,
    Blueprint, flash
)

import bcrypt
from rental.db import User
from rental import db

auth = Blueprint(
    'auth', __name__,
    template_folder='templates')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        try:
            password = bcrypt.hashpw(
                request.form['password'].encode(), bcrypt.gensalt())
            user = User(
                username=request.form['username'],
                password=password.decode(),
                email=request.form['email']
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(e)
            error = "An error occured while creating your account"
    return render_template('signup.html', error=error)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        print(user)
        if user is None:
            error = 'User does not exist'
        elif bcrypt.checkpw(password.encode(), user.password.encode()):
            session['logged_in'] = True
            session['user_id'] = user.id
            flash('You were logged_in')
            return redirect(url_for('rental.home'))
    return render_template('login.html', error=error)


@auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('auth.login'))
