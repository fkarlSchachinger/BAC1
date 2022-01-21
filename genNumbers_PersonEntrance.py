import random

def genNumbers():
    # generate random numbers with time of entrance of an person and time of exit of a person
    # time difference of person is min 5 minutes and max 1 hour

    startingpoint = 1594512095  # start of sensor data
    endpoint = 1595203418  # end of sensor datax

    values_entry = []  # declare empty list

    for i in range(20): # 20 persons enter room
        entrytime = random.randint(startingpoint, endpoint)
        values_entry.append(entrytime)

    values_entry.sort()
    values_exit = []

    # create times for exit
    for i in range(20):
        exittime = values_entry[i] + random.randint(300, 3600)  # person leaves room after random time between 5-60 minutes
        values_exit.append(exittime)

    values_entry.insert(0, "entry")
    values_exit.insert(0, "leave")

    f = open('persondata.csv', 'w')
    for i in range(20):
        f.write(str(values_entry[i]) + "," + str(values_exit[i]))  # write one value
        f.write('\n')  # newline to get new column in csv

    f.close()

    return True
