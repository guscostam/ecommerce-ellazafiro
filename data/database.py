import sqlite3

conn = sqlite3.connect('data/clients.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    lastname TEXT,
                    email TEXT,
                    password TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ecommerce_clients (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    lastname TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT
                )''')

clients = [
    ('Gustavo', 'Margotti', 'guscostam@gmail.com', '12345')
]

ecommerce_clients = [
    ('Isabella', 'Nacimbem', 'isa@gmail.com', '(14) 99896-0719', 'Rua B')
]

cursor.executemany("INSERT INTO clients (name, lastname, email, password) VALUES (?, ?, ?, ?)", clients)
cursor.executemany("INSERT INTO ecommerce_clients (name, lastname, email, phone, address) VALUES (?, ?, ?, ?, ?)", ecommerce_clients)

conn.commit()
conn.close()
