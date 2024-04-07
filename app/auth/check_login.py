import sqlite3

def check_login(email, password):
    conn = sqlite3.connect('data/clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE email=? AND password=?', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user
