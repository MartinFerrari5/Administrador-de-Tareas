# Archivo que contiene la logica del administrador de tareas
import csv
from datetime import datetime
import time
from id_functions import *
headers = ['id','titulo','descripcion','estado', 'prioridad','fecha_creacion']

def crear_archivo():
        with open('tareas.csv', 'w') as f:
            csv_writer =   csv.DictWriter(f,fieldnames=headers)
            csv_writer.writeheader()
            time.sleep(3)
            print('Archivo creado') 
        
def leer_tareas():
    try:
        
        with open('tareas.csv', 'r',newline='') as f:
            next(f)
            for i in f.readlines():
                print(i)
    except FileNotFoundError:
        print('El archivo no existe, se creara uno nuevo llamado "tareas.csv"...')
        crear_archivo()

def crear_tarea():
    try:
        fecha_hoy = datetime.date(datetime.now())
        id = obtener_id()
        with open('tareas.csv', 'a',newline='') as f:
            csv_writer = csv.DictWriter(f,fieldnames=headers,delimiter=',')

            titulo =  input('Ingreso el titulo para la tarea:')
            descripcion = input('Ingrese la descripcion para la tarea:')
            estado = input('Ingrese el estado para la tarea:')
            prioridad = input('Ingrese la prioridad para la tarea:')

            csv_writer.writerow(
                {
                    'id':id,
                    'titulo': titulo,
                    'descripcion': descripcion,
                    'estado': estado,
                    'prioridad': prioridad,
                    'fecha_creacion' : fecha_hoy
                }
            )
        print('Tarea agregada correctamente')
    except FileNotFoundError:
        print('El archivo no existe, se creara uno nuevo llamado "tareas.csv"...')
        crear_archivo()

def eliminar_tarea():
    tareas_filtradas = []
    try:
        leer_tareas()
        option = int(input('Elija id de tarea a eliminar:'))
        id = obtener_id()
        
        
        while option not in range(1,id-1):
            option = input('Elija nuevamente, la tarea no existe: \n')
       
        
        with open('tareas.csv', 'r',newline='') as f:
            
            csv_reader = csv.DictReader(f,fieldnames=headers,lineterminator='')
            next(csv_reader)
            for tarea in csv_reader:
                if int(tarea['id']) != option:
                    tareas_filtradas.append(tarea)
                    
        if len(tareas_filtradas)>0:
            tareas_filtradas = modify_id(tareas_filtradas)
            
        with open('tareas.csv','w',newline='') as f:
            csv_writer = csv.DictWriter(f,fieldnames=headers,lineterminator='\n')
            csv_writer.writeheader()
            for tarea in tareas_filtradas:
                csv_writer.writerow(tarea)
        
    except FileNotFoundError:
        print('El archivo no existe, se creara uno nuevo llamado "tareas.csv"...')
        crear_archivo()
    except ValueError:
        print('Opcion invalida')


    