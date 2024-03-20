from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = {'gustavo': '1234'}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        return redirect(url_for('success', username=username))
    else:
        return redirect(url_for('index'))
    
@app.route('/success/<username>')
def success(username):
    return f'Bem-vindo, {username}!'

if __name__ == '__main__':
    app.run(debug=True)
