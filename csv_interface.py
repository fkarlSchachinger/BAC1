import pandas as pandas

# change this to read from another CSV file
CSV_NAME = 'critical_case.csv'
PERIOD_IN_SEC = 18000

def generateRange(time):  # generate initial time range from user input
    # function is used as base for the other data gen functions
    # function generates the dataframe in only the timerange

    df = pandas.read_csv(CSV_NAME)  # read csv from file into a dataframe
    tStart = time - PERIOD_IN_SEC  # define range from user input
    tEnd = time
    temp = df[(df['ts'] >= tStart) & (df['ts'] <= tEnd)]  # trim data to time range from start - (start -3h)
    return temp


def genlpgMEAN(temp):
    # generate mean humidity of last 3 hours
    result = temp['lpg'].mean()
    return result


def genTempMEAN(temp):
    # generate mean temperatur of last 3 hours
    result = temp['temp'].mean()
    return result


def genSmokeMEAN(temp):
    # generate mean smoke value
    result = temp['smoke'].mean()
    return result


def genMean(df: pandas.DataFrame, columnName: str):
    return df[columnName].mean()

def genMin(df: pandas.DataFrame, columName:str):
    return df[columName].min()

def genMax(df: pandas.DataFrame, columnName:str):
    return df[columnName].max()

def getLatest(df: pandas.DataFrame, columnName:str):
    return df[columnName].iat[-1]
