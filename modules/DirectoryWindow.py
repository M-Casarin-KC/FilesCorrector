from .CorrectorIncidentes import CorrectorIncidentes
from .DetectorIncidentes import DetectorIncidentes
from .Logger import Logger
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QProgressBar, QMessageBox
from PySide6.QtGui import QIcon
import sys
from .utils import Colors
import os

class DirectoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_folder = None
        self.initUI()

    def initUI(self):
        # Establecer icono
        self.setWindowIcon(QIcon("assets/FilesCorrectorIcono.png"))

        # Cargar estilo desde el archivo QSS
        with open("styles.qss", "r") as file:
            self.setStyleSheet(file.read())

        self.setWindowTitle('Files Corrector')
        self.setGeometry(300, 300, 450, 250)

        # Layout principal
        self.layout = QVBoxLayout()

        # Botón para seleccionar carpeta
        self.select_button = QPushButton('Seleccionar Carpeta')
        self.select_button.clicked.connect(self.pintar_folder_dialog)
        self.layout.addWidget(self.select_button)

        # Etiqueta para mostrar la carpeta seleccionada
        self.status_label = QLabel("No se ha seleccionado ninguna carpeta")
        self.layout.addWidget(self.status_label)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)  # Oculta inicialmente
        self.layout.addWidget(self.progress_bar)

        # Botón para iniciar el proceso
        self.start_button = QPushButton('Iniciar Proceso')
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.iniciar_proceso)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def pintar_folder_dialog(self):
        """
        Muestra el cuadro de diálogo para seleccionar carpeta
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder_path:
            self.selected_folder = folder_path
            self.status_label.setText(f"Carpeta seleccionada: {folder_path}")
            self.start_button.setEnabled(True)
        else:
            self.status_label.setText("No se seleccionó ninguna carpeta")
            self.start_button.setEnabled(False)

    def iniciar_proceso(self):
        """
        Función proporcionada por el usuario. NO SE MODIFICA.
        """
        if self.selected_folder:
            try:

                detector = DetectorIncidentes(self.selected_folder)
                detector.detectar_incidentes()

                # Obtenemos los archivos que tienen incidencias 
                archivos_incidentes = detector.archivosPorCorregir
                # Colors.p("RED", f"{archivos_incidentes}")

                if archivos_incidentes: 
                # Mostrar barra de progreso
                    self.progress_bar.setVisible(True)
                    self.progress_bar.setValue(50)

                    # Ejecutar todo en el corrector 
                    corrector = CorrectorIncidentes(archivos_incidentes)
                    proceso = corrector.corregir_archivos()

                    # Finalizar barra de progreso
                    self.progress_bar.setValue(100)

                    if proceso:
                        completadas, fallidas = str(corrector.cantidadIncidenciasCompletadas), str(corrector.cantidadIncidenciasFallidas)
                        resultado = f"Limpieza terminada! Completadas: {completadas}, Fallidas: {fallidas}"
                        self.status_label.setText("Proceso de corrección completado!")
                        Logger.error(resultado)

                        # Resetear estado
                        self.selected_folder = None
                        self.start_button.setEnabled(False)
                        self.progress_bar.setVisible(False)

                    else:
                        self.status_label.setText("Corrección completada.")
                        Colors.p("GREEN", "Correccion completada")
                else:
                    self.status_label.setText("La carpeta no mostro incidencias.")

                    Colors.p("GREEN", "La Carpeta no mostro incidencias")


            except Exception as e:
                self.status_label.setText(f"Error: {e}")
                Logger.error(f"Error: {e}")
                QMessageBox.critical(self, "Error", f"Ocurrió un error durante el proceso: {e}")

        else:
            self.status_label.setText("No se ha seleccionado una carpeta.")
