from flask import Blueprint, request, render_template, redirect, url_for, session

system_index_bp = Blueprint('system_index', __name__)

@system_index_bp.route('/clients')
def clients():
    if 'username' in session:
        return render_template('clients_homepage.html')
    else:
        return redirect(url_for('login.index_login'))

@system_index_bp.route('/signup-clients', methods=['GET', 'POST'])
def signup_clients():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            addres = request.form['addres']

        return render_template('signup_clients.html')
    else:
        return redirect(url_for('login.index_login'))
