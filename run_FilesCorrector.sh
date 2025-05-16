#!/bin/bash

# Ruta del proyecto
PROJECT_DIR="./Files_Corrector"
VENV_DIR="$PROJECT_DIR/venv"
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"
MAIN_FILE="$PROJECT_DIR/main.py"

echo "=================================="
echo "       Files Corrector Setup      "
echo "=================================="

# Paso 1: Crear entorno virtual
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando entorno virtual en $VENV_DIR..."
    python -m venv "$VENV_DIR"
else
    echo "El entorno virtual ya existe."
fi

# Paso 2: Activar el entorno virtual
echo "Activando el entorno virtual..."
source "$VENV_DIR/Scripts/activate"

if [ $? -ne 0 ]; then
    echo "Error al activar el entorno virtual."
    exit 1
fi

# Paso 3: Instalar los requerimientos
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Instalando requerimientos..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "Archivo requirements.txt no encontrado en $REQUIREMENTS_FILE"
    exit 1
fi

# Paso 4: Ejecutar la aplicación
if [ -f "$MAIN_FILE" ]; then
    echo "Ejecutando la aplicación..."
    python "$MAIN_FILE"
else
    echo "Archivo main.py no encontrado en $MAIN_FILE"
    exit 1
fi

# Desactivar el entorno virtual al finalizar
deactivate

echo "Proceso completado."
