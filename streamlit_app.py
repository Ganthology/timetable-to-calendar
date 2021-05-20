# from numpy import NaN
import tabula
import pandas as pd
import re
import streamlit as st
import base64
import datetime

"""
# Timetable to Calendar Converter

This app converts timetable pdf to csv file, the csv file can then be exported to Google Calendar.

The purpose of this app is to encourage students to use calendar app as their time management tool.

-- Boon Kit

## Steps
1. Upload your timetable in ENGLISH in .pdf format

2. Select the date for your Semester, Mid-Semester Break and Study Week.

3. Download the csv file at the Download section

4. Import the csv file to your Google Calendar 

[Refer here for Importing CSV file](https://support.google.com/calendar/answer/37118?co=GENIE.Platform%3DDesktop&hl=en)

[Link to my GitHub](https://github.com/Ganthology)


## **Upload your timetable(.pdf) here**

"""

# functions
def rename_headers(columns):
    # rename the headers so only left with the first part, the rest after space are dumped
    new_name = [(re.match(r"(?P<column_name>\w+)(?= .+)|([\d]{1,2}-[\d]{1,2})", column)).group(0) for column in columns]
    return new_name

def get_subject(data):
    if not isinstance(data, str):
        return ''
    subject = re.match(r"^[\w]+", data)
    return subject.group()

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

def file_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="class_calendar.csv">Download the Calendar CSV file</a>'
    return href  
#end

file = st.file_uploader("Upload Timetable PDF", type='pdf')

"""
#### This app does not work for every timetable pdf file, currently available for:

- Universiti Putra Malaysia

## Date Section
"""
start_date = st.date_input("Semester Start Date", datetime.datetime.now(), key="sem_start")
end_date = st.date_input("Semester End Date", datetime.datetime.now(), key="sem_end")

start_break = st.date_input("Mid Semester Break Start Date", datetime.datetime.now(), key="break_start")
end_break = st.date_input("Mid Semester Break End Date", datetime.datetime.now(), key="break_end")

start_study_week = st.date_input("Study Week Start Date", datetime.datetime.now(), key="study_start")
end_study_week = st.date_input("Study Week End Date", datetime.datetime.now(), key="study_end")

f"""
### Date Checking
- Your semester is from {start_date} until {end_date}
- Your Mid Semester Break is from {start_break} until {end_break}
- Your Study Week is from {start_study_week} until {end_study_week}
"""

if file is not None:
    tables = tabula.read_pdf(file)[0]

    ori = tables
    # Data cleaning
    # ori.columns = ori.iloc[0]
    # ori.drop(0, inplace=True)
    # ori.reset_index(drop=True)

    ori.columns = rename_headers(ori.columns)

    # # Drop empty columns/index
    # ori = ori[ori["TIME"] != np.nan]
    ori = ori.dropna(subset=['TIME'])
    print(ori)
    ori.set_index("TIME", inplace=True)
    print(ori.iloc[0,10])
    print(type(ori.iloc[0,10]))

    # Clean subject values
    ori = ori.applymap(lambda x: get_subject(x))
    print(ori)
    index = ori.index

    list = []

    """
    ## Is This Your Timetable?
    #### The timetable after cleaning
    """
    ori
    
    for i, idx in enumerate(index):
        day = idx[:3].upper()

        date_range = pd.date_range(start = start_date, end = end_date, freq = f"W-{day}")
        sembreak = pd.date_range(start=start_break, end=end_break, freq=f"W-{day}")
        study_week = pd.date_range(start=start_study_week, end=end_study_week, freq=f"W-{day}")

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
        newDf = newDf.loc[~newDf["start_date"].isin(study_week)]

        if not newDf.empty:
            newDf = newDf.apply(format_time, axis=1)
            list.append(newDf)
    if list:
        result = pd.concat(list).sort_values(by="start_date").reset_index(drop=True)
        result.columns = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time']
        result['All Day Event'] = False
        result['Description'] = "Lecture"
        result['Location'] = ""
        result['Private'] = False

        """
        ## Download Section

        Check the CSV file in excel or Google Sheet before importing to calendar, as the process is irreversible.
        """
        st.markdown(file_download_link(result), unsafe_allow_html=True)
        """
        #### First 10 row of the CSV file
        """
        st.dataframe(result.head(10))
        """

        ## Feedback
        Do fill this feedback form if you like my work!

        [Feedback Form](https://forms.gle/3DLemvUE5FNzBJws8)
        """
"""
#### Copyright © Gan Boon Kit / UPM
"""

