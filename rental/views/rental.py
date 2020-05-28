from flask import (Flask, request, render_template, session, g, redirect, url_for,
    abort, Blueprint, flash, current_app
)
import secrets
from rental.db import Link, User, Password
from rental.db import db

rental = Blueprint(
    'rental', __name__,
    template_folder='templates')


@rental.route('/')
def home():
    print(request.url, request.base_url)
    if session.get('logged_in', None) is None:
        return redirect(url_for('auth.login'))
    print(session.get('user_id', None))
    return render_template('home.html')


@rental.route('/add-password', methods=['POST'])
def add_password():
    user_id = session['user_id']
    password = secrets.token_urlsafe(10)
    username = request.form['username']
    website = request.form['website']
    try:
        passw = Password(
            username=username, website=website, password=password)
        user = User.query.filter_by(id=user_id).first()
        user.passwords.append(passw)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        flash('An error occured while saving user data')
        return redirect(url_for('rental.home'))

    flash('Password has been added successfully')
    return redirect(url_for('rental.home'))


@rental.route('/show-passwords', methods=['GET'])
def list_password():
    user_id = session['user_id']
    passwords = Password.query.filter_by(user_id=user_id).all()
    return render_template(
        'show_pasword.html', passwords=passwords)


@rental.route('/show-links', methods=['GET'])
def show_links():
    user_id = session['user_id']
    links = Link.query.filter_by(user_id=user_id).all()
    return render_template(
        'show_link.html', links=links, host=request.host_url)


@rental.route('/<url>', methods=['GET'])
def link(url):
    link = Link.query.filter_by(short_url=url).first()
    return redirect(link.url)


@rental.route('/add-link', methods=['POST'])
def short_link():
    url = request.form['url']
    short_url = secrets.token_urlsafe(5)
    try:
        link = Link(url=url, short_url=short_url)
        user = User.query.filter_by(id=session['user_id']).first()
        user.links.append(link)
        db.session.add(user)
        db.session.commit()
        flash('Short link has been generated')
        return redirect(url_for('rental.home'))
    except Exception as e:
        print(e)
        flash('An error occured', e)
    return redirect(url_for('rental.show_links'))
