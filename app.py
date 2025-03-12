from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Función para inicializar la base de datos
def init_db():
    with sqlite3.connect("survey.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                satisfaction INTEGER,
                branch TEXT,
                professional TEXT,
                recommend TEXT,
                comments TEXT
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        satisfaction = request.form['satisfaction']
        branch = request.form['branch']
        professional = request.form['professional']
        recommend = request.form['recommend']
        comments = request.form['comments']

        with sqlite3.connect("survey.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO responses (satisfaction, branch, professional, recommend, comments)
                VALUES (?, ?, ?, ?, ?)""",
                (satisfaction, branch, professional, recommend, comments))
            conn.commit()
        
        return redirect(url_for('thank_you'))
    
    return render_template('survey.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/admin')
def admin():
    with sqlite3.connect("survey.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM responses")
        responses = cursor.fetchall()
    return render_template('admin.html', responses=responses)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
