from flask import Flask, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'rahasia123'  # kunci rahasia session

# Data username dan password (hash)
USER = {
    'admin': generate_password_hash('admin123')
}

# Data penting
important_data = {
    'pesan': 'gmail:muhammadriskyramadan979,sandi:dzikri12345678.'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USER and check_password_hash(USER[username], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Login gagal. Username atau Password salah."
    return '''
        <h2>Login Aman</h2>
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f'''
            <h2>Selamat datang, {session['username']}!</h2>
            <p>Data penting: {important_data['pesan']}</p>
            <br>
            <a href="/admin">Halaman Admin</a><br>
            <a href="/logout">Logout</a>
        '''
    else:
        return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' in session and session['username'] == 'admin':
        if request.method == 'POST':
            new_user = request.form['new_user']
            new_pass = request.form['new_pass']
            if new_user and new_pass:
                USER[new_user] = generate_password_hash(new_pass)
                return f'User {new_user} berhasil ditambahkan! <a href="/admin">Kembali</a>'
        user_list = '<br>'.join(USER.keys())
        return f'''
            <h2>Admin Panel</h2>
            <p>User yang terdaftar:</p>
            {user_list}
            <h3>Tambah User Baru:</h3>
            <form method="post">
                Username: <input type="text" name="new_user"><br>
                Password: <input type="password" name="new_pass"><br>
                <input type="submit" value="Tambah User">
            </form>
            <br>
            <a href="/dashboard">Kembali ke Dashboard</a>
        '''
    else:
        return "Akses ditolak. Hanya admin yang bisa masuk!"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT',
5000)) # ambil dari environment,
fallback ke 5000
    app.run(host='0.0.0.0', port=port)
