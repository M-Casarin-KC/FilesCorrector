# -*- coding: utf-8 -*-

import os
from PyMultiDictionary import MultiDictionary
from .Logger import Logger
from .utils import Colors

class CorrectorIncidentes:
    """
    Actúa como un agente que corrige aquellos archivos que deben ser corregidos,
    requiere que se le indiquen los archivos.
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

    log = ""

    def __init__(self, correccionesDetectadas: list[tuple[str, str]]):
        self.correccionesDetectadas = correccionesDetectadas
        self.casosEspeciales = []
        self.corregirArchivos = []
        self.log = ""
        self.cantidadIncidenciasCompletadas = 0 
        self.cantidadIncidenciasFallidas = 0 


    def _consulta(self, palabra: str):
        """
        Consulta la definición de una palabra en el diccionario.
        """
        if not isinstance(palabra, str):
            raise TypeError("La palabra debe ser un string.")

        try:
            diccionario = MultiDictionary()
            definicion = diccionario.meaning("es", palabra)
            if definicion:
                return definicion
        except Exception as e:
            print(f"Error al consultar '{palabra}': {e}")

        return None

    def _mejorCandidato(self, name: str):
        """
        Intenta encontrar el mejor candidato reemplazando el carácter '_'
        por vocales acentuadas.
        """
        vocales = ["á", "é", "í", "ó", "ú"]
        posibles = [name.replace("_", x) for x in vocales]

        for posible in posibles:
            defi = self._consulta(posible)
            
            if defi[0]:
                return posible  # Retorna el primer candidato válido
            
        return name  # Si no se encuentra un candidato válido, retorna el original

    def _corregirEspeciales(self, directory: str, file: str):
        """
        Trata los casos especiales, aquellos que contienen '_'.
        """
        reconocidos = {
            "Pr_stamo": "Prestamo", 
            "PR_STAMO": "PRESTAMO", 
            "inter_s":  "interes",
            "Inter_s":  "Interes", 
            "INTER_S":  "INTERES", 
        }

        inicial = file 

        for rec in reconocidos.keys(): 
            if rec in file: 
                file = file.replace(rec, reconocidos[rec])

        if inicial == file: 
            nuevo_nombre = file
            if nuevo_nombre != file:  # Solo actúa si se generó un nuevo nombre
                self._generarNuevoNombre(directory, nuevo_nombre)
        
        else: 
            self._generarNuevoNombre(directory, file)


    def _generarNuevoNombre(self, directory: str, file: str):
        """
        Quita los acentos del nombre del archivo y genera un nuevo nombre.
        """
        original_file = file

        for bad_char, good_char in self.reemplazos.items():
            file = file.replace(bad_char, good_char)
            file = file.replace(bad_char.upper(), good_char.upper())

        # self.casosEspeciales.append((directory, file))
        nuevo_nombre = os.path.join(directory, file)
        viejo_nombre = os.path.join(directory, original_file)

        # Guardar los archivos a corregir
        self.corregirArchivos.append((viejo_nombre, nuevo_nombre))


    def corregir_archivos(self):
        """
        Itera sobre los archivos detectados, genera los nuevos nombres y corrige los especiales.
        """
        # Procesar archivos normales

        try: 
            for correccion in self.correccionesDetectadas:
                self._generarNuevoNombre(correccion[0], correccion[1])

            # Ahora en corregir archivos estan los nuevos nombre s

            self.rename_files()
            # for input in self.corregirArchivos:
            #     old_fname = input[0]
            #     new_fname = input[1]

        except Exception as e: 
            Colors.p("RED",f"Error al corregir archivos: {e}")
        

        # for especial in self.casosEspeciales:
        #     self._corregirEspeciales()
      

    def rename_files(self):
        """
        Renombra los archivos procesados:
        """
        countSuccess = 0 
        countFailed = 0 

        for viejo_nombre, nuevo_nombre in self.corregirArchivos:

            try:
                # Mueve viejo_nombre a nuevo_nombre (sustituye si existe)
                os.rename(viejo_nombre, nuevo_nombre)
                info = f"{viejo_nombre} Renombrado a: {nuevo_nombre}"
                countSuccess += 1
                Logger.info(info)


            except Exception as e:
                info = f"Error al renombrar {viejo_nombre} como: {nuevo_nombre} || Error: {e}"
                countFailed += 1 
                Logger.error(info)            


        self.cantidadIncidenciasCompletadas = countSuccess
        self.cantidadIncidenciasFallidass = countFailed

        return True
