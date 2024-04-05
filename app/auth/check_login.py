from re import match
import sqlite3

def check_login(email, password):
    conn = sqlite3.connect('data/clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE email=? AND password=?', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def validate_email(email):
    return match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None
