import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from id_functions import *
from datetime import datetime
import csv
import time

class Task_Manager():
    def __init__(self):
        # Crea la ventana con un tema moderno (elige el que prefieras)
        self.root = ttk.Window(themename="superhero")          # darkly, superhero, litera, etc.

        # ----- Frames --------------------------------------------------
        self.tasks_frame = ttk.Frame(self.root)  # padding externo

        # ----- Etiqueta de título --------------------------------------
        title = ttk.Label(
            self.root,
            text="Administrador de Tareas",
            font=("Segoe UI", 20, "bold"),
            bootstyle=PRIMARY               # color del tema
        )
        title.pack(padx=10)    # margen arriba/abajo

        # Marco para mensajes (ej. “Tarea creada”)
        self.message_frame = ttk.Frame(self.root)

        # Empaquetar el resto
        self.tasks_frame.pack(fill=BOTH, padx=10)
        self.message_frame.pack(fill=X, padx=10)
        
        self.headers = ['id','titulo','descripcion','estado', 'prioridad','fecha_creacion']

        self.button_grid = tk.Frame(self.root)
        self.button_grid.columnconfigure(0, weight=1)
        self.button_grid.columnconfigure(1, weight=1)
        self.button_grid.columnconfigure(2, weight=1)
        self.button_grid.columnconfigure(3, weight=1)
        
        # Valores de tareas
        self.title_entry = ''
        self.description_entry = ''
        self.status_entry = ''
        self.prioridad_entry = ''
        
        self.id_entry = ''
        
        self.create_ui()
    def create_ui(self):
        button_read = tk.Button( self.button_grid,text='Leer Tareas', bg='white', fg='black', width=12,cursor='hand2', command=self.leer_tareas)
        button_read.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        button_create = tk.Button(self.button_grid,text='Crear Tarea', bg='white', fg='black', width=12,cursor='hand2', command=self.crear_tarea_ui)
        button_create.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        button_delete = tk.Button(self.button_grid,text='Eliminar Tarea', bg='white', fg='black', width=12,cursor='hand2',command=self.eliminar_tarea_ui)
        button_delete.grid(row=0, column=3, sticky='nsew', padx=5, pady=5)
    
        button_update = tk.Button(self.button_grid,text='Actualizar Tarea', bg='white', fg='black', width=12,cursor='hand2', command=self.actualizar_tarea_ui)
        button_update.grid(row=0, column=4, sticky='nsew', padx=5, pady=5)

        self.button_grid.pack(padx=10, pady=10)

        self.root.geometry("900x500")
        self.root.mainloop()

    def crear_archivo(self):
        with open('tareas.csv', 'w',newline='') as f:
            csv_writer =   csv.DictWriter(f,fieldnames=self.headers)
            csv_writer.writeheader()
            time.sleep(1)
            label = tk.Label(self.message_frame, text='El archivo no existe, se creara uno nuevo llamado "tareas.csv"...', fg='blue' ,font=("Arial", 12))
            label.grid(row=0, column=1, sticky='nsew')
            self.message_frame.pack(padx=10, pady=10)
    def leer_tareas(self):
        try:
           
            self.clean_frame()
            with open('tareas.csv', 'r',newline='') as f:
                #next(f)
                for i,k in enumerate(f.readlines()):
                    k = k.replace(',', ' -- ').replace('_',' ').upper()
                    size = i == 0 and 14 or 12
                    color = i == 0 and 'black' or 'gray'
                    
                    label = tk.Label(self.tasks_frame, text=k,fg=color ,font=("Arial", size),pady=0)
                    label.grid(row=i, column=1, sticky='nsew', pady=0,ipady=0)
            self.tasks_frame.pack(padx=10, pady=1)
        except FileNotFoundError:
            label = tk.Label(self.message_frame, text='El archivo no existe, se creara uno nuevo llamado "tareas.csv"...', fg='blue' ,font=("Arial", 12))
            label.grid(row=0, column=1, sticky='nsew')
            self.message_frame.pack(padx=10, pady=10)
            self.crear_archivo()
    def crear_tarea_ui(self):
        try:
            
            self.clean_frame()
            
            self.tasks_fields()
            
            submit_button = tk.Button(self.tasks_frame,text='Submit', bg='white', fg='black', width=10,cursor='hand2',command=self.post_tarea)
            submit_button.grid(row=5, column=1, sticky='nsew', padx=5, pady=5)
            
            self.tasks_frame.pack()
           
        except FileNotFoundError:
            print('El archivo no existe, se creara uno nuevo llamado "tareas.csv"...')
            # crear_archivo()

    def post_tarea(self):
        
        try:
            fecha_hoy = datetime.date(datetime.now())
            id = obtener_id()
            
            with open('tareas.csv', 'a',newline='') as f:
                csv_writer = csv.DictWriter(f,fieldnames=self.headers,delimiter=',')

                csv_writer.writerow(
                {
                'id':id,
                'titulo': self.title_entry.get(),
                'descripcion': self.description_entry.get("1.0", tk.END).strip(),
                'estado': self.status_entry.get(),
                'prioridad': self.prioridad_entry.get(),
                'fecha_creacion' : fecha_hoy
                }
                )
            self.title_entry.delete(0, tk.END)
            self.description_entry.delete("1.0", tk.END)
            self.status_entry.delete(0, tk.END)
            self.prioridad_entry.delete(0, tk.END)
             
             
            label = tk.Label(self.message_frame, text='Tarea creada con exito', fg='green' ,font=("Arial", 12))
            label.grid(row=0, column=1, sticky='nsew')
            self.message_frame.pack(padx=10, pady=10) 
        except Exception as e:
            print(e)
            label = tk.Label(self.root, text='Error al crear la tarea', fg='red' ,font=("Arial", 12))
            label.pack()
        except FileNotFoundError:
            print('El archivo no existe, se creara uno nuevo llamado "tareas.csv"...')
            label = tk.Label(self.message_frame, text='El archivo no existe, se creara uno nuevo llamado "tareas.csv"...', fg='blue' ,font=("Arial", 12))
            label.grid(row=0, column=1, sticky='nsew')
            self.message_frame.pack(padx=10, pady=10)
            self.crear_archivo()

    def eliminar_tarea_ui(self):
       
        self.clean_frame()
        try:
            
            id_label = tk.Label(self.tasks_frame,text='Elija id de tarea a eliminar:', font=("Arial", 12))
            id_label.grid(row=0, column=0,pady=5)
            
            self.id_entry = tk.Entry(self.tasks_frame, width=10 )
            self.id_entry.grid(row=0, column=1,pady=5)
            
            submit_button = tk.Button(self.tasks_frame,text='Borrar', font=("Arial", 12), cursor='hand2',command=self.delete_tarea)
            submit_button.grid(row=1, column=0,pady=5)
            
            self.tasks_frame.pack()
            
        except FileNotFoundError:
            print('El archivo no existe, se creara uno nuevo llamado "tareas.csv"...')
            self.crear_archivo()
        except ValueError:
            print('Opcion invalida')    
    
    def actualizar_tarea_ui(self):
        self.clean_frame()
        
        id_label = tk.Label(self.tasks_frame,text='Elija id de tarea a actualizar:', font=("Arial", 12))
        id_label.grid(row=0, column=0,pady=5)
            
        self.id_entry = tk.Entry(self.tasks_frame, width=10 )
        self.id_entry.grid(row=0, column=1,pady=5)
        
        self.tasks_fields()
        
        submit_button = tk.Button(self.tasks_frame,text='Obtener', font=("Arial", 12), cursor='hand2',command=self.get_tarea)
        submit_button.grid(row=6, column=0,pady=5)
        
        submit_button = tk.Button(self.tasks_frame,text='Actualizar', font=("Arial", 12), cursor='hand2',fg='green',command=self.put_tarea)
        submit_button.grid(row=6, column=1,pady=5)
        
        self.tasks_frame.pack() 

    def put_tarea(self):
        try:
            updated_tasks = []
            with open('tareas.csv', 'r',newline='') as f:
                csv_reader = csv.DictReader(f,fieldnames=self.headers,lineterminator='')
                next(csv_reader)
                for row in  csv_reader:
                    if row['id'] == self.id_entry.get():
                        row['titulo'] = self.title_entry.get()
                        row['descripcion'] = self.description_entry.get("1.0", tk.END).strip()
                        row['estado'] = self.status_entry.get()
                        row['prioridad'] = self.prioridad_entry.get()
                        updated_tasks.append(row)
                    else:
                        updated_tasks.append(row)
            
                with open('tareas.csv','w',newline='') as f:
                    csv_writer = csv.DictWriter(f,fieldnames=self.headers,lineterminator='\n')
                    csv_writer.writeheader()
                
                    for row in updated_tasks:
                        csv_writer.writerow(row)
             
            self.send_message('Tarea actualizada con exito', 'SUCCESS') 
        except:
            self.send_message('Error al actualizar la tarea', 'DANGER')
    def get_tarea(self):
        try:
            task = []
            with open('tareas.csv', 'r',newline='') as f:
                csv_reader = csv.DictReader(f,fieldnames=self.headers,lineterminator='')
                for row in  csv_reader: 
                    if row['id'] == self.id_entry.get():
                        task.append(row)
            
                        self.title_entry.insert(0, row['titulo'])
                        self.description_entry.insert("1.0", row['descripcion'])
                        self.status_entry.insert(0, row['estado'])
                        self.prioridad_entry.insert(0, row['prioridad'])
                        
            if len(task) == 0:
                raise Exception('La tarea no existe')
            
        except FileNotFoundError:
            self.send_message('El archivo no existe, se creara uno nuevo llamado "tareas.csv"...', 'PRIMARY')
            self.crear_archivo()
        except Exception as e:
            self.send_message('Error: La tarea no existe', 'DANGER')
            self.delete_fields()
    def delete_tarea(self):
        try:
            tareas_filtradas = []
            id = obtener_id()
            print(id,self.id_entry.get())
            
            if self.id_entry.get() == '' or int(self.id_entry.get()) not in range(1,id):
                win = tk.Toplevel()
                win.wm_title("Opcion Invalida")

                label = ttk.Label(win, text="Error: La tarea no existe", font=("Arial", 12, "bold"), bootstyle="danger")
                label.grid(row=0, column=0,padx=10,pady=10)

                button = tk.Button(win, text="Aceptar", command=win.destroy, font=("Arial", 12, "bold"), bg='white', fg='black', width=10,cursor='hand2')
                button.grid(row=1, column=0)
                return
        
            with open('tareas.csv', 'r',newline='') as f:
                
                csv_reader = csv.DictReader(f,fieldnames=self.headers,lineterminator='')
                next(csv_reader)
                for tarea in csv_reader:
                    if tarea['id'] != self.id_entry.get():
                        tareas_filtradas.append(tarea)
                        
            if len(tareas_filtradas)>0:
                tareas_filtradas = modify_id(tareas_filtradas)
                
            with open('tareas.csv','w',newline='') as f:
                csv_writer = csv.DictWriter(f,fieldnames=self.headers,lineterminator='\n')
                csv_writer.writeheader()
                for tarea in tareas_filtradas:
                    csv_writer.writerow(tarea)
            self.send_message('Tarea eliminada con exito','SUCCESS')
        except:
            self.send_message('Error: La tarea no existe','DANGER')
    def clean_frame(self):
        frames = [self.tasks_frame, self.message_frame]
        
        for frame in frames:
            for widget in frame.winfo_children( ):
                widget.destroy()
            frame.pack_forget()
    
    def tasks_fields(self):
            title_label = tk.Label(self.tasks_frame, text="Titulo Tarea", font=("Arial", 12))
            title_label.grid(row=1, column=0,pady=5)
            self.title_entry = tk.Entry(self.tasks_frame)
            self.title_entry.grid(row=1, column=1,pady=5)
            
            description_label = tk.Label(self.tasks_frame, text="Descripcion Tarea", font=("Arial", 12))
            description_label.grid(row=2, column=0,pady=5)
            self.description_entry = tk.Text(self.tasks_frame, height=2, width=30)
            self.description_entry.grid(row=2, column=1, pady=5)
            
            status_label = tk.Label(self.tasks_frame, text="Estado de la Tarea", font=("Arial", 12))
            status_label.grid(row=3, column=0,pady=5)
            self.status_entry = tk.Entry(self.tasks_frame)
            self.status_entry.grid(row=3, column=1,pady=5)
            
            prioridad_label = tk.Label(self.tasks_frame, text="Prioridad Tarea", font=("Arial", 12))
            prioridad_label.grid(row=4, column=0,pady=5)
            self.prioridad_entry = tk.Entry(self.tasks_frame)
            self.prioridad_entry.grid(row=4, column=1,pady=5)
    
    def delete_fields(self):
        self.title_entry.delete(0,'end')
        self.description_entry.delete("1.0", tk.END)
        self.status_entry.delete(0,'end')
        self.prioridad_entry.delete(0,'end')
    def send_message(self,texto,color):
        label = ttk.Label(self.message_frame, text=texto, bootstyle=color ,font=("Arial", 12))
        label.grid(row=0, column=1, sticky='nsew')
        self.message_frame.pack(padx=10, pady=10)


Task_Manager()