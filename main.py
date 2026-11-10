from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'insecure-key-for-demo'

def get_db():
    return sqlite3.connect('app.db')

@app.route('/')
def index():
    conn = get_db()
    comments = conn.execute("SELECT content FROM comments").fetchall()
    conn.close()
    return render_template('page.html', view='index', title='Guestbook',
                           comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        user = conn.execute(
            "SELECT id, username FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['user'] = user[1]
            return redirect(url_for('index'))
        return "Invalid credentials", 401
    return render_template('page.html', view='login', title='Login')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    # УЯЗВИМОСТЬ A01:2021 (IDOR).
    user = conn.execute(
        "SELECT id, username, email FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    if user is None:
        return "User not found", 404
    return render_template('page.html', view='profile', title='Profile',
                           user=user)

@app.route('/comment', methods=['POST'])
def add_comment():
    content = request.form['content']
    conn = get_db()
    # УЯЗВИМОСТЬ A03:2021 (Stored XSS).
    conn.execute("INSERT INTO comments (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
