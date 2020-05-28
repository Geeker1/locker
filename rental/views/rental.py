from flask import (Flask, request, render_template, session, g, redirect, url_for,
    abort, Blueprint, flash, current_app
)
import secrets
from rental.db import Link, User, Password
from rental.db import db
from rental.decorators import login_required

rental = Blueprint(
    'rental', __name__,
    template_folder='templates')


@rental.route('/')
@login_required
def home():
    return render_template('home.html')


@rental.route('/add-password', methods=['POST'])
@login_required
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
@login_required
def list_password():
    user_id = session['user_id']
    passwords = Password.query.filter_by(user_id=user_id).all()
    return render_template(
        'show_pasword.html', passwords=passwords)


@rental.route('/show-links', methods=['GET'])
@login_required
def show_links():
    user_id = session['user_id']
    links = Link.query.filter_by(user_id=user_id).all()
    return render_template(
        'show_link.html', links=links, host=request.host_url)


@rental.route('/<url>', methods=['GET'])
@login_required
def link(url):
    link = Link.query.filter_by(short_url=url).first()
    return redirect(link.url)


@rental.route('/add-link', methods=['POST'])
@login_required
def short_link():
    url = request.form['url']
    short_url = secrets.token_urlsafe(5)
    try:
        link = Link(url=url, short_url=short_url)
        user = User.query.filter_by(id=session['user_id']).first()
        user.links.append(link)
        db.session.add(user)
        db.session.commit()
        session['short_url'] = short_url
        flash('Short link has been generated')
        return redirect(url_for('rental.success'))
    except Exception as e:
        print(e)
        flash('An error occured', e)
    return redirect(url_for('rental.show_links'))


@rental.route('/success', methods=['GET'])
@login_required
def success():
    short_url = session.get('short_url', None)
    if short_url is None:
        abort(404)
    session.pop('short_url', None)
    return render_template(
        'success.html', host=request.host_url, short_url=short_url)
