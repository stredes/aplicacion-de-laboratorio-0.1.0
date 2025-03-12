import sys
import os

# Agregar la carpeta raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import init_db, init_pacientes_db
import appointments
from ui import login_ui
