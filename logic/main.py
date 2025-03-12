import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import init_db, init_pacientes_db
from logic import appointments
from ui.login_ui import login_ui
import sys

def main():
    try:
        init_db()
        init_pacientes_db()
        appointments.init_appointments_db()
        login_ui()
    except Exception as e:
        print(f"Error starting the application: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
