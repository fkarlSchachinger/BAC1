import datetime
import math

from PyQt5.QtWidgets import *
from dateutil.parser import parse
import person_check
import csv_interface
from csv_interface import *
from pyqtgraph import *
from pyqtgraph import PlotWidget


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

        formatted_time = datetime.datetime.fromtimestamp(self.unix).strftime("%d.%m.%Y %X")

        # Create selected time label
        selected_time_label = QLabel(formatted_time)  # user input time
        selected_time_label.setStyleSheet('font-size: 24px;')
        time_label = QLabel("Time:")
        time_label.setStyleSheet('font-size: 24px;')
        time_label.setBuddy(selected_time_label)

        # Create period time label
        period_label = QLabel("Period: ")
        period_label.setStyleSheet('font-size: 24px;')
        period_val_label = QLabel(str(csv_interface.PERIOD_IN_SEC/3600) + "h")
        period_val_label.setStyleSheet('font-size: 24px;')
        period_label.setBuddy(period_val_label)

        # Call GroupBox creations
        self.createDataBox()
        self.createStatusGroupBox()
        self.createGraphGroupBox()

        # Create upper part (outside of Group boxes)
        upper_left_layout = QHBoxLayout()
        upper_left_layout.addWidget(time_label, 1)
        upper_left_layout.addWidget(selected_time_label, 1)
        upper_left_layout.addStretch(2)
        upper_left_layout.addWidget(period_label)
        upper_left_layout.addWidget(period_val_label)

        # Main Layout, items to be shown must be nested inside this
        main_layout = QGridLayout()

        # Add GroupBoxes to main layout
        main_layout.addLayout(upper_left_layout, 0, 0, 1, 1)
        main_layout.addWidget(self.statusGroupBox, 1, 0)
        main_layout.addWidget(self.statusBox, 1, 1)
        main_layout.addWidget(self.graphGroupBox, 2, 0, 2, 2)

        # Set main layout parameters
        main_layout.setRowStretch(1, 1)
        main_layout.setRowStretch(2, 1)
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 1)

        # Set the layout to main layout
        self.setLayout(main_layout)
        self.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle("Asset Status")

    def createStatusGroupBox(self):
        self.statusGroupBox = QGroupBox("Current status")
        layout = QVBoxLayout()

        # Show number of people currently inside
        person_inside_label = QLabel()
        if self.people_inside > 0:
            person_inside_label.setText("Number of people inside: " + str(self.people_inside))
            person_inside_label.setStyleSheet('color: orange; font-size: 22px')
        else:
            person_inside_label.setText("There is currently no one inside.")
            person_inside_label.setStyleSheet('color: green; font-size: 22px')
        layout.addWidget(person_inside_label)

        # Critical values GroupBox:
        crit_group_box = QGroupBox("Critical values:")
        crit_layout = QHBoxLayout()
        crit_lpg_label = QLabel("LPG: " + ("%.4f" % self.CRITLPG))
        crit_temp_label = QLabel("Temperature: " + ("%.4f" % self.CRITTEMP))
        crit_smoke_label = QLabel("Smoke: " + ("%.4f" % self.CRITSMOKE))
        crit_layout.addWidget(crit_lpg_label)
        crit_layout.addWidget(crit_temp_label)
        crit_layout.addWidget(crit_smoke_label)
        crit_group_box.setLayout(crit_layout)
        layout.addWidget(crit_group_box)

        # Get current values
        curr_lpg = getLatest(self.data_frame, 'lpg')
        curr_temp = getLatest(self.data_frame, 'temp')
        curr_smoke = getLatest(self.data_frame, 'smoke')

        # Current values GroupBox
        current_group_box = QGroupBox("Current values:")
        current_layout = QHBoxLayout()
        current_lpg_label = QLabel("LPG: " + ("%.4f" % curr_lpg))
        current_temp_label = QLabel("Temperature: " + ("%.4f" % curr_temp))
        current_smoke_label = QLabel("Smoke: " + ("%.4f" % curr_smoke))
        current_layout.addWidget(current_lpg_label)
        current_layout.addWidget(current_temp_label)
        current_layout.addWidget(current_smoke_label)
        current_group_box.setLayout(current_layout)
        layout.addWidget(current_group_box)

        # Color the values, depending on whether they exceeded critical values
        current_lpg_label.setStyleSheet(('color: red;' if curr_lpg > self.CRITLPG else 'color: green;'))
        current_temp_label.setStyleSheet(('color: red;' if curr_temp > self.CRITTEMP else 'color: green;'))
        current_smoke_label.setStyleSheet(('color: red;' if curr_smoke > self.CRITSMOKE else 'color: green;'))

        # Notification part
        notification_layout = QVBoxLayout()
        notification_layout.addStretch(1)

        # Check if a critical value has been exceeded
        warning = False
        if (curr_lpg > self.CRITLPG) or (curr_temp > self.CRITTEMP) or (curr_smoke > self.CRITSMOKE):
            warning = True

        # Warnings if a value is too high
        if warning:
            warning_label = QLabel("A critical value has been exceeded")
            warning_label.setStyleSheet('color: orange; font-size: 22px;')
            notification_layout.addWidget(warning_label)
            if self.people_inside > 0:
                # Extra warning if there are people inside
                people_warning = QLabel("Caution! Person currently inside")
                people_warning.setStyleSheet('color: red; font-size: 24px;')
                notification_layout.addWidget(people_warning)
        else:
            okay_label = QLabel("All values within acceptable range")
            okay_label.setStyleSheet('color: green; font-size: 24px;')
            notification_layout.addWidget(okay_label)

        layout.addLayout(notification_layout)
        layout.addStretch(1)
        self.statusGroupBox.setLayout(layout)

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

        # peak values
        lpg_max = genMax(self.data_frame, 'lpg')
        temp_max = genMax(self.data_frame, 'temp')
        smoke_max = genMax(self.data_frame, 'smoke')

        lpg_max_label = QLabel("Peak concentration: " + ("%.9f" % lpg_max))
        temp_max_label = QLabel("Peak temperature: " + ("%.9f" % temp_max))
        smoke_max_label = QLabel("Peak concentration: " + ("%.9f" % smoke_max))

        # LPG GroupBox
        lpg_layout = QVBoxLayout()
        lpg_group_box = QGroupBox("LPG concentration in ppm over given period")
        lpg_layout.addWidget(lpg_low_label)
        lpg_layout.addWidget(lpg_mean_label)
        lpg_layout.addWidget(lpg_max_label)
        lpg_group_box.setLayout(lpg_layout)
        layout.addWidget(lpg_group_box)

        # Temperature GroupBox
        temp_layout = QVBoxLayout()
        temp_group_box = QGroupBox("Temperature in Fahrenheit over given period")
        temp_layout.addWidget(temp_low_label)
        temp_layout.addWidget(temp_mean_label)
        temp_layout.addWidget(temp_max_label)
        temp_group_box.setLayout(temp_layout)
        layout.addWidget(temp_group_box)

        # Smoke GroupBox
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

        # format time
        time_series = self.data_frame['ts']
        time_val = numpy.array(time_series.values.tolist())
        t_mean = time_val.mean()
        t_mean = math.trunc(t_mean)
        title_time = datetime.datetime.fromtimestamp(t_mean).strftime("%d.%m.%Y")

        # format values
        lpg_values = self.data_frame['lpg']
        lpg_val = numpy.array(lpg_values.values.tolist())
        temp_values = self.data_frame['temp']
        temp_val = numpy.array(temp_values.values.tolist())
        smoke_values = self.data_frame['smoke']
        smoke_val = numpy.array(smoke_values.values.tolist())

        # lpg graph
        lpg_graph = PlotWidget()
        title = 'LPG Value ' + title_time
        lpg_graph.plotItem.setTitle(title)
        lpg_date_axis = DateAxisItem()
        lpg_graph.plotItem.setAxisItems({'bottom': lpg_date_axis})
        lpg_limit = InfiniteLine(self.CRITLPG, pen='red', angle=0)
        lpg_graph.plotItem.plot(time_val, lpg_val)
        lpg_graph.setYRange(0, 0.01)
        lpg_graph.plotItem.addItem(lpg_limit)

        # temperature graph
        temp_graph = PlotWidget()
        title = 'Temperatures ' + title_time
        temp_graph.plotItem.setTitle(title)
        temp_date_axis = DateAxisItem()
        temp_graph.plotItem.setAxisItems({'bottom': temp_date_axis})
        temp_limit = InfiniteLine(self.CRITTEMP, pen='red', angle=0)
        temp_graph.plotItem.addItem(temp_limit)
        temp_graph.setYRange(15, 35)
        temp_graph.plotItem.plot(time_val, temp_val)

        # smoke graph
        smoke_graph = PlotWidget()
        title = 'Smoke ' + title_time
        smoke_graph.plotItem.setTitle(title)
        smoke_date_axis = DateAxisItem()
        smoke_graph.plotItem.setAxisItems({'bottom': smoke_date_axis})
        smoke_limit = InfiniteLine(self.CRITSMOKE, pen='red', angle=0)
        smoke_graph.plotItem.addItem(smoke_limit)
        smoke_graph.plotItem.plot(time_val, smoke_val)
        smoke_graph.setYRange(0.01, 0.03)

        layout.addWidget(lpg_graph)
        layout.addWidget(temp_graph)
        layout.addWidget(smoke_graph)
        self.graphGroupBox.setLayout(layout)

    # function to calculate KPI from sensor DATA
    # def telemetryKPI(self):
