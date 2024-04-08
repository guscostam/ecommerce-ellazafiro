from flask import Blueprint, request
import sqlite3

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/sign-up', methods=['POST'])
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
        
        cursor.execute("INSERT INTO clients (name, lastname, email, password) VALUES (?, ?, ?, ?)", (name, lastname, email, password))
        conn.commit()
        return f'<script>alert("Cadastrado feito com sucesso!"); window.location.href = "/";</script>'
    except Exception as e:
        return f'<script>alert("Ocorreu um erro ao cadastrar o cliente: {e}"); window.location.href = "/sign-up";</script>', 400
    finally:
        conn.close()
