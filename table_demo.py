import camelot
import tabula
import streamlit as st

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
# umt = "/Users/ganthology/Downloads/umt_semester_timetable(dragged).pdf"

tables = camelot.read_pdf(file)
# tables2 = tabula.read_pdf(file)
# umt_table = camelot.read_pdf(umt)
# umt_table2 = tabula.read_pdf(umt)

# print(tables2)
# print(umt_table2)

print(tables[0].df)
df = tables[0].df

df.columns = df.iloc[0]
df.drop(0, inplace=True)
# df.reset_index(inplace=True)
# df = df.set_index('index')
print(df)
print(df.iloc[0])
# print(list(tables[0].df.index))
# print(list(tables[0].df.columns))

# print(f"Tables: {umt_table.n}")
# print(umt_table.df)

# print(list(umt_table[0].df.index))
# print(list(umt_table[0].df.columns))