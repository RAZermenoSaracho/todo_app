"""
Script de inicialización para la To Do App.
Este script asegura que la base de datos y tabla inicial estén listas para usar.
"""

from models.task import Task

def initialize():
    print("Inicializando base de datos y estructura de tabla...")
    Task.create_table()
    print("✔ Listo. Puedes ejecutar main.py para abrir la aplicación.")

if __name__ == "__main__":
    initialize()
