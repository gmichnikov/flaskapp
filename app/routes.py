from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from app.forms import RegistrationForm, LoginForm, AdminPasswordResetForm

@app.route('/')
def index():
    # Check if a user is logged in
    if current_user.is_authenticated:
        username = current_user.username
        return render_template('index.html', logged_in=True, username=username)
    else:
        return render_template('index.html', logged_in=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('register'))
        
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        # Automatically make user 'greg' an admin
        if form.username.data.lower() == 'greg':
            new_user.is_admin = True

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin_reset_password', methods=['GET', 'POST'])
@login_required
def admin_reset_password():
    if not current_user.is_admin:
        return redirect(url_for('index'))

    form = AdminPasswordResetForm()
    form.username.choices = [(user.username, user.username) for user in User.query.all()]

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password reset successfully.')
        else:
            flash('User not found.')

    return render_template('admin_reset_password.html', form=form)
