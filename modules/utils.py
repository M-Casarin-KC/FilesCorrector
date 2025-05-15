import os 
import glob
from PyMultiDictionary import MultiDictionary


def consulta(palabra: str): 

    if not isinstance(palabra, str): 
        raise TypeError(f"La palabra debe ser un string")

    diccionario = MultiDictionary()
    definicion = diccionario.meaning("es", palabra)

    if definicion:
        print(f"Definición de '{palabra}':\n {definicion}")
        return definicion
        
    else: 
        print("No se encuentra en el diccionario la palabra: ", palabra)
        return None


