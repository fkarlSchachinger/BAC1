import datetime
import math

from PyQt5.QtWidgets import *
from dateutil.parser import parse
import person_check
import csv_interface
from csv_interface import *
from pyqtgraph import *
from pyqtgraph import PlotItem


class AssetApplication(QDialog):
    def __init__(self, str_time, parent=None):
        super(AssetApplication, self).__init__(parent)
        self.str_time = str_time
        self.unix = parse(str_time).timestamp()
        self.people_inside = person_check.checkForPersons(self.unix)
        self.data_frame = generateRange(self.unix)
        # setting critical values
        if self.people_inside > 0:
            self.CRITLPG = 0.009
            self.CRITTEMP = 30
            self.CRITSMOKE = 0.022
        else:
            self.CRITLPG = 0.01
            self.CRITTEMP = 32
            self.CRITSMOKE = 0.024

        # Setting styleSheet
        with open("style.qss", "r") as styleSheet:
            self.setStyleSheet(styleSheet.read())

        time_short = str_time[0:10]  # cut string for nicer output
        # Create Labels Time = inputTime
        selected_time_label = QLabel(str(time_short))  # user input time
        time_label = QLabel("&Time:")  # create label
        time_label.setBuddy(selected_time_label)  # connect label with input time

        # Create all the parts
        self.createDataBox()
        self.createpersonGroupBox()
        self.createGraphGroupBox()

        # Create upper part (outside of Group boxes)
        upper_left_layout = QHBoxLayout()
        upper_left_layout.addWidget(time_label, 0)
        upper_left_layout.addWidget(selected_time_label, 0)
        upper_left_layout.addStretch(1)

        # Main Layout (this will actually be shown, all other parts should be nested inside this)
        main_layout = QGridLayout()
        # Add all boxes to main layout
        main_layout.addLayout(upper_left_layout, 0, 0, 1, 1)
        main_layout.addWidget(self.personGroupBox, 1, 0)
        main_layout.addWidget(self.statusBox, 1, 1)
        main_layout.addWidget(self.graphGroupBox, 2, 0, 2, 2)

        # Set main layout parameters, so it looks better
        main_layout.setRowStretch(1, 1)
        main_layout.setRowStretch(2, 1)
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 1)

        # Set the layout to main layout, so it actually gets shown
        self.setLayout(main_layout)
        self.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle("Asset Status")

    def createpersonGroupBox(self):
        self.personGroupBox = QGroupBox("Status")
        layout = QVBoxLayout()

        person_inside_label = QLabel()
        if self.people_inside > 0:
            person_inside_label.setText("Number of people inside: " + str(self.people_inside))
            person_inside_label.setStyleSheet('color: orange; font-size: 22px')
        else:
            person_inside_label.setText("There is currently no one inside.")
            person_inside_label.setStyleSheet('color: green; font-size: 22px')

        # critical values:
        crit_group_box = QGroupBox("Critical values:")
        crit_layout = QHBoxLayout()
        crit_lpg_label = QLabel("LPG: " + ("%.4f" % self.CRITLPG))
        crit_temp_label = QLabel("Temperature: " + ("%.4f" % self.CRITTEMP))
        crit_smoke_label = QLabel("Smoke: " + ("%.4f" % self.CRITSMOKE))
        crit_layout.addWidget(crit_lpg_label)
        crit_layout.addWidget(crit_temp_label)
        crit_layout.addWidget(crit_smoke_label)
        crit_group_box.setLayout(crit_layout)

        # current values:
        curr_lpg = getLatest(self.data_frame, 'lpg')
        curr_temp = getLatest(self.data_frame, 'temp')
        curr_smoke = getLatest(self.data_frame, 'smoke')
        current_group_box = QGroupBox("Current values:")
        current_layout = QHBoxLayout()
        current_lpg_label = QLabel("LPG: " + ("%.4f" % curr_lpg))
        current_temp_label = QLabel("Temperature: " + ("%.4f" % curr_temp))
        current_smoke_label = QLabel("Smoke: " + ("%.4f" % curr_smoke))
        current_layout.addWidget(current_lpg_label)
        current_layout.addWidget(current_temp_label)
        current_layout.addWidget(current_smoke_label)
        current_group_box.setLayout(current_layout)

        warning = False
        if (curr_lpg > self.CRITLPG) or (curr_temp > self.CRITTEMP) or (curr_smoke > self.CRITSMOKE):
            warning = True

        current_lpg_label.setStyleSheet(('color: red;' if warning else 'color: green;'))
        current_temp_label.setStyleSheet(('color: red;' if warning else 'color: green;'))
        current_smoke_label.setStyleSheet(('color: red;' if warning else 'color: green;'))

        if warning:
            warning_label = QLabel("A critical value has been exceeded")
            warning_label.setStyleSheet('color: red; font-size: large;')


        layout.addWidget(person_inside_label)
        layout.addWidget(crit_group_box)
        layout.addWidget(current_group_box)
        layout.addStretch(1)
        self.personGroupBox.setLayout(layout)

    def createDataBox(self):
        self.statusBox = QGroupBox("Performance Indicators")
        layout = QVBoxLayout()

        # min values
        lpg_low = genMin(self.data_frame, 'lpg')
        temp_low = genMin(self.data_frame, 'temp')
        smoke_low = genMin(self.data_frame, 'smoke')

        lpg_low_label = QLabel("Lowest concentration: " + ("%.9f" % lpg_low))
        temp_low_label = QLabel("Lowest temperature: " + ("%.9f" % temp_low))
        smoke_low_label = QLabel("Lowest concentration: " + ("%.9f" % smoke_low))

        # mean values
        lpg_mean = csv_interface.genMean(self.data_frame, 'lpg')
        temp_mean = csv_interface.genMean(self.data_frame, 'temp')
        smoke_mean = csv_interface.genMean(self.data_frame, 'smoke')

        lpg_mean_label = QLabel("Mean concentration: " + ("%.9f" % lpg_mean))
        temp_mean_label = QLabel("Mean temperature: " + ("%.9f" % temp_mean))
        smoke_mean_label = QLabel("Mean concentration: " + ("%.9f" % smoke_mean))

        # peak
        lpg_max = genMax(self.data_frame, 'lpg')
        temp_max = genMax(self.data_frame, 'temp')
        smoke_max = genMax(self.data_frame, 'smoke')

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

        time = self.data_frame['ts']
        time_val = numpy.array(time.values.tolist())
        t_mean = time_val.mean()
        t_mean = math.trunc(t_mean)
        t = datetime.datetime.fromtimestamp(t_mean)

        # lpg
        lpgGraph = PlotWidget()
        lpgValues = self.data_frame['lpg']
        lpg_val = numpy.array(lpgValues.values.tolist())
        title = 'LPG Value ' + str(t)
        lpgGraph.plotItem.setTitle(title)
        lpg_limit = InfiniteLine(self.CRITLPG, pen='red', angle=0)
        lpgGraph.plotItem.plot(time_val, lpg_val)
        lpgGraph.setYRange(0, 0.01)
        lpgGraph.plotItem.addItem(lpg_limit)
        layout.addWidget(lpgGraph)

        # temp
        temp_graph = PlotWidget()
        temp_values = self.data_frame['temp']
        temp_val = numpy.array(temp_values.values.tolist())
        title = 'Temperatures ' + str(t)
        temp_graph.plotItem.setTitle(title)
        temp_limit = InfiniteLine(self.CRITTEMP, pen='red', angle=0)
        temp_graph.plotItem.addItem(temp_limit)
        temp_graph.setYRange(15, 30)
        temp_graph.plotItem.plot(time_val, temp_val)
        layout.addWidget(temp_graph)

        # smoke
        smoke_graph = PlotWidget()
        smoke_values = self.data_frame['smoke']
        smoke_val = numpy.array(smoke_values.values.tolist())
        title = 'Smoke ' + str(t)
        smoke_graph.plotItem.setTitle(title)
        smoke_limit = InfiniteLine(self.CRITSMOKE, pen='red', angle=0)
        smoke_graph.plotItem.addItem(smoke_limit)
        smoke_graph.plotItem.plot(time_val, smoke_val)
        smoke_graph.setYRange(0.01, 0.03)
        layout.addWidget(smoke_graph)


        self.graphGroupBox.setLayout(layout)

    # function to calculate KPI from sensor DATA
    # def telemetryKPI(self):
