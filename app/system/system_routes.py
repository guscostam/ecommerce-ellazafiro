from flask import Blueprint, render_template, redirect, url_for, session

system_index_bp = Blueprint('system_index', __name__)

@system_index_bp.route('/clients')
def clients():
    if 'username' in session:
        return render_template('clients_homepage.html')
    else:
        return redirect(url_for('login.index_login'))
