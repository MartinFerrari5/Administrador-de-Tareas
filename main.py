# Importar librerias
import logging
import os
import csv
from tareas import *

def select_action():
    print("""
    Bienvenido al Administrador de Tareas
          
          Eligar una opcion:
          1. Listar tareas
          2. Crear Tarea
          3. Eliminar Tarea
    """)
    valores_tareas = {
        1: leer_tareas,
        2: crear_tarea,
        3: eliminar_tarea
    }
    option = int(input("Eliga una opcion: "))

    try:
        if option in valores_tareas.keys():
            valores_tareas[option]() 
        else: raise ValueError('Valor no valido')
    except ValueError as e:
        print(e)
    finally:
        print("""
            Salir:
            1. Si
            2. No
        """)
        option = input("Eliga una opcion: ")
        while option not in ['1','2']:
            option = input("""Opcion invalida, elija de nuevo: 
                           Salir:
                            1. Si
                            2. No
                           """)
        if int(option) == 1:
            print("Saliendo del Administrador...")
            exit()
        else: 
            select_action()
        
select_action()