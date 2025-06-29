def obtener_id():
    """
    Obtiene el siguiente ID disponible para una nueva tarea.
    """
    with open('tareas.csv','r') as f:
        next(f)
        id = len(f.readlines()) + 1
        return id
    
def modify_id(tareas_filtradas):
    """
    Reformate los id de las tareas para que esten en orden
    """
    for i,k in zip(tareas_filtradas,range(1,len(tareas_filtradas)+1)):
        i['id'] = k
    return tareas_filtradas