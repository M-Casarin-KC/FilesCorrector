import os 
import shutil 
import pytest
from modules.CorrectorIncidentes import CorrectorIncidentes

TEST_DIR = "test_files"

# Configuramos nuestro entorno de pruebas 
@pytest.fixture(scope="module")
def setup_test_enviroment(): 
    
    # Simular el directorio 
    os.makedirs(TEST_DIR, exist_ok=True)

    # Archivos sin incidentes 
    open(os.path.join(TEST_DIR, "archivo1.txt"), "w").close()
    open(os.path.join(TEST_DIR, "documento.docx"), "w").close()

    # Archivos que tendran la incidencia 
    open(os.path.join(TEST_DIR, "áccento.txt"), "w").close()
    open(os.path.join(TEST_DIR, "ñandú.pdf"), "w").close()
    open(os.path.join(TEST_DIR, "Pr�stamo char.txt"), "w").close()
    
    # Lista de incidentes para pasar al corrector 


    yield 
    shutil.rmtree(TEST_DIR)


def test_consulta(setup_test_enviroment): 
    test_fnames_incidentes = [
        (TEST_DIR, "áccento.txt"),
        (TEST_DIR, "ñandú.pdf"), 
        (TEST_DIR, "Pr�stamo char.txt")    
    ]
    palabras = ["Libertad", "Igualdad", "Fraternidad"]

    corrector = CorrectorIncidentes(test_fnames_incidentes)

    definiciones = ["" for _ in range(len(palabras))] 

    for i, palabra in enumerate(palabras): 
        definiciones[i] = corrector._consulta(palabra=palabra)

        assert definiciones

    # cardinalidad = [len(definiciones[i]) for i in range(len(palabras))]




def test_mejorCandidato(setup_test_enviroment): 
    test_fnames_incidentes = [
        (TEST_DIR, "áccento.txt"),
        (TEST_DIR, "ñandú.pdf"), 
        (TEST_DIR, "Pr�stamo char.txt")    
    ]

    corrector = CorrectorIncidentes(test_fnames_incidentes)

    palabras = ["Pr_stamo", "Inter_s", "M_dico", "Canci_n"]

    combinaciones = [corrector._mejorCandidato(palabra) for palabra in palabras]

    candidatos_esperados = ["Préstamo", "Interés", "Médico", "Canción"]

    assert (set(combinaciones) == set(candidatos_esperados))


def test_generarNuevoNombre(setup_test_enviroment): 
    test_fnames_incidentes = [
        (TEST_DIR, "áccento.txt"),
        (TEST_DIR, "ñandú.pdf"), 
        (TEST_DIR, "Pr�stamo char.txt")    
    ]

    corrector = CorrectorIncidentes(test_fnames_incidentes)

    for input in test_fnames_incidentes: 
        dir = input[0]
        file = input[1]

        corrector._generarNuevoNombre(dir, file)

    f1v = os.path.join(TEST_DIR, "áccento.txt")
    f1n = os.path.join(TEST_DIR, "accento.txt")

    f2v = os.path.join(TEST_DIR, "ñandú.pdf")
    f2n = os.path.join(TEST_DIR, "nandu.pdf")


    assert (set(corrector.corregirArchivos) == set([(f1v, f1n), (f2v, f2n)]))

    
