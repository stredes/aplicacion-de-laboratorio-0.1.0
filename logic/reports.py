import matplotlib.pyplot as plt
from database import cargar_desde_base_de_datos
import os

def generate_statistics(save_path=None):
    pacientes = cargar_desde_base_de_datos()
    data = {paciente['Nombre']: len(paciente['Examenes']) for paciente in pacientes.values()}
    
    names = list(data.keys())
    counts = list(data.values())
    
    plt.figure(figsize=(10,6))
    plt.bar(names, counts, color='skyblue')
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Cantidad de exámenes")
    plt.title("Exámenes por paciente")
    plt.tight_layout()
    
    if save_path:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        plt.savefig(os.path.join(save_path, "report.png"))
    else:
        plt.show()
