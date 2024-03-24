from flask import Blueprint, render_template, request, redirect, url_for

login_bp = Blueprint('login', __name__)

users = {'gustavo': '1234'}

@login_bp.route('/')
def index_login():
    return render_template('login.html')

@login_bp.route('/login', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        return redirect(url_for('login.success', username=username))
    else:
        return redirect(url_for('login.index_login'))
    
@login_bp.route('/success/<username>')
def success(username):
    return f'Bem-vindo, {username}!'
