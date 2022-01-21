from datetime import datetime
from genNumbers_PersonEntrance import *
from csv_interface import *
from application import *
from dateutil.parser import parse


def main():
    user_input = input("Time in Format: YYYY-MM-DD HH:mm:ss")
    time = parse(user_input).timestamp()  # time is in unixformat
    # genNumbers()
    temp = generateRange(time)
    lpg = genlpgMEAN(temp)
    smoke = genSmokeMEAN(temp)
    temperatur = genTempMEAN(temp)

    temperaturArr = temp['temp']
    timeArr = temp['ts']
    smokeArr = temp['smoke']
    lpgArr = temp['lpg']

    context = QApplication([])
    context.setStyle('Fusion')
    our_app = AssetApplication(user_input)
    our_app.show()
    context.exec()
    # myTime = datetime(time)
    # print for debugging purposes
    print(lpg, smoke, temperatur)



if __name__ == "__main__":
    main()
    # print(values)
