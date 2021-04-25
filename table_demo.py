import camelot
import tabula
import streamlit as st

# Subject, Start Date, All Day Event, Start Time, End Time, Location, Description （For csv import to google calendar)
# MTH3411, EVERY MONDAY, FALSE, 0800, 1000, , 
# User input (Semester Start date, End date), sem break date/period]
# pd.date_range(start="2018-09-09",end="2020-02-02")
# pd.date_range(start= start_date, end= end_date)

file = "/Users/ganthology/Desktop/semester2_2020:2021.pdf"
umt = "/Users/ganthology/Downloads/umt_semester_timetable(dragged).pdf"

tables = camelot.read_pdf(file)
# tables2 = tabula.read_pdf(file)
umt_table = camelot.read_pdf(umt)
umt_table2 = tabula.read_pdf(umt)

# print(tables2)
print(umt_table2)

print(tables[0].df)

# print(list(tables[0].df.index))
# print(list(tables[0].df.columns))

# print(f"Tables: {umt_table.n}")
print(umt_table.df)

# print(list(umt_table[0].df.index))
# print(list(umt_table[0].df.columns))