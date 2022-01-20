from PyQt5.QtWidgets import *


# Used tutorial for PyQt5: https://build-system.fman.io/pyqt5-tutorial

class AssetApplication(QDialog):
    def __init__(self, time, parent=None):
        super(AssetApplication, self).__init__(parent)

        self.time = time
        self.setStyle('Fusion')

        # Setting styleSheet
        with open("style.qss", "r") as styleSheet:
            self.setStyleSheet(styleSheet.read())

        selectedTimeLabel = QLabel(time)
        timeLabel = QLabel("&Time:")
        timeLabel.setBuddy(selectedTimeLabel)

        upperLeftLayout = QHBoxLayout()
        upperLeftLayout.addWidget(timeLabel)
        upperLeftLayout.addWidget(selectedTimeLabel)

        mainLayout = QGridLayout()

        self.setWindowTitle("Asset Status")
        self.setLayout(mainLayout)

        def createpersonGroupBox(self):
            self.personGroupBox = QGroupBox("Person")
            personInsideLabel = QLabel()
            if time > 50:
                personInsideLabel.setText("There is currently a person inside.")
            else:
                personInsideLabel.setText("There is currently no one inside.")

    # function to calculate KPI from sensor DATA
    # def telemetryKPI(self):
