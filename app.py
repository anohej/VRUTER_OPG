from flask import Flask, render_template, redirect, url_for, session, request
import mysql.connector
import hashlib
from waitress import serve

app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_db_connection():
    return mysql.connector.connect(
        host="10.200.14.28",
        user="anohej",
        password="Ih8Fags",
        database="todolist_db",
    )


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            db.commit()
        except mysql.connector.IntegrityError:
            return "username already exists"
        finally:
            cursor.close()
            db.close()

        return redirect(url_for('login'))

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, hashed_password)
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            return "invalid username or password"

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))




@app.route('/')
def index():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()

    cursor = db.cursor(dictionary=True) # dictionary=True gjør at tasks blir liste av dictionaries

    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC") # ORDER BY created_at DESC = nyeste først

    # fetchall returnerer liste (list) med oppgaver
    tasks = cursor.fetchall()

    cursor.close()
    db.close()

    # sender tasks (liste) og username (string) til html
    return render_template('index.html', tasks=tasks, username=session['username'])





#@app.route('/add')


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
        