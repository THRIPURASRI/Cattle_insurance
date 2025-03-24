from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User
from forms import RegistrationForm, LoginForm
from flask import jsonify


auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/')
def home():
    return redirect(url_for('auth_routes.login'))

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth_routes.register'))
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            password=hashed_password,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth_routes.login'))
    return render_template('register.html', form=form)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('auth_routes.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_routes.login'))

@auth_routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)

@auth_routes.route('/api/user/<int:user_id>')
def get_user_info(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role
    })
