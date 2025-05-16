import os
import shutil
import pytest
from modules.DetectorIncidentes import DetectorIncidentes
from modules.CorrectorIncidentes import CorrectorIncidentes

TEST_DIR = "test_files"


@pytest.fixture(scope="module")
def setup_test_environment():
    """
    Configura un entorno de prueba creando un conjunto de archivos con y sin incidencias.
    """
    os.makedirs(TEST_DIR, exist_ok=True)

    # Archivos sin incidencia
    open(os.path.join(TEST_DIR, "archivo1.txt"), "w").close()
    open(os.path.join(TEST_DIR, "documento.docx"), "w").close()

    # Archivos que tendran la incidencia 
    open(os.path.join(TEST_DIR, "áccento.txt"), "w").close()
    open(os.path.join(TEST_DIR, "ñandú.pdf"), "w").close()
    open(os.path.join(TEST_DIR, "Pr�stamo char.txt"), "w").close()

    yield

    # Limpiar archivos después de las pruebas
    # shutil.rmtree(TEST_DIR)

def test_ejecutarTodoProceso(setup_test_environment): 


    detector = DetectorIncidentes(TEST_DIR)
    detector.detectar_incidentes()

    # Obtenemos los archivos que tienen incidencias 
    archivos_incidentes = detector.archivosPorCorregir

    # Ejecutar todo en el corrector 
    corrector = CorrectorIncidentes(archivos_incidentes)

    corrector.corregir_archivos()


    assert len(corrector.log) > 0




