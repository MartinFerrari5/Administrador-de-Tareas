# <h1 style="text-align:center">Administrador de Tareas</h1>

<div style="height:50vh;" align='center'><img src="https://static.vecteezy.com/system/resources/previews/005/320/884/original/task-manager-illustration-3d-modern-awesome-flat-landing-page-free-vector.jpg"></div>
</div>

## Tabla de contenido
1. [Contexto](#📖-conmtexto)
2. [Herramientas y Librerias Utilizadas](#⚙️-herramientas-y-librerias-utilizadas)
3. [Estuctura del Proyecto](#📁-estructura-del-proyecto)
4. [Instrucciones](#🖊️-instrucciones)
5. [Autor](#👤-autor) 

## 📖 Contexto

<div>En esta oportunidad, presento un Administrador de Tareas en donde se podrá:
    <li>Listar las tareas</li>
    <li>Crear un titulo, descripcion, estado, prioridad</li>
    <li>Actualizar las tareas</li>
    <li>Eliminar las tareas</li>
<div>

## ⚙️ Herramientas y Librerias Utilizadas
Para el siguiente proyecto se hizo uso de las siguientes herramientas y librerias (el conocimiento sobre los mismos no require de un nivel avanzado para el entendimiento del proyecto):
1. ***Python***
2. ***Manejo de archivos con `csv`***
3. ***Creacion de logs con `logging`***
4. ***Interfaz grafica con `tkinter`***
5. ***Estilos a la interfaz con `ttkbootstrap`***
6. ***Manejo de fechas con `datetieme`***

## 📁 Estructura del proyecto
`/main.py`: Archivo que contiene la logica y el armado de la GUI <br>
`/logs.py`: Archivo que instancia el funcionamiento de los _logs_. <br>
`/id_functions.py`: Archivo que funciona como modulo para el manejo de **id** de las tareas.<br>
`tareas.csv` y `logs.log`: Almacenan las tareas y los logs. Estos archivos pueden ser eliminados.

## 🖊️ Instrucciones

#### 1) Clona el repositorio:
```
git clone https://github.com/MartinFerrari5/first_project.git
```

- Es recomendado usar un entorno virtual (venv):
### Crea entorno virtual.
```bash
python -m venv environment_name
```

- Activatar:
``Windows``: venv\Scripts\activate

``Mac/Linux``: venv/bin/activate

#### 2) Instalar librerias.
```bash
python -m pip install -r requirements.txt
```
#### 3) En la terminal ejecute.
```bash
python main.py
```

## 👤 Autor
Este proyecto fue realizado por Martin Ferrari. Muchas gracias a todos por leer, no dudes en contactarme a mi <a href="https://www.linkedin.com/in/martin-ferrari-bb0547219/">LinkedIn</a> ante cualquier duda.
