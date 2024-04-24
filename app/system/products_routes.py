from flask import Blueprint, render_template, redirect, url_for, session, request
import sqlite3

products_bp = Blueprint('products', __name__)

def product_registration_database(name, price, size, color):
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect(f'data/user_{username}.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (product_name, product_price, product_size, product_color) VALUES (?, ?, ?, ?)", (name, price, size, color))
        conn.commit()
        conn.close()

def get_products_from_database():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect(f'data/user_{username}.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(products)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        conn.close()
        return products, column_names

@products_bp.route('/products-registration', methods=['GET', 'POST'])
def products_registration():
    if 'username' in session:
        if request.method == 'POST':
            product_name = request.form['product_name']
            product_price = request.form['product_price']
            product_size = request.form['product_size']
            product_color = request.form['product_color']

            product_registration_database(product_name, product_price, product_size, product_color)

            return f'<script>alert("Cliente cadastrado com sucesso!"); window.location.href = "/products-registration";</script>'

        return render_template('products_registration.html')
    else:
        return redirect(url_for('login.index_login'))

@products_bp.route('/products-list')
def products_list():
    if 'username' in session:
        products, column_names = get_products_from_database()
        if not products:
            message = 'Não há produtos cadastrados.'
        else:
            message = None
        return render_template('products_list.html', products=products, column_names=column_names, message=message)
    else:
        return redirect(url_for('login.index_login'))
