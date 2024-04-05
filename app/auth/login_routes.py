from flask import Blueprint, render_template, request, redirect, url_for, session
from app.auth.check_login import check_login, validate_email
import sqlite3

login_bp = Blueprint('login', __name__)

@login_bp.route('/')
def index_login():
    return render_template('login.html')

@login_bp.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

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
        return render_template('system_index.html')
    else:
        return redirect(url_for('login.index_login'))

@login_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login.index_login'))

@login_bp.route('/sign-up', methods=['POST'])
def client_signup ():
    name = request.form['sign-up name']
    lastname = request.form['sign-up lastname']
    email = request.form['sign-up email']
    password = request.form['sign-up password']
    confirm_password = request.form['sign-up confirm-password']

    if password != confirm_password:
        return f'<script>alert("As senhas não coincidem. Tente novamente."); window.location.href = "/sign-up";</script>', 400
    if not validate_email(email):
        return f'<script>alert("Por favor, insira um e-mail válido."); window.location.href = "/sign-up";</script>', 400
    try:
        conn = sqlite3.connect('data/clients.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (name, lastname, email, password) VALUES (?, ?, ?, ?)", (name, lastname, email, password))
        conn.commit()
        return "Cliente cadastrado com sucesso!"
    except Exception as e:
        return f"Ocorreu um erro ao cadastrar o cliente: {e}", 400
    finally:
        conn.close()
