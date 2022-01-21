from PyQt5.QtWidgets import *
import pandas as pds
from dateutil.parser import parse
from pyqtgraph import *
import pyqtgraph as pg
from csv_interface import generateRange
import person_check

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
        self.createGraphGroupBox()

        # Create upper part (outside of Group boxes)
        upperLeftLayout = QHBoxLayout()
        upperLeftLayout.addWidget(timeLabel, 0, 0)
        upperLeftLayout.addWidget(selectedTimeLabel, 0, 1)
        upperLeftLayout.addStretch(1)

        # Main Layout (this will actually be shown, all other parts should be nested inside this)
        mainLayout = QGridLayout()
        # Add all boxes to main layout
        mainLayout.addLayout(upperLeftLayout, 0, 0, 1, 1)
        mainLayout.addWidget(self.personGroupBox)
        mainLayout.addWidget(self.statusBox)
        mainLayout.addWidget(self.graphGroupBox)


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
        people_inside = person_check.checkForPersons(self.unix)
        if people_inside > 0:
            personInsideLabel.setText("Number of people inside: " + str(people_inside))
            personInsideLabel.setStyleSheet('color: orange;')
        else:
            personInsideLabel.setText("There is currently no one inside.")
            personInsideLabel.setStyleSheet('color: green;')

    def createStatusBox(self):
        self.statusBox = QGroupBox("Current Status")
        layout = QVBoxLayout()
        statusLabel = QLabel("Status:")

        layout.addWidget(statusLabel)

        self.statusBox.setLayout(layout)

    def createGraphGroupBox(self):
        self.graphGroupBox = QGroupBox("Graphs:")
        layout = QVBoxLayout()

        dataFrame = generateRange(self.unix)
        time = dataFrame['ts']

        #lpg
        lpgGraph = pg.PlotWidget()
        lpgValues = dataFrame['lpg']
        lpgGraph.plotItem.setTitle('LPG Value')
        # plot failed
        lpgGraph.plotItem.plot(time, lpgValues)
        layout.addWidget(lpgGraph, 0, 0)

        #temp
        tempGraph = PlotWidget()
        tempValues = dataFrame['temp']
        tempGraph.plotItem.setTitle('Temperatures')
        tempGraph.plotItem.plot(time, tempValues)
        layout.addWidget(tempGraph, 0, 1)

        #smoke
        smokeGraph = PlotWidget()
        smokeValues = dataFrame['smoke']
        smokeGraph.plotItem.setTitle('Smoke')
        smokeGraph.plotItem.plot(time, smokeValues)
        layout.addWidget(smokeGraph, 0, 2)

        self.graphGroupBox.setLayout(layout)

    # function to calculate KPI from sensor DATA
    # def telemetryKPI(self):
