from flask import Flask, render_template, redirect, url_for, session, request
import mysql.connector
import hashlib
from waitress import serve

app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="anohej",
        password="Ih8Fags",
        database="skolesystem",
    )


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        brukernavn = request.form["brukernavn"]
        password_hashed = request.form["password_hashed"]
        hashed_password = hashlib.sha256(password_hashed.encode()).hexdigest()

        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO bruker (brukernavn, password_hashed) VALUES (%s, %s)",
                (brukernavn, hashed_password)
            )
            db.commit()
        except mysql.connector.IntegrityError:
            return "brukernavn already exists"
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
        brukernavn = request.form["brukernavn"]
        password = request.form["password"]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE brukernavn = %s AND password = %s",
            (brukernavn, hashed_password)
        )
        bruker = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            session['user_id'] = bruker['id']
            session['brukernavn'] = bruker['brukernavn']
            return redirect(url_for('index'))
        else:
            return "invalid brukernavn or password"

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

    # sender tasks (liste) og brukernavn (string) til html
    return render_template('index.html', tasks=tasks, brukernavn=session['brukernavn'])


#ny oppgave
@app.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    #henter data fra skjemaet
    title = request.form.get('title')
    description = request.form.get('description')

    db = get_db_connection
    cursor = db.cursor()


    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (%s, %s)", #insert legger inn en ny oppgave
        (title, description)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('index'))


@app.route('/done/<int_task_id>') # markerer opg som frdy, <int: task_id> betyr at task_id er et heltall (int)
def mark_done(tasks_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db_connection()
    cursor = db.cursor()



@app.roure('/delete/<int:task_id>')
def delete_task(tasks_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (tasks_id,)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)




        
