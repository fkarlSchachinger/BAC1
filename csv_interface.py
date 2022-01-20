import pandas


def generateGraphs(time):
    dataFrame = pandas.read_csv('iot_telemetry_data.csv')
    temp = dataFrame.loc[:, "temp"]
    hum = dataFrame.loc[:, "humidity"]
    menHum = hum.mean()

    # meanTemp = temp.mean()
    # print(meanTemp)
    # print(menHum)

    timeBeginn = time - 18000
    timeEnd = time
    graphDataHumidity = dataFrame.loc[ > timeEnd, "humidity"]
    return graphDataHumidity

    # print(dataFrame.loc[:, ["temp"]])
