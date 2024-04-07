from flask import Blueprint, render_template, request, redirect, url_for, session
from app.auth.check_login import check_login
import sqlite3

login_bp = Blueprint('login', __name__)

@login_bp.route('/')
def index_login():
    return render_template('login.html')

@login_bp.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@login_bp.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@login_bp.route('/login', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    user = check_login(username, password)
    if user:
        session['username'] = username
        return redirect(url_for('login.dashboard'))
    else:
        return f'<script>alert("Credenciais inválidas. Tente novamente."); window.location.href = "/";</script>', 400
   
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
def client_signup():
    name = request.form['sign-up name'].capitalize()
    lastname = request.form['sign-up lastname'].capitalize()
    email = request.form['sign-up email'].lower()
    password = request.form['sign-up password']
    confirm_password = request.form['sign-up confirm-password']

    if password != confirm_password:
        return f'<script>alert("As senhas não coincidem. Tente novamente."); window.location.href = "/sign-up";</script>', 400
    
    try:
        conn = sqlite3.connect('data/clients.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE email=?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return f'<script>alert("O email já está cadastrado. Por favor, use outro email."); window.location.href = "/sign-up";</script>', 400
        
        cursor.execute("INSERT INTO clients (name, lastname, email, password, confirmpassword) VALUES (?, ?, ?, ?, ?)", (name, lastname, email, password, confirm_password))
        conn.commit()
        return f'<script>alert("Cadastrado feito com sucesso!"); window.location.href = "/";</script>'
    except Exception as e:
        return f"Ocorreu um erro ao cadastrar o cliente: {e}", 400
    finally:
        conn.close()
