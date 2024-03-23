import sqlite3

conn = sqlite3.connect('data/clients.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    password TEXT,
                    phonenumber TEXT,
                    addres TEXT
                )''')

clients = [
    ('João Silva', 'joao@email.com', 'senha1', '123456789', 'Rua A, 123'),
    ('Maria Santos', 'maria@email.com', 'senha2', '987654321', 'Avenida B, 456'),
    ('Pedro Oliveira', 'pedro@email.com', 'senha3', '456789123', 'Rua C, 789')
]

cursor.executemany("INSERT INTO clients (name, email, password, phonenumber, addres) VALUES (?, ?, ?, ?, ?)", clients)

conn.commit()
conn.close()
