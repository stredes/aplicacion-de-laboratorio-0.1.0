import serial
import threading
import time
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------- Funciones para cargar la configuración ----------------------

def load_config():
    config_file_path = 'config.json'
    
    if not os.path.exists(config_file_path):
        print(f"Advertencia: El archivo {config_file_path} no fue encontrado. Usando valores predeterminados.")
        return {
            "devices": [
                {"port": "COM3", "baudrate": 9600},
                {"port": "COM4", "baudrate": 9600}
            ]
        }
    try:
        with open(config_file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: El archivo config.json no tiene un formato válido. Usando valores predeterminados.")
        return {
            "devices": [
                {"port": "COM3", "baudrate": 9600},
                {"port": "COM4", "baudrate": 9600}
            ]
        }

# ---------------------- Comunicadores Base y Dirui ----------------------

class BaseCommunicator:
    def __init__(self, port, baudrate, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.running = False

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.running = True
            print(f"Connected to {self.port}")
        except serial.SerialException as e:
            print(f"Connection error on {self.port}: {e}")

    def disconnect(self):
        if self.ser:
            self.running = False
            self.ser.close()

    def read_data(self):
        raise NotImplementedError

    def run(self):
        self.connect()
        while self.running:
            data = self.read_data()
            if data:
                self.process_data(data)
            time.sleep(0.1)

    def process_data(self, data):
        pass

class DiruiCommunicator(BaseCommunicator):
    def read_data(self):
        if self.ser and self.ser.in_waiting:
            return self.ser.readline().decode('utf-8').strip()
        return None

    def process_data(self, data):
        print(f"Received data from Dirui: {data}")

# ---------------------- Función de inicio de comunicación ----------------------

def start_device_communication():
    config = load_config()
    devices = config['devices']
    threads = []
    
    # Iniciar la comunicación para cada dispositivo
    for device_info in devices:
        communicator = DiruiCommunicator(**device_info)
        t = threading.Thread(target=communicator.run, daemon=True)
        t.start()
        threads.append(t)
    
    # Devolver los hilos para mantener la comunicación activa
    return threads

# ---------------------- Función de la GUI ----------------------

class CommunicationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Comunicación con Equipos Médicos")
        self.root.geometry("400x300")  # Tamaño de la ventana
        self.device_config = load_config()
        self.devices = self.device_config["devices"]
        
        # Crear la interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        # Frame de selección de dispositivo
        self.device_frame = ttk.LabelFrame(self.root, text="Conexión a Dispositivo", padding="10")
        self.device_frame.grid(row=0, column=0, padx=10, pady=10)

        # Combobox para elegir el puerto
        self.port_label = ttk.Label(self.device_frame, text="Puerto COM:")
        self.port_label.grid(row=0, column=0, padx=5, pady=5)
        self.port_combobox = ttk.Combobox(self.device_frame, values=[device['port'] for device in self.devices], state="readonly")
        self.port_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Combobox para elegir el baudrate
        self.baudrate_label = ttk.Label(self.device_frame, text="Baudrate:")
        self.baudrate_label.grid(row=1, column=0, padx=5, pady=5)
        self.baudrate_combobox = ttk.Combobox(self.device_frame, values=[device['baudrate'] for device in self.devices], state="readonly")
        self.baudrate_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Botón de conexión
        self.connect_button = ttk.Button(self.device_frame, text="Conectar", command=self.connect_device)
        self.connect_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Área de mensajes
        self.message_area = ttk.Label(self.root, text="Mensajes de conexión aparecerán aquí...")
        self.message_area.grid(row=1, column=0, padx=10, pady=10)

    def connect_device(self):
        port = self.port_combobox.get()
        baudrate = int(self.baudrate_combobox.get())
        
        # Iniciar la comunicación con el dispositivo seleccionado
        communicator = DiruiCommunicator(port, baudrate)
        communicator.connect()
        
        # Actualizar la interfaz
        self.message_area.config(text=f"Conectado a {port} a {baudrate} baudios.")
        print(f"Conectado a {port} a {baudrate} baudios.")

        # Abrir una nueva ventana (GUI) de conexión exitosa
        self.show_connected_gui()

        # Iniciar el hilo de comunicación
        threading.Thread(target=communicator.run, daemon=True).start()

    def show_connected_gui(self):
        # Crear una nueva ventana para mostrar la conexión exitosa
        connected_win = tk.Toplevel(self.root)
        connected_win.title("Conexión Exitosa")
        connected_win.geometry("300x200")
        connected_message = ttk.Label(connected_win, text="¡Conexión exitosa con el dispositivo!", font=("Arial", 14))
        connected_message.pack(padx=20, pady=50)
        connected_win.mainloop()

# ---------------------- Función principal ----------------------

def main():
    # Crear la ventana principal
    root = tk.Tk()
    app = CommunicationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
