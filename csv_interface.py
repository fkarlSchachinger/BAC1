import pandas as pandas

# File name for the CSV file that should be used
CSV_NAME = 'critical_case.csv'
PERIOD_IN_SEC = 18000


# generate initial time range from user input
def generateRange(selected_time):
    # This function generates the dataframe in only the timerange

    df = pandas.read_csv(CSV_NAME)  # read csv from file into a dataframe
    start_time = selected_time - PERIOD_IN_SEC  # define range from user input
    end_time = selected_time
    trimmed_frame = df[(df['ts'] >= start_time) & (df['ts'] <= end_time)]  # trim data to time range from start
    return trimmed_frame


# help functions for easier usage
def genMean(df: pandas.DataFrame, column_name: str):
    return df[column_name].mean()


def genMin(df: pandas.DataFrame, column_name: str):
    return df[column_name].min()


def genMax(df: pandas.DataFrame, column_name: str):
    return df[column_name].max()


def getLatest(df: pandas.DataFrame, column_name: str):
    return df[column_name].iat[-1]
