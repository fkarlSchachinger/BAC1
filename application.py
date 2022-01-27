import datetime
import math

from PyQt5.QtWidgets import *
import pandas as pds
from dateutil.parser import parse
from pyqtgraph import *
import pyqtgraph as pg
import person_check
import csv_interface
from csv_interface import *

# Used tutorial for PyQt5: https://build-system.fman.io/pyqt5-tutorial
from pyqtgraph import PlotWidget
from pyqtgraph import *


class AssetApplication(QDialog):
    def __init__(self, str_time, parent=None):
        super(AssetApplication, self).__init__(parent)
        self.str_time = str_time
        self.unix = parse(str_time).timestamp()
        self.people_inside = person_check.checkForPersons(self.unix)

        # Setting styleSheet
        with open("style.qss", "r") as styleSheet:
            self.setStyleSheet(styleSheet.read())

        time_short = str_time[0:10]  # cut string for nicer output
        # Create Labels Time = inputTime
        selectedTimeLabel = QLabel(str(time_short))  # user input time
        timeLabel = QLabel("&Time:")  # create label
        timeLabel.setBuddy(selectedTimeLabel)  # connect label with input time

        # Create all the parts
        self.createDataBox()
        self.createpersonGroupBox()
        self.createGraphGroupBox()

        # Create upper part (outside of Group boxes)
        upperLeftLayout = QHBoxLayout()
        upperLeftLayout.addWidget(timeLabel, 0)
        upperLeftLayout.addWidget(selectedTimeLabel, 0)
        upperLeftLayout.addStretch(1)

        # Main Layout (this will actually be shown, all other parts should be nested inside this)
        mainLayout = QGridLayout()
        # Add all boxes to main layout
        mainLayout.addLayout(upperLeftLayout, 0, 0, 1, 1)
        mainLayout.addWidget(self.personGroupBox, 1, 0)
        mainLayout.addWidget(self.statusBox, 1, 1)
        mainLayout.addWidget(self.graphGroupBox, 2, 0, 2, 2)

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
        self.personGroupBox = QGroupBox("Status")
        personInsideLabel = QLabel()


        if self.people_inside > 0:
            personInsideLabel.setText("Number of people inside: " + str(self.people_inside))
            personInsideLabel.setStyleSheet('color: orange;')
        else:
            personInsideLabel.setText("There is currently no one inside.")
            personInsideLabel.setStyleSheet('color: green;')

        layout = QVBoxLayout()
        layout.addWidget(personInsideLabel)
        layout.addStretch(1)
        self.personGroupBox.setLayout(layout)

    def createDataBox(self):
        self.statusBox = QGroupBox("Performance Indicators")
        data_frame = generateRange(self.unix)
        layout = QVBoxLayout()

        #min values
        lpg_low = genMin(data_frame, 'lpg')
        temp_low = genMin(data_frame, 'temp')
        smoke_low = genMin(data_frame, 'smoke')

        lpg_low_label = QLabel("Lowest concentration: " + ("%.9f" % lpg_low))
        temp_low_label = QLabel("Lowest temperature: " + ("%.9f" % temp_low))
        smoke_low_label = QLabel("Lowest concentration: " + ("%.9f" % smoke_low))

        # mean values
        lpg_mean = csv_interface.genMean(data_frame, 'lpg')
        temp_mean = csv_interface.genMean(data_frame, 'temp')
        smoke_mean = csv_interface.genMean(data_frame, 'smoke')

        lpg_mean_label = QLabel("Mean concentration: " + ("%.9f" % lpg_mean))
        temp_mean_label = QLabel("Mean temperature: " + ("%.9f" % temp_mean))
        smoke_mean_label = QLabel("Mean concentration: " + ("%.9f" % smoke_mean))

        # peak
        lpg_max = genMax(data_frame, 'lpg')
        temp_max = genMax(data_frame, 'temp')
        smoke_max = genMax(data_frame, 'smoke')

        lpg_max_label = QLabel("Peak concentration: " + ("%.9f" % lpg_max))
        temp_max_label = QLabel("Peak temperature: " + ("%.9f" % temp_max))
        smoke_max_label = QLabel("Peak concentration: " + ("%.9f" % smoke_max))

        lpg_layout = QVBoxLayout()
        lpg_group_box = QGroupBox("LPG concentration in ppm over given period")
        lpg_layout.addWidget(lpg_low_label)
        lpg_layout.addWidget(lpg_mean_label)
        lpg_layout.addWidget(lpg_max_label)
        lpg_group_box.setLayout(lpg_layout)
        layout.addWidget(lpg_group_box)

        temp_layout = QVBoxLayout()
        temp_group_box = QGroupBox("Temperature in Fahrenheit over given period")
        temp_layout.addWidget(temp_low_label)
        temp_layout.addWidget(temp_mean_label)
        temp_layout.addWidget(temp_max_label)
        temp_group_box.setLayout(temp_layout)
        layout.addWidget(temp_group_box)

        smoke_layout = QVBoxLayout()
        smoke_group_box = QGroupBox("Smoke concentration in ppm over given period")
        smoke_layout.addWidget(smoke_low_label)
        smoke_layout.addWidget(smoke_mean_label)
        smoke_layout.addWidget(smoke_max_label)
        smoke_group_box.setLayout(smoke_layout)
        layout.addWidget(smoke_group_box)

        self.statusBox.setLayout(layout)

    def createGraphGroupBox(self):
        self.graphGroupBox = QGroupBox("Graphs:")
        layout = QHBoxLayout()
        dataFrame = generateRange(self.unix)
        time = dataFrame['ts']
        time_val = numpy.array(time.values.tolist())
        t_mean = time_val.mean()
        t_mean = math.trunc(t_mean)
        t = datetime.datetime.fromtimestamp(t_mean)

        # lpg
        lpgGraph = PlotWidget()
        lpgValues = dataFrame['lpg']
        lpg_val = numpy.array(lpgValues.values.tolist())
        title = 'LPG Value ' + str(t)
        lpgGraph.plotItem.setTitle(title)
        lpgGraph.plotItem.plot(time_val,
                               lpg_val)  # this works -> fix values from dataframe by using "numpy.array(vals.values.tolist())"
        layout.addWidget(lpgGraph)
        lpgGraph.setYRange(0, 0.01)
        lpg_limit = InfiniteLine(0.009, pen='red', angle=0)
        lpgGraph.plotItem.addItem(lpg_limit)

        # temp
        tempGraph = PlotWidget()
        tempValues = dataFrame['temp']
        temp_val = numpy.array(tempValues.values.tolist())
        title = 'Temperatures ' + str(t)
        tempGraph.plotItem.setTitle(title)
        temp_limit = InfiniteLine(30, pen='red', angle=0)
        tempGraph.plotItem.addItem(temp_limit)
        tempGraph.setYRange(15, 30)
        tempGraph.plotItem.plot(time_val, temp_val)
        layout.addWidget(tempGraph)

        # smoke
        smokeGraph = PlotWidget()
        smokeValues = dataFrame['smoke']
        smoke_val = numpy.array(smokeValues.values.tolist())
        title = 'Smoke ' + str(t)
        smokeGraph.plotItem.setTitle(title)
        smoke_limit = InfiniteLine(0.022, pen='red', angle=0)
        smokeGraph.plotItem.addItem(smoke_limit)
        smokeGraph.plotItem.plot(time_val, smoke_val)
        smokeGraph.setYRange(0.01, 0.03)
        layout.addWidget(smokeGraph)


        self.graphGroupBox.setLayout(layout)

    # function to calculate KPI from sensor DATA
    # def telemetryKPI(self):
