import os 
import glob



class DetectorIncidentes: 
    """
    Actua como un agente que detecta aquellos archivos que deberan ser corregidos

    """ 
    
    elementosIncidencia = ['á', 'é', 'í', 'ó', 'ú', 'ñ', '�']

    def __init__(self, dir_path: str): 
        self.dir_path = dir_path
        self.archivosPorCorregir = []

        if not os.path.exists(self.dir_path):
            raise FileNotFoundError(f"El directorio {self.dir_path} no existe.")

        self.recorrido = os.walk(self.dir_path) # El primer elemento mapeará todo


    def _existeIncidencia(self, nombre_archivo: str) :
        for incidencia in self.elementosIncidencia:
            if incidencia.upper() in nombre_archivo.upper().split():
                # Basta la existencia de almenos uno 
                return True
            
            return False


    def detectar_incidentes(self): 

        for dir, sub, files in self.recorrido: 
            print(f"\nRuta Actual: {dir}")

            if len(files) == 0: 
                print(f"La ruta actual no tiene archivos")
                continue

            print(f"Cuenta con {len(files)} archivos")
            for indice_file, file in enumerate(files): 
                print(file)
                # Verificar si existe incidencia en el archivo 
                if self._existeIncidencia(file): 
                    print(f"El archivo {file} tiene incidencia")
                    # Si existe incidencia, se corrige el nombre del archivo
                    self.archivosPorCorregir.append((dir, file))


    
