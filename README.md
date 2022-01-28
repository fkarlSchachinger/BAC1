# BAC1|  Identification, processing and utilization of data in an Industry environment | Franz-Karl Schachinger, Alexander Pascal Gewal, Maximilian Posch

Application for visual processing of sensor and persona data

Functionality: 
The application reads data from two different CSV files. 1: Sensor data, which has been aggregated and stored in the files "critical_case.csv" "normal_case.csv". These files are used for the graphical representation. To see the full functionality of the GUI change in the file "csv_interface.py" the file path in the variable "CSV_NAME" in line 4 from "critical_case.csv" to "normal_case.csv". 
The full sensor data is available in the file "iot_telemetry_data.csv". 

Handling of the Application: 

The applications first takes a timestamp from user input to select the time range of which the data is displayed. 
We advise following timestamps for testing (file: "critical_case.csv"):

This timestamp shows the application when 1 Person is in the "machine room", the critical values are lowered because of this and the threshold are not overstepped
2020-07-18 12:14:20    


This timestamp shows the application when no Person is in the "machine room", the critical values have a higher threshold and is overstepped
2020-07-20 00:03:22     


This timestamp shows the application when no person is inside and the thresholds are not met: 
2020-07-18 21:52:27


This timestamp shows the application when a person is inside the machinery room and the thresholds are overstepped: 
2020-07-17 15:58:48


With these timestamps the application functionality can be tested. 
Steps: 
1. Start Application
2. Enter timestamp
3. See results
