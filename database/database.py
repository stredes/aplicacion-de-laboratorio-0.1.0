import sqlite3

# Base de datos de usuarios
def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nombre TEXT, 
                      email TEXT UNIQUE, 
                      contraseña TEXT)''')
    conn.commit()
    conn.close()

def add_user(nombre, email, contraseña):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, email, contraseña) VALUES (?, ?, ?)",
                       (nombre, email, contraseña))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(email, contraseña):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND contraseña = ?", (email, contraseña))
    user = cursor.fetchone()
    conn.close()
    return user

# Base de datos para pacientes y exámenes
def init_pacientes_db():
    conn = sqlite3.connect('pacientes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pacientes (
        codigo INTEGER PRIMARY KEY,
        nombre TEXT, 
        rut TEXT, 
        fecha_nacimiento TEXT, 
        edad TEXT, 
        sexo TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS examenes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_barras TEXT, 
        examen TEXT, 
        codigo_paciente INTEGER, 
        resultado TEXT,
        FOREIGN KEY(codigo_paciente) REFERENCES pacientes(codigo))''')
    # Opcional: tabla de historial clínico
    c.execute('''CREATE TABLE IF NOT EXISTS historial (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 patient_code INTEGER,
                 fecha TEXT,
                 descripcion TEXT,
                 FOREIGN KEY(patient_code) REFERENCES pacientes(codigo))''')
    conn.commit()
    conn.close()

def guardar_en_base_de_datos(pacientes):
    conn = sqlite3.connect('pacientes.db')
    c = conn.cursor()
    for codigo, datos in pacientes.items():
        c.execute("INSERT OR REPLACE INTO pacientes (codigo, nombre, rut, fecha_nacimiento, edad, sexo) VALUES (?, ?, ?, ?, ?, ?)",
                  (codigo, datos['Nombre'], datos['Rut'], datos['Fecha Nacimiento'], datos['Edad'], datos['Sexo']))
        for examen in datos['Examenes']:
            c.execute("INSERT INTO examenes (codigo_barras, examen, codigo_paciente, resultado) VALUES (?, ?, ?, ?)",
                      (examen['Código de Barras'], examen['Examen'], codigo, examen['Resultado']))
    conn.commit()
    conn.close()

def cargar_desde_base_de_datos():
    pacientes = {}
    conn = sqlite3.connect('pacientes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM pacientes")
    for row in c.fetchall():
        codigo, nombre, rut, fecha_nacimiento, edad, sexo = row
        pacientes[codigo] = {
            'Código': codigo,
            'Nombre': nombre,
            'Rut': rut,
            'Fecha Nacimiento': fecha_nacimiento,
            'Edad': edad,
            'Sexo': sexo,
            'Examenes': []
        }
    c.execute("SELECT * FROM examenes")
    for row in c.fetchall():
        _, codigo_barras, examen, codigo_paciente, resultado = row
        if codigo_paciente in pacientes:
            pacientes[codigo_paciente]['Examenes'].append({
                'Examen': examen,
                'Código de Barras': codigo_barras,
                'Resultado': resultado
            })
    conn.close()
    return pacientes
