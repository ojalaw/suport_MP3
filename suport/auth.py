from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.overview'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        favourite_team = request.form.get('favourite_team')
        favourite_sport = request.form.get('favourite_sport')

        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()

        if len(username) > 25:
            flash('Username must be less than 25 characters', category='error')
            return redirect(url_for('auth.sign_up'))
        if len(password1) > 25:
            flash('Password must be less than 25 characters', category='error')
            return redirect(url_for('auth.sign_up'))
        if len(favourite_team) > 25:
            flash('Favorite team must be less than 25 characters', category='error')
            return redirect(url_for('auth.sign_up'))
        if len(favourite_sport) > 25:
            flash('Favorite sport must be less than 25 characters', category='error')
            return redirect(url_for('auth.sign_up'))
        if user_email:
            flash('Email already exists. Please log in.', category='error')
        elif user_username:
            flash('Username already exists. Please choose another username.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 3:
            flash('Username must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$", password1):
            flash('Password must contain an uppercase letter, a lowercase letter, and a number.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'), favourite_team=favourite_team, favourite_sport=favourite_sport)
            db.session.add(new_user)
            db.session.commit()
            flash('You created an account! Please log in.', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign-up.html", user=current_user)
