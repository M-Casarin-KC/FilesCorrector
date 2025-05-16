import os 
import glob
from PyMultiDictionary import MultiDictionary


def consulta(palabra: str): 

    if not isinstance(palabra, str): 
        raise TypeError(f"La palabra debe ser un string")

    diccionario = MultiDictionary()
    definicion = diccionario.meaning("es", palabra)

    if definicion:
        print(f"Definici�n de '{palabra}':\n {definicion}")
        return definicion
        
    else: 
        print("No se encuentra en el diccionario la palabra: ", palabra)
        return None


TEST_DIR = "test_files"
SUBTESTS_DIR = [os.path.join(TEST_DIR, f"Sub{i}") for i in range(3)]

def crear_entorno_dev():
    """
    """
    os.makedirs(TEST_DIR, exist_ok=True)

    # Archivos sin incidencia
    open(os.path.join(TEST_DIR, "archivo1.txt"), "w").close()
    open(os.path.join(TEST_DIR, "documento.docx"), "w").close()

    # Archivos que tendran la incidencia 
    open(os.path.join(TEST_DIR, "áccento.txt"), "w").close()
    open(os.path.join(TEST_DIR, "Áandú.pdf"), "w").close()
    open(os.path.join(TEST_DIR, "Pr�stamo char.txt"), "w").close()
    open(os.path.join(TEST_DIR, "ñandú.pdf"), "w").close()

    open(os.path.join(TEST_DIR, "Péccento ÁCñ.txt"), "w").close()

    for sub in SUBTESTS_DIR: 
        os.makedirs(sub, exist_ok=True)
        # Archivos sin incidencia
        open(os.path.join(sub, "archivo1.txt"), "w").close()
        open(os.path.join(sub, "documento.docx"), "w").close()

        # Archivos que tendran la incidencia 
        open(os.path.join(sub, "áccento.txt"), "w").close()
        open(os.path.join(sub, "Áandú.pdf"), "w").close()
        open(os.path.join(sub, "Pr�stamo char.txt"), "w").close()
        open(os.path.join(sub, "ñandú.pdf"), "w").close()

        open(os.path.join(sub, "Péccento ÁCñ.txt"), "w").close()

from colorama import Style, Fore

from typing import Literal
class Colors(): 
    
    @staticmethod 
    def p(color: Literal['RED','BLUE', 'GREEN', 'YELLOW', 'CYAN'], texto):
        
        colores= {
            'RED': Fore.RED,
            'BLUE': Fore.BLUE,
            'GREEN': Fore.GREEN, 
            'YELLOW': Fore.YELLOW,
            'CYAN' : Fore.CYAN
        }

        try: 
            print(colores[color], texto)
            print(Style.RESET_ALL)

        except KeyError as e: 
            Colors.p(color='RED', texto=f"Error! El color {color} no esta disponible, use: {[x for x in colores.keys()]}")


if __name__ == "__main__":
    Colors.p('RED', 'SOY ROJO')
    Colors.p('BLUE', 'SOY AZUL')
    Colors.p(color="YELLOW", texto="SOY AMARILLO")
    Colors.p('GREEN', 'SOY VERDE')
    Colors.p('CYAN', 'SOY CYAN')
    Colors.p('black', 'SOY CYAN')

    crear_entorno_dev()