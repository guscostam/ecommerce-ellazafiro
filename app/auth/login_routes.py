from flask import Blueprint, render_template, request, redirect, url_for, session
from app.auth.check_login import check_login

login_bp = Blueprint('login', __name__)

@login_bp.route('/')
def index_login():
    return render_template('login.html')

@login_bp.route('/login', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    user = check_login(username, password)
    if user:
        session['username'] = username
        return redirect(url_for('login.dashboard'))
    else:
        return 'Credenciais inválidas. Tente novamente.'
   
@login_bp.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f'Bem-vindo, {session["username"]}! Você está logado.'
    else:
        return redirect(url_for('login.index_login'))

@login_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login.index_login'))
