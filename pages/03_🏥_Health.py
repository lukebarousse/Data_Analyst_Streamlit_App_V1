import streamlit as st
import pandas as pd
import numpy as np
import datetime
from modules.formater import Title, Footer

# Title page and footer
title = "🏥 Health"
t = Title().page_config(title)
f = Footer().footer()

# import and cleanup
data_url = 'https://storage.googleapis.com/gsearch_share/gsearch_jobs.csv'
jobs_all = pd.read_csv(data_url)
jobs_all.date_time = pd.to_datetime(jobs_all.date_time) # convert to date time
jobs_all = jobs_all.drop(labels=['Unnamed: 0', 'index'], axis=1, errors='ignore')

# Calculate number jobs repeated
repeat_jobs = jobs_all.job_id.value_counts()
try:
    repeat_jobs = repeat_jobs[repeat_jobs>1].index[0]
    repeat_jobs = len(repeat_jobs)
except IndexError:
    repeat_jobs = "None"

# Calculate number jobs and trend
num_jobs = len(jobs_all)

# Calculate number of missing dates
first_date = jobs_all.date_time.dt.date.min()
today_date = datetime.date.today() #+ datetime.timedelta(days=2) # test function works
date_count = pd.DataFrame(jobs_all.date_time.dt.date.value_counts())
missing_dates = list(pd.date_range(start=first_date, end=today_date).difference(date_count.index))

# Job count dataframe calc
jobs_daily = jobs_all.date_time.dt.date
jobs_daily = jobs_daily.value_counts().rename_axis('Date').reset_index(name='Job Postings')
jobs_daily = jobs_daily.sort_values(by='Date', ascending=False)

# Calculate average number of job postings a day
delta_days = (today_date - (first_date - datetime.timedelta(days=2))).days # first day was actually day prior but UTC
jobs_day = round(len(jobs_all)/delta_days)
jobs_today = jobs_daily[jobs_daily.Date == datetime.date.today()]
try:
    jobs_today = jobs_today['Job Postings'].fillna(0).iloc[0]
except IndexError: #Error when coming to new day and no values for new day
    jobs_today = jobs_daily[jobs_daily.Date == datetime.date.today() - datetime.timedelta(days=1)]
    jobs_today = jobs_today['Job Postings'].fillna(0).iloc[0]
jobs_delta = 100 * (jobs_today - jobs_day) / jobs_day
jobs_delta = jobs_delta.round(1)

# calculate database size yesterday to today
jobs_yesterday = num_jobs - jobs_today
jobs_all_delta = ((num_jobs - jobs_yesterday) * 100) / jobs_yesterday
jobs_all_delta = jobs_all_delta.round(1)

# Date Display:
update_date = jobs_all.date_time.max()
update_time = update_date.strftime("%H:%M")
update_time = f"{update_time} UTC"
update_date = update_date.strftime("%d-%b-%Y")

st.markdown("## 🏥 Health of Job Data Collection")
col1, col2, col3 = st.columns(3)
col1.metric("Jobs Last Updated", update_time, update_date, delta_color="off")
col2.metric("Jobs Added in Update", jobs_today, f"{jobs_delta}%")
col3.metric("Size of Jobs Database", num_jobs, f"{jobs_all_delta}%") # Calculate % increase


st.write(f"#### 📈 Daily job scraping status")
st.line_chart(jobs_daily,x='Date',  y='Job Postings')
st.write(f"📆 Collecting data for {delta_days} days now since {first_date}... \n")
if len(missing_dates) > 0:
    st.write("❌ Missing data for following dates:")
    for date in missing_dates:
        st.write(date)