from flask import Blueprint, session, request, render_template, redirect, url_for
import sqlite3

client_bp = Blueprint('client', __name__)

def signup_clients_db(name, last_name, email, phone, address):
    conn = sqlite3.connect('data/clients.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ecommerce_clients (name, lastname, email, phone, address) VALUES (?, ?, ?, ?, ?)', (name, last_name, email, phone, address))
    conn.commit()
    conn.close()

def email_exist(email):
    conn = sqlite3.connect('data/clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ecommerce_clients WHERE email=?', (email,))  
    existing_email = cursor.fetchone()
    return existing_email

def phone_exist(phone):
    conn = sqlite3.connect('data/clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ecommerce_clients WHERE phone=?', (phone,))
    existing_phone = cursor.fetchone()
    return existing_phone

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

        return render_template('signup_clients.html')
    else:
        return redirect(url_for('login.index_login'))
