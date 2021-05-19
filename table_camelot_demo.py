import camelot
import streamlit as st
import re
import numpy as np
import pandas as pd

# Subject, Start date, Start time, End date, End Time, All Day Event, Description, Location, Private,
# MTH0000, 04/25/2021, 8:00 PM, 04/25/2021, 10:00 PM, False,"DEMO", , False

# # User input (Semester Start date, End date), sem break date/period]
# pd.date_range(start="2018-09-09",end="2020-02-02",freq="W-SUN")
# pd.date_range(start= start_date, end= end_date)

# sembreak = pd.date_range(start="", end="")
# new_range = list(set(range) - set(sembreak))

# date = pd.Timestamp("2019-09-09")
# print(date.day_name()) >>> Monday

# streamlit date picker widget
# d = st.date_input("When's your birthday",datetime.date(2019, 7, 6))

file = "/Users/ganthology/Desktop/semester2_2020:2021.pdf"
file2 = "./timetables-pdf/cass timetable sem 4.pdf"

tables = camelot.read_pdf(file)
table2 = camelot.read_pdf(file2)

def rename_headers(columns):
    # rename the headers so only left with the first part, the rest after space are dumped
    new_name = [(re.match(r"(?P<column_name>\w+)(?= .+)|([\d]{1,2}-[\d]{1,2})", column)).group(0) for column in columns]
    return new_name

# print(tables[0].df)
df = tables[0].df
df2 = table2[0].df


# df2.columns = rename_headers(df.iloc[0])
# df2.drop(0, inplace=True)
# df2.reset_index(drop=True)

# print(df2)

df.columns = df.iloc[0]
print(df)
df.drop(0, inplace=True)
print(df)
df.reset_index(drop=True)

def get_subject(data):
    if data == '':
        return ''
    subject = re.match(r"(?P<subject>\w+)(?=\s.+)", data)
    return subject.group(0)

df.columns = rename_headers(df.columns)
# Drop empty columns
df = df[df["TIME"]!='']
df.set_index("TIME", inplace=True)

# print(df.applymap(lambda x: get_subject(x)))

df = df.applymap(lambda x: get_subject(x))

# print(df.iloc[0])
monday = df.iloc[0]
# drop empty rows
uniq_mon = monday[monday!=''].reset_index()
# rename the index column name to "time"
uniq_mon.columns = ['time','subject']

# print(uniq_mon["time"])

# functions to group subjects with consecutive time
# idea outline:
# def function(row):
#     the row format should be "subject_name start date end date time(with dash)"
#     row[time] split to "start time" and "end time" column
#     for current row and next row, if the subject_name is equal, and (current end time equal to next start time) then merge
#     take the first start_time merge with last end_time   

def split_time(row):
    # time_col = row["time"]
    time = re.match(r"([\d]{1,2})-([\d]{1,2})", row["time"])
    row["start_time"] = time.group(1)
    row["end_time"] = time.group(2)
    return row

# split the time column to [start_time],[end_time]
uniq_mon = uniq_mon.apply(split_time, axis=1).drop(columns=['time'])

# new dataframe for each day
grouped = uniq_mon.groupby("subject")
newDf = {
    "subject":[],
    "start_time":[],
    "end_time":[]
}

for group,data in grouped:
    newDf["subject"].append(data.iloc[0,0])
    newDf["start_time"].append(data.iloc[0,1])
    newDf["end_time"].append(data.iloc[-1,2])
newDf = pd.DataFrame(newDf)
# print(newDf)