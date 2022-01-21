from PyQt5.QtWidgets import *
import pandas as pds
from dateutil.parser import parse
from pyqtgraph import *
import pyqtgraph as pg
from csv_interface import generateRange

# Used tutorial for PyQt5: https://build-system.fman.io/pyqt5-tutorial

class AssetApplication(QDialog):
    def __init__(self, str_time, parent=None):
        super(AssetApplication, self).__init__(parent)
        self.str_time = str_time
        self.unix = parse(str_time).timestamp()

        # Setting styleSheet
        with open("style.qss", "r") as styleSheet:
            self.setStyleSheet(styleSheet.read())

        time_short = str_time[0:10]  # cut string for nicer output
        # Create Labels Time = inputTime
        selectedTimeLabel = QLabel(str(time_short))  # user input time
        timeLabel = QLabel("&Time:")  # create label
        timeLabel.setBuddy(selectedTimeLabel)  # connect label with input time

        # Create all the parts
        self.createStatusBox()
        self.createpersonGroupBox()
        # Create upper part (outside of Group boxes)
        upperLeftLayout = QHBoxLayout()
        upperLeftLayout.addWidget(timeLabel)
        upperLeftLayout.addWidget(selectedTimeLabel)
        upperLeftLayout.addStretch(1)

        # Main Layout (this will actually be shown, all other parts should be nested inside this)
        mainLayout = QGridLayout()
        # Add all boxes to main layout
        mainLayout.addLayout(upperLeftLayout, 0, 0, 1, 1)
        mainLayout.addWidget(self.personGroupBox, 1, 0)
        mainLayout.addWidget(self.statusBox, 2, 0)

        # Set main layout parameters, so it looks better
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        # Set the layout to main layout, so it actually gets shown
        self.setLayout(mainLayout)
        self.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle("Asset Status")


    def createpersonGroupBox(self):
        self.personGroupBox = QGroupBox("Person")
        personInsideLabel = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(personInsideLabel)
        layout.addStretch(1)
        self.personGroupBox.setLayout(layout)

        # dummy, so the other path is reachable

        if parse(self.str_time).timestamp() > 50:
            personInsideLabel.setText("There is currently a person inside.")
            personInsideLabel.setStyleSheet('color: yellow;')
        else:
            personInsideLabel.setText("There is currently no one inside.")
            personInsideLabel.setStyleSheet('color: green;')

    def createStatusBox(self):
        self.statusBox = QGroupBox("Current Status")
        layout = QVBoxLayout()
        statusLabel = QLabel("Status:")

        layout.addWidget(statusLabel, 0, 0)

        self.statusBox.setLayout(layout)

    def createGraphGroupBox(self):
        self.graphGroupBox = QGroupBox("Graphs:")
        layout = QVBoxLayout()

        dataFrame = generateRange(self.unix)
        time = dataFrame['ts']

        #lpg
        lpgGraph = pg.PlotWidget()
        lpgValue = dataFrame['lpg']
        lpgGraph.plotItem.setTitle('LPG Value')
        lpgGraph.plotItem.plot(time, lpgValue)
        layout.addWidget(lpgGraph, 0, 0)

        #temp
        tempGraph = PlotWidget()
        tempValues = dataFrame['temp']

        #smoke


        self.graphGroupBox.setLayout(layout)

    # function to calculate KPI from sensor DATA
    # def telemetryKPI(self):
