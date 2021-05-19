import camelot
import pandas as pd
import re

# functions
def rename_headers(columns):
    # rename the headers so only left with the first part, the rest after space are dumped
    new_name = [(re.match(r"(?P<column_name>\w+)(?= .+)|([\d]{1,2}-[\d]{1,2})", column)).group(0) for column in columns]
    return new_name

def get_subject(data):
    if data == '':
        return ''
    subject = re.match(r"(?P<subject>\w+)(?=\s.+)", data)
    return subject.group(0)

def split_time(row):
    # time_col = row["time"]
    time = re.match(r"([\d]{1,2})-([\d]{1,2})", row["time"])
    row["start_time"] = time.group(1)
    row["end_time"] = time.group(2)
    return row

def format_time(row):
    # Subject, Start date, Start time, End date, End Time, All Day Event, Description, Location, Private,
    # MTH0000, 04/25/2021, 8:00 PM, 04/25/2021, 10:00 PM, False,"DEMO", , False
    row['start_time'] = int(row['start_time'])
    row['end_time'] = int(row['end_time'])
    
    quotient = row['start_time']//12
    remainder = row['start_time']%12
    if quotient == 1:
        meridiem = "PM"
    else:
        meridiem = "AM"

    if remainder == 0:
        remainder = 12
    row["start_time"] = f"{remainder}:00 {meridiem}"

    quotient = row['end_time']//12
    remainder = row['end_time']%12
    if quotient == 1:
        meridiem = "PM"
    else:
        meridiem = "AM"

    if remainder == 0:
        remainder = 12
    row["end_time"] = f"{remainder}:00 {meridiem}"

    return row

file = "/Users/ganthology/Desktop/semester2_2020:2021.pdf"

tables = camelot.read_pdf(file)


ori = tables[0].df
print(ori)
# Data cleaning
ori.columns = ori.iloc[0]
ori.drop(0, inplace=True)
ori.reset_index(drop=True)

ori.columns = rename_headers(ori.columns)

# Drop empty columns/index
ori = ori[ori["TIME"]!='']
ori.set_index("TIME", inplace=True)

# Clean subject values
ori = ori.applymap(lambda x: get_subject(x))

index = ori.index

list = []

for i, idx in enumerate(index):
    day = idx[:3].upper()
    start_date = "2021-01-01"
    end_date = "2021-02-01"

    sembreak_starts = "2021-01-07"
    sembreak_ends = "2021-01-14"

    date_range = pd.date_range(start = start_date, end = end_date, freq = f"W-{day}")
    sembreak = pd.date_range(start=sembreak_starts, end=sembreak_ends, freq=f"W-{day}")
    # new_range = list(date_range - sembreak)
    # df.loc[~df.index.isin(exclusion_dates)]
    df = ori.copy()
    # Select only the row == day
    day = df.iloc[i]

    # drop time with no subjects
    uniq_subjects = day[day != ''].reset_index()

    # rename the index column name to "time"
    uniq_subjects.columns = ['time','subject']

    # split the time column to [start_time],[end_time]
    uniq_subjects = uniq_subjects.apply(split_time, axis=1).drop(columns=['time'])

    # new dataframe for each day
    grouped = uniq_subjects.groupby("subject")
    # newDf = {
    #     "subject":[],
    #     "start_time":[],
    #     "end_time":[]
    # }

    # for group,data in grouped:
    #     newDf["subject"].append(data.iloc[0,0])
    #     newDf["start_time"].append(data.iloc[0,1])
    #     newDf["end_time"].append(data.iloc[-1,2])

    newDf = {
        "subject":[],
        "start_date":[],
        "start_time":[],
        "end_date":[],
        "end_time":[],
    }
    for i in date_range:
        for group,data in grouped:
            newDf["subject"].append(data.iloc[0,0])
            newDf["start_time"].append(data.iloc[0,1])
            newDf["end_time"].append(data.iloc[-1,2])        

            newDf['start_date'].append(i)
            newDf['end_date'].append(i)

    newDf = pd.DataFrame(newDf)
    # df.loc[~df.index.isin(exclusion_dates)]
    newDf = newDf.loc[~newDf["start_date"].isin(sembreak)]
    if not newDf.empty:
        newDf = newDf.apply(format_time, axis=1)
        list.append(newDf)

result = pd.concat(list).sort_values(by="start_date").reset_index(drop=True)
result.columns = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time']
result['All Day Event'] = False
result['Description'] = "Lecture"
result['Location'] = ""
result['Private'] = False
print(result)