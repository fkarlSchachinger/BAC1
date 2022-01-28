import pandas as pd


def checkForPersons(current_time):
    df = pd.read_csv('persondata.csv')

    # trim to current time
    values = df[(df['entry'] <= current_time)]

    # if exit times are past current time, means that exit is in future and persons are still in room
    exits = values['leave']
    people_inside = exits[exits > current_time].count()
    return people_inside
