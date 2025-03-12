class Paciente:
    def __init__(self, nombre, rut, fecha_nacimiento, edad, sexo):
        self.nombre = nombre
        self.rut = rut
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = edad
        self.sexo = sexo
        self.examenes = []

    def agregar_examen(self, examen):
        self.examenes.append(examen)

class Examen:
    def __init__(self, nombre, codigo_barras, resultado):
        self.nombre = nombre
        self.codigo_barras = codigo_barras
        self.resultado = resultado
