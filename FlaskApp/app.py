from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_socketio import SocketIO, emit
from flask_wtf import CSRFProtect
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
import os

# Importing custom modules (Assuming you've split your code)
from models import User
from forms import RegistrationForm

# Application Configuration
app = Flask(__name__)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_key')

socketio = SocketIO(app)

# Login Manager Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Database Setup
engine = create_engine('sqlite:///SlitheryPoker.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

@login_manager.user_loader
def load_user(user_id):
    with Session() as session:
        return session.query(User).get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/play_poker')
@login_required
def play_poker():
    return render_template('play_poker.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        with Session() as session:
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                flash('Username already exists', 'danger')
                return render_template('register.html', form=form)

            user = User(username=username, password=hashed_password)
            session.add(user)
            session.commit()

            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegistrationForm(request.form)  # Create an instance of the RegistrationForm
    if request.method == 'POST':
        username = request.form.get('username')

        if username:
            with Session() as session:
                user = session.query(User).filter_by(username=username).first()
                if user:
                    login_user(user)
                    return redirect(url_for('index'))
    return render_template('login.html', form=form)  # Pass the form to the template context

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# SocketIO Events
@socketio.on('message')
@login_required
def handle_message(data):
    emit('message', data, broadcast=True)

# Main
if __name__ == '__main__':
    socketio.run(app, debug=True)
