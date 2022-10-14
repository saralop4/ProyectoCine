import sqlite3
import os
import uuid

from flask_login import LoginManager, login_required, login_user, logout_user
from flask import Flask, flash, redirect, render_template, request, url_for
from models.User import User

app = Flask(__name__)
login_manager = LoginManager(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

path = './app/db/cine.db'
db_url  = os.path.abspath(path)

@login_manager.user_loader
def loader(id):
    conn = sqlite3.connect(db_url)
    return User.loggerUser(conn, id)

@app.route('/')
def init():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('registro.html')
    else:
        pass1 = request.form.get('password')
        pass2 = request.form.get('confirmarPassword')
        email1 = request.form.get('email')
        email2 = request.form.get('confirmarEmail')

        if pass1 != pass2:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('registro.html')
        if email1 != email2:
            flash('Las correo electrónicos no coinciden', 'error')
            return render_template('registro.html')

        conn = sqlite3.connect(db_url)
        with conn:
            user = User(
                str(uuid.uuid4()), 
                request.form.get('email'),
                request.form.get('password'),
                request.form.get('nombres'), 
                request.form.get('apellidos'),         
                request.form.get('nDocumento'),
                request.form.get('genero'),
                request.form.get('celular'),
                request.form.get('ciudad')
                )
            user.register(conn)
            return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def ingresar():
    if request.method == 'GET':
        return render_template('ingresar.html')
    else:
        conn = sqlite3.connect(db_url)
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(None,email, password, None, None, None, None, None, None)
        response = user.login(conn)

        if response == True:
            login_user(user)
            return redirect(url_for('dashboard'))
        elif response == None:
            return render_template('ingresar.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('ingresar'))     

@app.route('/estrenos')
def estrenos():
    return render_template('estrenos.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# ---------------------------------------------------------------------------- #
#                             MANEJAMOS LOS ERRORES                            #
# ---------------------------------------------------------------------------- #
@app.errorhandler(404)
def notFounded(error):
    return render_template('404.html'), 404

@app.errorhandler(401)
def status_401(error):
    return redirect(url_for('ingresar'))

if __name__ == '__name__':
    app.register_error_handler(404, notFounded)
    app.register_error_handler(401, status_401)
    app.run() 