from genNumbers_PersonEntrance import *
from csv_interface import *
from application import *
from dateutil.parser import parse
import csv_interface


def main():
    user_input = input("Time in Format: YYYY-MM-DD HH:mm:ss")
    time = parse(user_input).timestamp()  # time is in unixformat
    #our_app = AssetApplication(time)
    #genNumbers()
    dataIrgendwas = generateGraphs(time)
    print(dataIrgendwas)


if __name__ == "__main__":
    main()
    #values = genNumbers()
    # print(values)
