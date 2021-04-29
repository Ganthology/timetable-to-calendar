import camelot
import tabula
import streamlit as st
import re
import numpy as np
import pandas as pd

# Subject, Start date, Start time, End date, End Time, All Day Event, Description, Location, Private,
# MTH0000, 04/25/2021, 8:00 PM, 04/25/2021, 10:00 PM, False,"DEMO", , False

# # User input (Semester Start date, End date), sem break date/period]
# pd.date_range(start="2018-09-09",end="2020-02-02")
# pd.date_range(start= start_date, end= end_date)

# sembreak = pd.date_range(start="", end="")
# new_range = list(set(range) - set(sembreak))

# date = pd.Timestamp("2019-09-09")
# print(date.day_name()) >>> Monday

file = "/Users/ganthology/Desktop/semester2_2020:2021.pdf"
file2 = "./timetables-pdf/cass timetable sem 4.pdf"
# umt = "/Users/ganthology/Downloads/umt_semester_timetable(dragged).pdf"

tables = camelot.read_pdf(file)
table2 = camelot.read_pdf(file2)
# tables2 = tabula.read_pdf(file)
# umt_table = camelot.read_pdf(umt)
# umt_table2 = tabula.read_pdf(umt)

# print(tables2)
# print(umt_table2)

def rename_headers(columns):
    new_name = [(re.match(r"(?P<column_name>\w+)(?= .+)|([\d]{1,2}-[\d]{1,2})", column)).group(0) for column in columns]
    return new_name

# print(tables[0].df)
df = tables[0].df
df2 = table2[0].df


df2.columns = rename_headers(df.iloc[0])
df2.drop(0, inplace=True)
df2.reset_index(drop=True)

print(df2)

df.columns = df.iloc[0]
df.drop(0, inplace=True)
# df.reset_index(inplace=True)
# df = df.set_index('index')
df.reset_index(drop=True)
# print(df.columns)
# print(df.iloc[0])
# print(df.iloc[0])
# print(list(tables[0].df.index))
# print(list(tables[0].df.columns))

# print(f"Tables: {umt_table.n}")
# print(umt_table.df)

# print(list(umt_table[0].df.index))
# print(list(umt_table[0].df.columns))

def get_subject(data):
    if data == '':
        return ''
    subject = re.match(r"(?P<subject>\w+)(?=\s.+)", data)
    return subject.group(0)

df.columns = rename_headers(df.columns)
# print(df.columns)
# print(df)
df = df[df["TIME"]!='']
df.set_index("TIME", inplace=True)

print(df.applymap(lambda x: get_subject(x)))