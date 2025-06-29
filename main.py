import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from id_functions import *
from datetime import datetime
import csv
import time
import logging
from logs import start_logging

class Task_Manager():
    def __init__(self):
        """
        Inicializa el administrador de tareas
        
        - Se crea el panel inicial del GUI (Graphical User Interface)
        """
        
        
        # ----- Instanciar archivo logging --------------------------------------
        start_logging()
        # Crea la ventana con un tema moderno (elige el que prefieras)
        self.root = ttk.Window(themename="superhero")          # darkly, superhero, litera, etc.

        # ----- Frames --------------------------------------------------
        self.tasks_frame = ttk.Frame(self.root)  # padding externo

        # ----- Etiqueta de titulo --------------------------------------
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
        """
        Crea la interfaz principal del administrador de tareas, incluyendo los botones
        para leer, crear, eliminar y actualizar tareas. Tambien configura el tamaño 
        de la ventana principal y lanza el bucle de eventos de la aplicación.
        """

        # Botón para leer tareas
        button_read = tk.Button(
            self.button_grid,
            text='Leer Tareas',
            bg='white',
            fg='black',
            width=12,
            cursor='hand2',
            command=self.leer_tareas
        )
        button_read.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Botón para crear nueva tarea
        button_create = tk.Button(
            self.button_grid,
            text='Crear Tarea',
            bg='white',
            fg='black',
            width=12,
            cursor='hand2',
            command=self.crear_tarea_ui
        )
        button_create.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        # Botón para eliminar tarea existente
        button_delete = tk.Button(
            self.button_grid,
            text='Eliminar Tarea',
            bg='white',
            fg='black',
            width=12,
            cursor='hand2',
            command=self.eliminar_tarea_ui
        )
        button_delete.grid(row=0, column=3, sticky='nsew', padx=5, pady=5)

        # Botón para actualizar tarea
        button_update = tk.Button(
            self.button_grid,
            text='Actualizar Tarea',
            bg='white',
            fg='black',
            width=12,
            cursor='hand2',
            command=self.actualizar_tarea_ui
        )
        button_update.grid(row=0, column=4, sticky='nsew', padx=5, pady=5)

        # Empaquetar el grid de botones y configurar la ventana principal
        self.button_grid.pack(padx=10, pady=10)
        self.root.geometry("900x500")
        self.root.mainloop()


    def crear_archivo(self):
        """
        Crea un archivo CSV llamado 'tareas.csv' con los encabezados definidos en self.headers.
        Registra un mensaje de exito o error en el log y muestra un mensaje en la interfaz en caso de fallo.
        """
        try:
            with open('tareas.csv', 'w', newline='') as f:
                csv_writer = csv.DictWriter(f, fieldnames=self.headers)
                csv_writer.writeheader()
            logging.info('Archivo "tareas.csv" creado con exito')
        except Exception as e:
            self.send_message('Error: No se pudo crear el archivo', 'DANGER')
            logging.error(f'No se pudo crear el archivo "tareas.csv": {e}')
    def leer_tareas(self):
        """
        Lee el archivo 'tareas.csv' y muestra su contenido en la interfaz.
        Limpia el frame antes de cargar los datos.
        Si el archivo no existe, muestra un mensaje y lo crea automáticamente.
        """
        try:
            self.clean_frame()
            with open('tareas.csv', 'r', newline='') as f:
                # Itera sobre cada linea del archivo
                for i, k in enumerate(f.readlines()):
                    # Formatea el texto: reemplaza comas por ' -- ', guiones bajos por espacios y pasa a mayúsculas
                    k = k.replace(',', ' -- ').replace('_', ' ').upper()
                    
                    # Ajusta tamaño y color según si es la cabecera (linea 0)
                    size = 14 if i == 0 else 12
                    color = 'black' if i == 0 else 'gray'
                    
                    label = tk.Label(
                        self.tasks_frame,
                        text=k,
                        fg=color,
                        font=("Arial", size),
                        pady=0
                    )
                    label.grid(row=i, column=1, sticky='nsew', pady=0, ipady=0)
            
            self.tasks_frame.pack(padx=10, pady=1)
            logging.info('Archivo "tareas.csv" leido con exito')
        
        except FileNotFoundError:
            self.send_message(
                'El archivo no existe, se creará uno nuevo llamado "tareas.csv"...',
                'PRIMARY'
            )
            self.crear_archivo()
            logging.info('Creando archivo "tareas.csv"')
    def crear_tarea_ui(self):
        """
        Configura y muestra la interfaz para crear una nueva tarea.
        Limpia el frame actual, carga los campos necesarios y agrega un botón para enviar la tarea.
        Registra logs de exito o error en la carga de la interfaz.
        """
        try:
            self.clean_frame()
            self.tasks_fields()
            
            submit_button = tk.Button(
                self.tasks_frame,
                text='Crear',
                bg='white',
                fg='black',
                width=10,
                cursor='hand2',
                command=self.post_tarea
            )
            submit_button.grid(row=5, column=1, sticky='nsew', padx=5, pady=5)
            
            self.tasks_frame.pack()
            logging.info('Interfaz de creación de tareas cargada con exito')
            
        except FileNotFoundError as e:
            logging.error(f'No se pudo cargar la interfaz de creación de tareas: {e}')

    def post_tarea(self):
        """
        Guarda una nueva tarea en el archivo 'tareas.csv' con los datos ingresados en la interfaz.
        Luego limpia los campos de entrada y muestra un mensaje de confirmación.
        En caso de que el archivo no exista, lo crea automáticamente.
        Maneja errores y registra información relevante en el log.
        """
        try:
            # Obtener la fecha actual para registrar la creación de la tarea
            fecha_hoy = datetime.date(datetime.now())
            # Obtener el próximo ID disponible para la tarea
            id = obtener_id()
            
            # Abrir el archivo CSV en modo append para agregar la nueva tarea
            with open('tareas.csv', 'a', newline='') as f:
                csv_writer = csv.DictWriter(f, fieldnames=self.headers, delimiter=',')
                
                # Escribir la fila con los datos de la tarea recolectados desde los widgets
                csv_writer.writerow({
                    'id': id,
                    'titulo': self.title_entry.get(),
                    'descripcion': self.description_entry.get("1.0", tk.END).strip(),
                    'estado': self.status_entry.get(),
                    'prioridad': self.prioridad_entry.get(),
                    'fecha_creacion': fecha_hoy
                })
            
            # Limpiar los campos de entrada despues de guardar la tarea
            self.title_entry.delete(0, tk.END)
            self.description_entry.delete("1.0", tk.END)
            self.status_entry.delete(0, tk.END)
            self.prioridad_entry.delete(0, tk.END)
            
            # Mostrar mensaje de exito en la interfaz
            label = ttk.Label(self.message_frame, text='Tarea creada con exito', bootstyle='SUCCESS', font=("Arial", 12))
            label.grid(row=0, column=1, sticky='nsew')
            self.message_frame.pack(padx=10, pady=10)
            
            # Registrar en el log la creación exitosa de la tarea
            logging.info('Tarea creada con exito')
        
        except FileNotFoundError:
            # Manejo de error si no existe el archivo, se crea uno nuevo
            self.send_message('El archivo no existe, se creará uno nuevo llamado "tareas.csv"...', 'PRIMARY')
            self.crear_archivo()
            logging.info('Creando archivo "tareas.csv"')
        
        except Exception as e:
            # Mostrar mensaje de error en la interfaz en caso de cualquier excepción
            label = tk.Label(self.root, text='Error al crear la tarea', fg='red', font=("Arial", 12))
            label.pack()
            logging.error(f'Error al crear la tarea: {e}')


    def eliminar_tarea_ui(self):
        """
        Configura y muestra la interfaz para eliminar una tarea por su ID.
        Limpia el frame actual y despliega un campo de entrada para el ID
        y un botón para confirmar la eliminación.
        """
        self.clean_frame()
        try:
            # Etiqueta que indica al usuario que ingrese el ID de la tarea a eliminar
            id_label = tk.Label(self.tasks_frame, text='Elija id de tarea a eliminar:', font=("Arial", 12))
            id_label.grid(row=0, column=0, pady=5)
            
            # Campo de entrada para ingresar el ID
            self.id_entry = tk.Entry(self.tasks_frame, width=10)
            self.id_entry.grid(row=0, column=1, pady=5)
            
            # Botón para borrar la tarea indicada por el ID
            submit_button = tk.Button(
                self.tasks_frame,
                text='Eliminar',
                font=("Arial", 12),
                cursor='hand2',
                command=self.delete_tarea
            )
            submit_button.grid(row=1, column=0, pady=5)
            
            # Mostrar el frame con los widgets agregados
            self.tasks_frame.pack()
            
        except FileNotFoundError:
            logging.info('El archivo no existe, se creará uno nuevo llamado "tareas.csv"...')
            self.crear_archivo()

    
    def actualizar_tarea_ui(self):
        """
        Configura y muestra la interfaz para actualizar una tarea existente.
        Permite ingresar el ID de la tarea, obtener sus datos, modificar los campos y actualizarla.
        """
        self.clean_frame()
        
        # Etiqueta y entrada para el ID de la tarea a actualizar
        id_label = tk.Label(self.tasks_frame, text='Elija id de tarea a actualizar:', font=("Arial", 12))
        id_label.grid(row=0, column=0, pady=5)
        
        self.id_entry = tk.Entry(self.tasks_frame, width=10)
        self.id_entry.grid(row=0, column=1, pady=5)
        
        # Campos para editar la tarea (definidos en self.tasks_fields)
        self.tasks_fields()
        
        # Botón para obtener datos de la tarea con el ID ingresado
        obtener_button = tk.Button(
            self.tasks_frame,
            text='Obtener',
            font=("Arial", 12),
            cursor='hand2',
            command=self.get_tarea
        )
        obtener_button.grid(row=6, column=0, pady=5)
        
        # Botón para actualizar la tarea modificada
        actualizar_button = tk.Button(
            self.tasks_frame,
            text='Actualizar',
            font=("Arial", 12),
            cursor='hand2',
            fg='green',
            command=self.put_tarea
        )
        actualizar_button.grid(row=6, column=1, pady=5)
        
        self.tasks_frame.pack()
 

    def put_tarea(self):
        """
        Actualiza una tarea existente en el archivo 'tareas.csv' con los datos ingresados en la interfaz.
        Busca la tarea por ID, modifica sus campos y guarda todos los registros nuevamente en el archivo.
        Muestra mensajes de exito o error según corresponda.
        """
        try:
            updated_tasks = []
            with open('tareas.csv', 'r', newline='') as f:
                csv_reader = csv.DictReader(f, fieldnames=self.headers, lineterminator='')
                next(csv_reader)  # Saltar cabecera
                for row in csv_reader:
                    if row['id'] == self.id_entry.get():
                        # Actualizar campos de la tarea con valores del UI
                        row['titulo'] = self.title_entry.get()
                        row['descripcion'] = self.description_entry.get("1.0", tk.END).strip()
                        row['estado'] = self.status_entry.get()
                        row['prioridad'] = self.prioridad_entry.get()
                    updated_tasks.append(row)

            # Sobrescribir archivo con tareas actualizadas
            with open('tareas.csv', 'w', newline='') as f:
                csv_writer = csv.DictWriter(f, fieldnames=self.headers, lineterminator='\n')
                csv_writer.writeheader()
                csv_writer.writerows(updated_tasks)

            self.send_message('Tarea actualizada con exito', 'SUCCESS')

        except FileNotFoundError:
            self.send_message('El archivo no existe, se creará uno nuevo llamado "tareas.csv"...', 'PRIMARY')
            self.crear_archivo()
            logging.info('Creando archivo "tareas.csv"')

        except Exception as e:
            self.send_message('Error al actualizar la tarea', 'DANGER')
            logging.error(f'Error al actualizar la tarea: {e}')

    def get_tarea(self):
        """
        Busca en 'tareas.csv' la tarea cuyo ID coincide con el ingresado en el campo correspondiente.
        Si la encuentra, carga sus datos en los campos de entrada para editar.
        Si no existe, muestra un mensaje de error.
        """
        try:
            task = []
            with open('tareas.csv', 'r', newline='') as f:
                csv_reader = csv.DictReader(f, fieldnames=self.headers, lineterminator='')
                for row in csv_reader:
                    if row['id'] == self.id_entry.get():
                        task.append(row)
                        # Insertar datos en los campos de la interfaz
                        self.title_entry.insert(0, row['titulo'])
                        self.description_entry.insert("1.0", row['descripcion'])
                        self.status_entry.insert(0, row['estado'])
                        self.prioridad_entry.insert(0, row['prioridad'])
            
            # Si no se encontró la tarea, lanzar excepción personalizada
            if len(task) == 0:
                raise Exception('La tarea no existe')

        except FileNotFoundError:
            self.send_message('El archivo no existe, se creará uno nuevo llamado "tareas.csv"...', 'PRIMARY')
            self.crear_archivo()

        except Exception as e:
            self.send_message('Error: La tarea no existe', 'DANGER')
            self.delete_fields()

    def delete_tarea(self):
        """
        Elimina una tarea del archivo 'tareas.csv' según el ID ingresado en el campo correspondiente.
        Valida que el ID exista, muestra ventana de error si no, y actualiza el archivo con las tareas restantes.
        Ajusta los IDs para mantenerlos consecutivos y muestra mensajes de éxito o error según corresponda.
        """
        try:
            tareas_filtradas = []
            id_max = obtener_id()
            id_ingresado = self.id_entry.get()
            
            # Validar que el ID ingresado no esté vacío y esté en el rango válido
            if id_ingresado == '' or int(id_ingresado) not in range(1, id_max):
                win = tk.Toplevel()
                win.wm_title("Opción Inválida")
                
                label = ttk.Label(
                    win,
                    text="Error: La tarea no existe",
                    font=("Arial", 12, "bold"),
                    bootstyle="danger"
                )
                label.grid(row=0, column=0, padx=10, pady=10)
                
                button = tk.Button(
                    win,
                    text="Aceptar",
                    command=win.destroy,
                    font=("Arial", 12, "bold"),
                    bg='white',
                    fg='black',
                    width=10,
                    cursor='hand2'
                )
                button.grid(row=1, column=0)
                
                logging.info('Error: La tarea no existe')
                return
            
            # Leer tareas y filtrar la que no coincide con el ID a eliminar
            with open('tareas.csv', 'r', newline='') as f:
                csv_reader = csv.DictReader(f, fieldnames=self.headers, lineterminator='')
                next(csv_reader)  # saltar cabecera
                for tarea in csv_reader:
                    if tarea['id'] != id_ingresado:
                        tareas_filtradas.append(tarea)
            
            # Ajustar IDs para que sigan consecutivos
            if len(tareas_filtradas) > 0:
                tareas_filtradas = modify_id(tareas_filtradas)
            
            # Sobrescribir el archivo con las tareas filtradas
            with open('tareas.csv', 'w', newline='') as f:
                csv_writer = csv.DictWriter(f, fieldnames=self.headers, lineterminator='\n')
                csv_writer.writeheader()
                for tarea in tareas_filtradas:
                    csv_writer.writerow(tarea)
            
            self.send_message('Tarea eliminada con éxito', 'SUCCESS')
        
        except FileNotFoundError:
            self.send_message('El archivo no existe, se creará uno nuevo llamado "tareas.csv"...', 'PRIMARY')
            self.crear_archivo()
            logging.info('Creando archivo "tareas.csv"')
        
        except Exception as e:
            self.send_message('Error: La tarea no existe', 'DANGER')
            logging.error(f'Error al eliminar tarea: {e}')

    def clean_frame(self):
        """Limpia los frames de la interfaz."""
        frames = [self.tasks_frame, self.message_frame]
        
        for frame in frames:
            for widget in frame.winfo_children( ):
                widget.destroy()
            frame.pack_forget()
    
    def tasks_fields(self):
            """
            Crea los elementos entry para la entrada de datos.
            """
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
        """Limpia los valores de los elementos entry."""
        self.title_entry.delete(0,'end')
        self.description_entry.delete("1.0", tk.END)
        self.status_entry.delete(0,'end')
        self.prioridad_entry.delete(0,'end')
    def send_message(self,texto,color):
        """
        Envia mensaje customizado a la interfaz
        """
        label = ttk.Label(self.message_frame, text=texto, bootstyle=color ,font=("Arial", 12))
        label.grid(row=0, column=1, sticky='nsew')
        self.message_frame.pack(padx=10, pady=10)


Task_Manager()