def obtener_id():
    with open('tareas.csv','r') as f:
        next(f)
        id = len(f.readlines()) + 1
        return id
    
def modify_id(tareas_filtradas):

    for i,k in zip(tareas_filtradas,range(1,len(tareas_filtradas)+1)):
        i['id'] = k
    return tareas_filtradas