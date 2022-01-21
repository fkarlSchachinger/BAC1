import pandas as pd

def checkForPersons(current_time):
    df = pd.read_csv('persondata.csv')

    # check if 1 cell in exit is empty ?
    values = df[(df['entry'] <= current_time)]  # trim to current time

    # if exit times is past current time, means that exit is in future and persons are still in room
    exits = values['leave']
    people_inside = exits[exits > current_time].count()
    return people_inside
