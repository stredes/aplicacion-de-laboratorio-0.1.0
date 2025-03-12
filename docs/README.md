# Proyecto Maestro

Este es un sistema de gestión para el registro de pacientes, exámenes y citas médicas. El proyecto permite registrar, editar, eliminar pacientes y realizar un seguimiento de los exámenes realizados a cada paciente. Además, permite generar listados de derivación y programar citas.

## Características

- Registro de pacientes con nombre, RUT, fecha de nacimiento, edad y sexo.
- Registro de exámenes realizados a cada paciente, con resultado y código de barras.
- Generación de listados de derivación en formato Excel.
- Programación de citas para pacientes.
- Interfaz gráfica de usuario basada en `Tkinter`.
- Comunicación con dispositivos médicos a través de puertos COM.

## Requisitos

- Python 3.7 o superior.
- Paquetes de Python necesarios:
  - `openpyxl`
  - `tkinter`
  - `re`
  - `os`
  - `datetime`
  - `colorchooser`

## Instalación

### 1. Clonar el repositorio

Para clonar el proyecto, abre una terminal y ejecuta el siguiente comando:

```bash
git clone https://github.com/stredes/0master0.git
