import sqlite3

conn = sqlite3.connect('data/clients.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    lastname TEXT,
                    email TEXT,
                    password TEXT,
                    confirmpassword TEXT
                )''')

clients = [
    ('Gustavo', 'Margotti', 'guscostam@gmail.com', '12345', '12345')
]

cursor.executemany("INSERT INTO clients (name, lastname, email, password, confirmpassword) VALUES (?, ?, ?, ?, ?)", clients)

conn.commit()
conn.close()
