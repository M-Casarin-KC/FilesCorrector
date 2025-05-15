from .CorrectorIncidentes import CorrectorIncidentes
from .DetectorIncidentes import DetectorIncidentes
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel
import sys


class DirectoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_folder = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Selector de Carpeta')
        self.setGeometry(300, 300, 400, 150)

        # Crear el layout
        self.layout = QVBoxLayout()

        # Botón para seleccionar carpeta
        self.select_button = QPushButton('Seleccionar Carpeta')
        self.select_button.clicked.connect(self.show_folder_dialog)
        self.layout.addWidget(self.select_button)

        # Etiqueta para mostrar la carpeta seleccionada
        self.status_label = QLabel("No se ha seleccionado ninguna carpeta")
        self.layout.addWidget(self.status_label)

        # Botón para iniciar
        self.start_button = QPushButton('Iniciar Proceso')
        self.start_button.setEnabled(False)  # Desactivado hasta seleccionar carpeta
        self.start_button.clicked.connect(self.iniciar_proceso)
        self.layout.addWidget(self.start_button)

        # Aplicar el layout
        self.setLayout(self.layout)

    def show_folder_dialog(self):
        """
        Muestra el cuadro de diálogo para seleccionar una carpeta.
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
        Inicia el proceso de detección y corrección de archivos.
        """
        if self.selected_folder:
            try:
                # Crear instancia del detector
                detector = DetectorIncidentes(self.selected_folder)
                detector.detectar_incidentes()

                # Archivos con incidencias
                archivos_incidentes = detector.archivosPorCorregir
                print(f"Archivos detectados con incidencias: {archivos_incidentes}")

                # Si hay archivos por corregir, iniciar el corrector
                if archivos_incidentes:
                    corrector = CorrectorIncidentes(archivos_incidentes)
                    proceso = corrector.corregir_archivos(archivos_incidentes)

                    if proceso:
                        self.status_label.setText("Proceso de corrección completado.")
                        print("Proceso de corrección completado.")
                        self.selected_folder = None
                        self.start_button.setEnabled(False)
                    else:
                        self.status_label.setText("No se encontraron archivos a corregir.")
                else:
                    self.status_label.setText("No se encontraron archivos con incidencias.")

            except Exception as e:
                self.status_label.setText(f"Error: {e}")
                print(f"Error: {e}")
        else:
            self.status_label.setText("No se ha seleccionado una carpeta.")

