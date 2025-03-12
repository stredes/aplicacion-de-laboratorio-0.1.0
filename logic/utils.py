import re
import random
import openpyxl
from itertools import cycle
import os
from tkinter import simpledialog

def validar_rut(rut):
    rut = rut.replace(".", "").replace("-", "").upper()
    if len(rut) < 2:
        return False
    num, verificador = rut[:-1], rut[-1]
    try:
        reversed_digits = map(int, reversed(num))
    except ValueError:
        return False
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    check_digit = (-s) % 11
    check_digit = "K" if check_digit == 10 else str(check_digit)
    return check_digit == verificador

def obtener_codigo_barras():
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=12))

def cargar_listado_examenes_desde_excel(ruta_archivo):
    examenes = []
    try:
        workbook = openpyxl.load_workbook(ruta_archivo)
        sheet = workbook.active
        for row in sheet.iter_rows(values_only=True):
            if row[0] is not None and row[1] is not None:
                examenes.append((row[0], row[1]))
    except Exception as e:
        print(f"Error al cargar exámenes: {e}")
    return examenes

def obtener_codigo_paciente(parent):
    return simpledialog.askinteger("Número de Paciente", "Por favor, ingrese el número de paciente:", parent=parent)

def actualizar_bibliotecas(instalar=None):
    import subprocess, sys
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "setuptools"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "wheel"])
        if instalar:
            for libreria in instalar:
                subprocess.check_call([sys.executable, "-m", "pip", "install", libreria])
        print("¡Actualización e instalación de bibliotecas completadas con éxito!")
    except Exception as e:
        print(f"Error al actualizar o instalar bibliotecas: {e}")
