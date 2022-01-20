from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from csv_interface import *


class AssetApplication(QDialog):
    def __init__(self, time, parent=None):
        super(AssetApplication, self).__init__(parent)

        self.time = time
        self.setStyle('Fusion')

        # Setting styleSheet
        with open("style.qss", "r") as styleSheet:
            self.setStyleSheet(styleSheet.read())

        window = QWidget()
        window.setWindowTitle("Asset Status")
        layout = QVBoxLayout()

        window.setLayout(layout)
        window.show()
        self.exec()
    # function to calculate KPI from sensor DATA
    #def telemetryKPI(self):
