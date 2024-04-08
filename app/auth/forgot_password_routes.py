from flask import Blueprint, render_template, request, url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
import smtplib
import sqlite3

forgot_password_bp = Blueprint('forgot_password', __name__)

password_reset_tokens = {}

smtp_server = 'smtp.gmail.com'
smtp_port = 587
gmail_user = 'ellazaffirofashion@gmail.com'
gmail_password = 'epqmqbgskiiroztj'

def db_connection(email):
    conn = sqlite3.connect('data/clients.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE email=?", (email,))
    existing_user = cursor.fetchone()
    return existing_user

def update_password(email, new_password):
    conn = sqlite3.connect('data/clients.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE clients SET password=? WHERE email=?", (new_password, email))
    conn.commit()
    conn.close()

def generate_reset_token():
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return token

def send_reset_email(email, reset_link):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = email
    msg['Subject'] = 'Recuperação de senha'
    body = f"Para redefinir sua senha, clique no link a seguir:\n{reset_link}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, email, msg.as_string())
        server.quit()
        print('E-mail enviado com sucesso')   
    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')

@forgot_password_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.form['forgot-email']
    existing_user = db_connection(email)
    if existing_user:
        reset_token = generate_reset_token()
        password_reset_tokens[email] = reset_token
        reset_link = url_for('forgot_password.reset_password', token=reset_token, _external=True)
        send_reset_email(email, reset_link)
        return f'<script>alert("Um e-mail com as instruções de recuperação foi enviado para {email}"); window.location.href = "/forgot-password";</script>'
    else:
        return f'<script>alert("Este e-mail não está registrado"); window.location.href = "/forgot-password";</script>', 400
    
@forgot_password_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == "POST":
        new_password = request.form['reset-new-password']
        confirm_password = request.form['reset-confirm-password']
        if new_password != confirm_password:
            return f'<script>alert("As senhas não coincidem"); window.location.href = "/reset-password/{token}";</script>', 400
        
        email = [email for email, t in password_reset_tokens.items() if t == token]
        if not email:
            return f'<script>alert("Token inválido"); window.location.href = "/reset-password/{token}";</script>', 400
        
        del password_reset_tokens[email[0]]

        update_password(email[0], new_password)
        return f'<script>alert("Senha redefinida com sucesso"); window.location.href = "/";</script>'
    
    return render_template('reset_password.html', token=token)
