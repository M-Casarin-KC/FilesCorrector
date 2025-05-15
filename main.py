from modules.CorrectorIncidentes import CorrectorIncidentes
from modules.DetectorIncidentes import DetectorIncidentes
from modules.DirectoryWindow import DirectoryWindow
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel
import sys



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DirectoryWindow()
    window.show()
    sys.exit(app.exec())
