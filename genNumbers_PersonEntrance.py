import random

def genNumbers():
    #generate random numbers with time of entrance of an person and time of exit of a person
    #time difference of person is min 5 minutes and max 1 hour

    startingpoint = 1594512095 #start of sensor data
    endpoint = 1595203418 #end of sensor data

    values = []  # declare empty list
    for i in range(20): #20 persons enter room
        temp = random.randint(startingpoint, endpoint)
        temp1 = temp + random.randint(300, 3600) #person leaves room after random time between 5-60 minutes
        values.append(temp)  # insert rand int into list
        values.append(temp1) #insert exit time

    values.sort() #sort array for easier processing
    with open('C:/Users/Franz/OneDrive/Desktop/BAC1/datensatz/persondata.csv', 'w') as f:
        f.write("timestamp\n") #add heading to csv
        for line in values:
            f.write(str(line))  #write one value
            f.write('\n')   #newline to get new column in csv

    f.close()

    return values
