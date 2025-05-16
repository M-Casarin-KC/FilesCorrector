import logging
import sys
import os
import glob

"""
El modulo denota una clase que modela un logger, donde podremos registrar los 
eventos relevantes.
"""

# Forzar stdout y stderr a UTF-8 en Windows
if hasattr(sys.stdout, "reconfigure"):  
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):  
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

class Logger:
    # Asegurar existencia del directorio de logs
    os.makedirs("Logs", exist_ok=True)

    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.INFO)

    # FileHandler con encoding UTF-8
    file_handler = logging.FileHandler("Logs/app.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(file_formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    @staticmethod
    def info(message: str):
        """
        Guarda un log del tipo INFO en el archivo de logs y consola.
        """
        Logger.logger.info(message)

    @staticmethod
    def error(message: str):
        """
        Guarda un log del tipo ERROR en el archivo de logs y consola.
        """
        Logger.logger.error(message)

    @staticmethod
    def warning(message: str):
        """
        Guarda un log del tipo WARNING en el archivo de logs y consola.
        """
        Logger.logger.warning(message)


if __name__ == '__main__': 

    Logger.error("Ejemplo de error")
    Logger.info("Ejemplo de info ")
    Logger.warning("Ejemplo de warning")
    Logger.warning("No se leer ni escribir, solo se deletrear")
    Logger.warning("Que viva la fraternidad Universal")