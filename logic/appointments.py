import sqlite3

def init_appointments_db():
    with sqlite3.connect('appointments.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS appointments (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     patient_code INTEGER,
                     patient_name TEXT,
                     appointment_date TEXT,
                     notes TEXT)''')
        conn.commit()

def add_appointment(patient_code, patient_name, appointment_date, notes=""):
    with sqlite3.connect('appointments.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO appointments (patient_code, patient_name, appointment_date, notes) VALUES (?, ?, ?, ?)",
                  (patient_code, patient_name, appointment_date, notes))
        conn.commit()

def get_appointments():
    with sqlite3.connect('appointments.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM appointments ORDER BY appointment_date")
        return c.fetchall()

def delete_appointment(appointment_id):
    with sqlite3.connect('appointments.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
        conn.commit()
