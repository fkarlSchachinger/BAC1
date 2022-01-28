import random

def genPersonData():
    # generate random numbers with time of entrance of a person and time of exit of a person
    # time difference of person is min 5 minutes and max 1 hour

    first_timestamp = 1594512095  # start of sensor data
    last_timestamp = 1595203418  # end of sensor data

    values_entry = []

    for i in range(20):  # 20 persons enter room
        entry_time = random.randint(first_timestamp, last_timestamp)
        values_entry.append(entry_time)

    values_entry.sort()
    values_exit = []

    # create times for exit
    for i in range(20):
        # person leaves room after random time between 5-60 minutes
        exit_time = values_entry[i] + random.randint(300, 3600)
        values_exit.append(exit_time)

    values_entry.insert(0, "entry")
    values_exit.insert(0, "leave")

    # write generated dat to persondata.csv
    f = open('persondata.csv', 'w')
    for i in range(20):
        f.write(str(values_entry[i]) + "," + str(values_exit[i]))
        f.write('\n')

    f.close()

    return True
