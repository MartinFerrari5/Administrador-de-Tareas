import logging
from pathlib import Path

def start_logging():
    """
    Inicializa el modulo de logging

        - Si existe el archivo logs.log se instancia en modo append
        - Si no existe lo crea
    """
    
    if Path('./logs.log').is_file():
        logging.basicConfig(filename='logs.log',filemode='a',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(filename='logs.log',filemode='w',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')