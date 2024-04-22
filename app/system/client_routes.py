from flask import Blueprint, session, request, render_template, redirect, url_for
import sqlite3

client_bp = Blueprint('client', __name__)

def signup_clients_db(name, last_name, email, phone, address):
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect(f'data/user_{username}.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO clients (name, last_name, email, phone, address) VALUES (?, ?, ?, ?, ?)', (name, last_name, email, phone, address))
        conn.commit()
        conn.close()

def email_exist(email):
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect(f'data/user_{username}.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE email=?', (email,))  
        existing_email = cursor.fetchone()
        conn.close()
        return existing_email

def phone_exist(phone):
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect(f'data/user_{username}.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE phone=?', (phone,))
        existing_phone = cursor.fetchone()
        conn.close()
        return existing_phone

def get_clients_from_database():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect(f'data/user_{username}.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(clients)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
        conn.close()
        return clients, column_names

@client_bp.route('/signup-clients', methods=['GET', 'POST'])
def signup_clients():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['first_name'].capitalize()
            last_name = request.form['last_name'].capitalize()
            email = request.form['email'].lower()
            phone = request.form['phone']
            address = request.form['address'].capitalize()

            if email_exist(email):
                return f'<script>alert("Este e-mail já está registrado"); window.location.href = "/signup-clients";</script>', 400

            if phone_exist(phone):
                return f'<script>alert("Este celular já está registrado"); window.location.href = "/signup-clients";</script>', 400

            signup_clients_db(name, last_name, email, phone, address)

            return f'<script>alert("Cliente cadastrado com sucesso!"); window.location.href = "/signup-clients";</script>'

        return render_template('signup_clients.html')
    else:
        return redirect(url_for('login.index_login'))

@client_bp.route('/client-list')
def client_list():
    if 'username' in session:
        clients, column_names = get_clients_from_database()
        if not clients:
            message = "Não há clientes cadastrados."
        else:
            message = None
        return render_template('clients_list.html', clients=clients, column_names=column_names, message=message)
    else:
        return redirect(url_for('login.index_login'))
