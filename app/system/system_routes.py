from flask import Blueprint, render_template, redirect, url_for, session

system_index_bp = Blueprint('system_index', __name__)

@system_index_bp.route('/clients')
def clients():
    if 'username' in session:
        return render_template('clients_homepage.html')
    else:
        return redirect(url_for('login.index_login'))

@system_index_bp.route('/products')
def products():
    if 'username' in session:
        return render_template('products_homepage.html')
    else:
        return redirect(url_for('login.index_login'))
    
@system_index_bp.route('/reports')
def reports():
    if 'username' in session:
        return render_template('reports_homepage.html')
    else:
        return redirect(url_for('login.index_login'))

@system_index_bp.route('/product-reports')
def product_reports():
    if 'username' in session:
        return render_template('product_reports.html')
    else:
        return redirect(url_for('login.index_login'))

@system_index_bp.route('/client-reports')
def client_reports():
    if 'username' in session:
        return render_template('client_reports.html')
    else:
        return redirect(url_for('login.index_login'))
