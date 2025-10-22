# import library
from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# init main app
app = Flask(__name__)
app.secret_key = '!@#$%'

# konfigurasi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskmysql'

# inisialisasi koneksi MySQL
mysql = MySQL(app)

# ROUTE LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        passwd = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, passwd))
        result = cur.fetchone()
        cur.close()

        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]
            flash('Login berhasil! Selamat datang, ' + result[1], 'success')
            return redirect(url_for('home'))
        else:
            flash('Email atau password salah!', 'danger')

    return render_template('login.html')


# ROUTE REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        username = request.form['username']
        email = request.form['email']
        passwd = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        account = cur.fetchone()

        if account:
            flash('Email sudah terdaftar, silakan login!', 'warning')
        else:
            cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, passwd, email))
            mysql.connection.commit()
            flash('Pendaftaran berhasil! Silakan login.', 'success')

        cur.close()
        return redirect(url_for('login'))

    return render_template('register.html')


# ROUTE HOME (Daftar pengguna)
@app.route('/home')
def home():
    if 'is_logged_in' in session:
        username = session['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, email FROM users")
        users = cur.fetchall()
        cur.close()
        return render_template('home.html', username=username, users=users)
    else:
        return redirect(url_for('login'))


# ROUTE LOGOUT
@app.route('/logout')
def logout():
    session.pop('is_logged_in', None)
    session.pop('username', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
