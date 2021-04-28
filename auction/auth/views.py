from flask import Blueprint, session, redirect, url_for, render_template, abort, flash, request
from .forms import LoginForm, RegisterForm
from .. import db
from .models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    next = request.args.get('next')
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(name=login_form.user_name.data).first()

        # 1. Username is incorrect
        if not user:
            flash('username or password is incorrect', 'danger')
            return redirect(url_for('auth.login'))

        # 2. Username is correct but password isnt
        if not check_password_hash(user.password_hash,
                                   login_form.password.data):
            flash('username or password is incorrect', 'danger')
            return redirect(url_for('auth.login'))

        # 3. Username and Password are correct
        login_user(user)
        flash('Login sucessful!', 'success')
        if next:
            return redirect(next)
        return redirect(url_for('main.index'))

    return render_template('auth/login.html', title="Login", form=login_form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        # Check to see if username is unique
        existing_user = User.query.filter_by(
            name=register_form.user_name.data).first()

        if existing_user:
            flash('user already exists', 'danger')
            return redirect(url_for('auth.register'))

        user = User(form=register_form)

        db.session.add(user)
        db.session.commit()

        flash('Register successful!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',
                           title="Register",
                           form=register_form)


@auth_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        session.clear()
        flash('You have been successfully logged out!', 'success')
        return redirect(url_for('main.index'))
    abort(400)
