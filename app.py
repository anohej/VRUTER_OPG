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
        passord = request.form["passord"]
        passord_hash = hashlib.sha256(passord.encode()).hexdigest()

        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO bruker (brukernavn, passord_hash) VALUES (%s, %s)",
                (brukernavn, passord_hash)
            )
            db.commit()
        except mysql.connector.IntegrityError:
            return "brukernavn already exists"

        return redirect(url_for('login'))

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        brukernavn = request.form["brukernavn"]
        password = request.form["password"]
        passord_hash = hashlib.sha256(password.encode()).hexdigest()

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            # henter bruker fra databasen der brukernavn og passord_hash matcher
            "SELECT * FROM bruker WHERE brukernavn = %s AND passord_hash = %s",   
            (brukernavn, passord_hash)
        )
        bruker = cursor.fetchone()
        cursor.close()
        db.close()

        if bruker:
            session['user_id'] = bruker['id']
            session['brukernavn'] = bruker['brukernavn']
            return redirect(url_for('index'))
        else:
            return "ugyldig brukernavn eller passord"

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

    cursor.execute("SELECT * FROM deadline WHERE bruker_id = %s ORDER BY frist DESC", (session['user_id'],)) # ORDER BY frist DESC = nyeste først session iden til dem som er logget inn

    # fetchall returnerer liste (list) med deadlines
    deadlines = cursor.fetchall()

    cursor.close()
    db.close()

    # sender deadlines (liste) og brukernavn (string) til html
    return render_template('index.html', deadlines=deadlines, brukernavn=session['brukernavn'])



# ny deadline
@app.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # henter data fra skjemaet
    tittel = request.form.get('tittel')
    beskrivelse = request.form.get('beskrivelse')
    frist = request.form.get('frist')

    db = get_db_connection()  # husk parenteser!
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO deadline (tittel, beskrivelse, frist, bruker_id) VALUES (%s, %s, %s, %s)", # insert legger inn en ny deadline
        (tittel, beskrivelse, frist, session['user_id'])
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('index'))


@app.route('/done/<int:task_id>') # markerer deadline som ferdig, <int:task_id> betyr at task_id er et heltall (int)
def mark_done(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE deadline SET fullfort = 1 WHERE id = %s",
        (task_id,)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM deadline WHERE id = %s",
        (task_id,)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)



@app.route('/api/vaer')
def api_vaer():
    response = requests.get(
        "https://api.met.no/weatherapi/locationforecast/2.0/compact",
        params={"lat": "59.91", "lon": "10.75"},
        headers={"User-Agent": "kube-elev-dashboard kontakt@example.com"},
        timeout=5
    )
    data = response.json()
    now = data["properties"]["timeseries"][0]["data"]
    details = now["instant"]["details"]
    next1 = now.get("next_1_hours", {})

    return jsonify({
        "temp": round(details["air_temperature"], 1),
        "vind": round(details["wind_speed"], 1),
        "nedbor": next1.get("details", {}).get("precipitation_amount", 0)
    })