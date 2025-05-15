# -*- coding: utf-8 -*-

import os 
import glob
from PyMultiDictionary import MultiDictionary


class CorrectorIncidentes:
    """
    Actua como un agente que corrige aquellos archivos que deberan ser corregidos,
    requiere que se le indiquen los archivos 
    """

    reemplazos = {
        "ñ": "n",
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u", 
        "�": "_"
    }


    def __init__(self, correccionesDetectadas: list[tuple[str, str]]): 
        self.correccionesDetectadas = correccionesDetectadas
        self.casosEspeciales = []
        self.corregirArchivos = []

        # Iterar sobre las correcciones detectadas, para gener el nuevo nombre 
        for correcciones in self.correccionesDetectadas: 
            self._generarNuevoNombre(correccionesDetectadas[0], correccionesDetectadas[1])

        if len(self.casosEspeciales) > 0 : 
            for directory, file in self.casosEspeciales: 
                self._corregirEspeciales(directory, file)


    def _consulta(self, palabra: str): 

        if not isinstance(palabra, str): 
            raise TypeError(f"La palabra debe ser un string")

        diccionario = MultiDictionary()
        definicion = diccionario.meaning("es", palabra)

        if definicion:
            print(f"Definicion de '{palabra}':\n {definicion}")
            return definicion
            
        else: 
            print("No se encuentra en el diccionario la palabra: ", palabra)
            return None
        

    def _mejorCandidato(self, name):
        
       aux = ["á", "é", "í", "ó", "ú"]
       posibles = [name.replace("_", x) for x in aux]

       for posible in posibles: 
           defi = self._consulta(posible)

           if defi[0]:
                return posible


    def _corregirEspeciales(self, directory, file): 
        """
        Se encarga de tratar los casos especiales, aquellos que no pueden ser corregidos por el algoritmo
        """

        # Si no es un nombre válido, lo reemplaza por el mejor candidato
        nuevo_nombre = self._mejorCandidato(file)
        self._generarNuevoNombre(directory, nuevo_nombre)


    def _generarNuevoNombre(self, directory, file): 
        """
        Quita los acentos del nombre de los archivos 
        """
        aux = file

        for bad_char, good_char in self.reemplazos.items():
            file = file.replace(bad_char, good_char)
            file = file.replace(bad_char.upper(), good_char.upper())

        # Seperar los casos especiales 
        if '_' in file: 
            self.casosEspeciales.append((directory, file))

        else: 
            nuevo_nombre = os.path.join(directory, file)
            viejo_nombre = os.path.join(directory, aux)

            # Guardarlos en la lista de tuplas 
            self.corregirArchivos.append((viejo_nombre, nuevo_nombre))



    def corregir_archivos(self): 
        """
        Se encarga de corregir los archivos, renombrandolos 
        """
        for viejo_nombre, nuevo_nombre in self.corregirArchivos: 
            os.rename(viejo_nombre, nuevo_nombre)
            result = f"Renombrado: {viejo_nombre} -> {nuevo_nombre}"
            print(result)

        return True
        
        