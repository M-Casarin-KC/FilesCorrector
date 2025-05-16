import os
import shutil
import pytest
from modules.DetectorIncidentes import DetectorIncidentes

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
    shutil.rmtree(TEST_DIR)


def test_existeIncidencia(setup_test_environment):
    """
    Verifica que el método _existeIncidencia detecte correctamente las incidencias.
    """
    detector = DetectorIncidentes(TEST_DIR)

    # Archivos sin incidencias
    assert not detector._existeIncidencia("archivo1.txt")
    assert not detector._existeIncidencia("documento.docx")

    # Archivos con incidencias
    assert detector._existeIncidencia("áccento.txt")
    assert detector._existeIncidencia("ñandú.pdf")
    assert detector._existeIncidencia("Pr�stamo char.txt")


def test_detectar_incidentes(setup_test_environment):
    """
    Verifica que el método detectar_incidentes encuentre todos los archivos con incidencias.
    """
    detector = DetectorIncidentes(TEST_DIR)
    detector.detectar_incidentes()

    expected_files = [
        (TEST_DIR, "áccento.txt"),
        (TEST_DIR, "ñandú.pdf"),
        (TEST_DIR, "Pr�stamo char.txt")
    ]

    assert set(detector.archivosPorCorregir) == set(expected_files)


def test_directory_not_found():
    """
    Verifica que se lance una excepción cuando el directorio no existe.
    """
    with pytest.raises(FileNotFoundError):
        DetectorIncidentes("directorio_inexistente")
