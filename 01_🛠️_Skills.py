import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from modules.formater import Title, Footer
from modules.importer import DataImport

# Title page and footer
title = "🛠️ Skills"
t = Title().page_config(title)
f = Footer().footer()

# Import data
jobs_all = DataImport().fetch_and_clean_data()

# Dictionary for skills and tools mapping, in order to have a correct naming
keywords_skills = {
    'airflow': 'Airflow', 'alteryx': 'Alteryx', 'asp.net': 'ASP.NET', 'atlassian': 'Atlassian', 
    'excel': 'Excel', 'power_bi': 'Power BI', 'tableau': 'Tableau', 'srss': 'SRSS', 'word': 'Word', 
    'unix': 'Unix', 'vue': 'Vue', 'jquery': 'jQuery', 'linux/unix': 'Linux / Unix', 'seaborn': 'Seaborn', 
    'microstrategy': 'MicroStrategy', 'spss': 'SPSS', 'visio': 'Visio', 'gdpr': 'GDPR', 'ssrs': 'SSRS', 
    'spreadsheet': 'Spreadsheet', 'aws': 'AWS', 'hadoop': 'Hadoop', 'ssis': 'SSIS', 'linux': 'Linux', 
    'sap': 'SAP', 'powerpoint': 'PowerPoint', 'sharepoint': 'SharePoint', 'redshift': 'Redshift', 
    'snowflake': 'Snowflake', 'qlik': 'Qlik', 'cognos': 'Cognos', 'pandas': 'Pandas', 'spark': 'Spark', 'outlook': 'Outlook'
}

keywords_programming = {
    'sql' : 'SQL', 'python' : 'Python', 'r' : 'R', 'c':'C', 'c#':'C#', 'javascript' : 'JavaScript', 'js':'JS', 'java':'Java', 
    'scala':'Scala', 'sas' : 'SAS', 'matlab': 'MATLAB', 'c++' : 'C++', 'c/c++' : 'C / C++', 'perl' : 'Perl','go' : 'Go',
    'typescript' : 'TypeScript','bash':'Bash','html' : 'HTML','css' : 'CSS','php' : 'PHP','powershell' : 'Powershell',
    'rust' : 'Rust', 'kotlin' : 'Kotlin','ruby' : 'Ruby','dart' : 'Dart','assembly' :'Assembly',
    'swift' : 'Swift','vba' : 'VBA','lua' : 'Lua','groovy' : 'Groovy','delphi' : 'Delphi','objective-c' : 'Objective-C',
    'haskell' : 'Haskell','elixir' : 'Elixir','julia' : 'Julia','clojure': 'Clojure','solidity' : 'Solidity',
    'lisp' : 'Lisp','f#':'F#','fortran' : 'Fortran','erlang' : 'Erlang','apl' : 'APL','cobol' : 'COBOL',
    'ocaml': 'OCaml','crystal':'Crystal','javascript/typescript' : 'JavaScript / TypeScript','golang':'Golang',
    'nosql': 'No SQL', 'mongodb' : 'MongoDB','t-sql' :'Transact-SQL', 'no-sql' : 'No-SQL','visual_basic' : 'Visual Basic',
    'pascal':'Pascal', 'mongo' : 'Mongo', 'pl/sql' : 'PL/SQL','sass' :'Sass', 'vb.net' : 'VB.NET','mssql' : 'MSSQL',
}

# Skill sort, count, and filter list data
def agg_skill_data(jobs_df):
    keywords_all = {**keywords_skills, **keywords_programming}
    for index, row in jobs_df.iterrows():
        for i, token in enumerate(row['description_tokens']):
            if token.lower() in keywords_all:
                row['description_tokens'][i] = keywords_all[token.lower()]
        jobs_df.at[index, 'description_tokens'] = row['description_tokens']
    skill_data = pd.DataFrame(jobs_df.description_tokens.sum()).value_counts().rename_axis('keywords').reset_index(name='counts')
    skill_data = skill_data[skill_data.keywords != '']
    skill_data['percentage'] = skill_data.counts / len(jobs_df)
    return skill_data


# Aggregate skills daily
def agg_skill_daily_data(jobs_df):
    jobs_df['date'] = jobs_df.date_time.dt.date
    first_date = jobs_all.date.min()
    last_date = jobs_all.date.max()
    list_dates = pd.date_range(first_date,last_date,freq='d')
    list_dates = pd.DataFrame(list_dates)
    list_dates = list_dates[0].dt.date
    skill_daily_df = pd.DataFrame()
    for date in list_dates:
        date_df = jobs_df[jobs_df.date == date]
        if len(date_df) == 0: # throws error if df is blank
            continue
        date_agg_df = pd.DataFrame(date_df.description_tokens.sum()).value_counts().rename_axis('keywords').reset_index(name='counts')
        date_agg_df = date_agg_df[date_agg_df.keywords != '']
        date_agg_df['percentage'] = date_agg_df.counts / len(date_df)
        date_agg_df['date'] = date
        skill_daily_df = pd.concat([date_agg_df, skill_daily_df], ignore_index=True, axis=0)
    return skill_daily_df



skill_count = agg_skill_data(jobs_all)

print(skill_count)

# Top page build
st.markdown("## 🛠️ What is the TOP Skill for Data Analysts?!?")
col1, col2, col3, col4 = st.columns(4)
with col1:
    keyword_list = ["All Tools", "Languages"]
    keyword_choice = st.radio('Skill:', keyword_list, horizontal=False) # label_visibility="collapsed"
with col4:
    graph_list = ["All Time", "Daily Trend"]
    graph_choice = st.radio('Time:', graph_list, horizontal=False)

# Skill list for slicer... NOT USED
select_all = "Select All"
skills = list(skill_count.keywords)
skills.insert(0, select_all)

# Number skill selctor for slider
skill_dict = {"Top 5": 5, "Top 10": 10, "Top 20": 20, "Top 50": 50, "All 🥴" : len(skill_count)}

# Platform sort, count, and filter for slicer
platform_count = jobs_all.via.value_counts().rename_axis('platforms').reset_index(name='counts')
platform = list(platform_count.platforms)
platform.insert(0, select_all)

# Other Filter data for slicers
job_type = pd.DataFrame(jobs_all.schedule_type.drop_duplicates())
job_type = job_type[job_type.schedule_type.notna()]
job_type = list(job_type.schedule_type)
job_type.insert(0, select_all)

with st.sidebar:
    st.markdown("# 🛠️ Filters")
    top_n_choice = st.radio("Data Skills:", list(skill_dict.keys()))
    # skills_choice = st.selectbox("Data Skill:", skills)
    job_type_choice = st.radio("Job Type:", job_type)
    platform_choice = st.selectbox("Social Platform:", platform)

# Side column filter data transform
# if skills_choice != select_all:
#     jobs_all = jobs_all[jobs_all.description_tokens.apply(lambda x: skills_choice in x)]
if platform_choice != select_all:
    jobs_all = jobs_all[jobs_all.via.apply(lambda x: platform_choice in x)]
if job_type_choice != select_all:
    jobs_all = jobs_all[jobs_all.schedule_type.apply(lambda x: job_type_choice in str(x))]

# Skill Filters - top n and languages
skill_all_time = agg_skill_data(jobs_all)
skill_filter = skill_dict[top_n_choice]
if keyword_choice != keyword_list[0]:
    skill_all_time = skill_all_time[skill_all_time.keywords.isin(list(keywords_programming.values()))]
skill_all_time = skill_all_time.head(skill_filter)
skill_all_time_list = list(skill_all_time.keywords)



# All time line chart
selector = alt.selection_single(encodings=['x', 'y'])
all_time_chart = alt.Chart(skill_all_time).mark_bar(
    cornerRadiusTopLeft=10,
    cornerRadiusTopRight=10    
).encode(
    x=alt.X('keywords', sort=None, title="", axis=alt.Axis(labelFontSize=20) ),
    y=alt.Y('percentage', title="Likelyhood to be in Job Posting", axis=alt.Axis(format='%', labelFontSize=17, titleFontSize=17)),
    color=alt.condition(selector, 'percentage', alt.value('lightgray'), legend=None),
    tooltip=["keywords", alt.Tooltip("percentage", format=".1%")]
).add_selection(
    selector
).configure_view(
    strokeWidth=0
)

skill_daily_data = agg_skill_daily_data(jobs_all)
skill_daily_data = skill_daily_data[skill_daily_data.keywords.isin(skill_all_time_list)]

# Daily trend line chart
source = skill_daily_data
x = 'date'
y = 'percentage'
color = 'keywords'
selector = alt.selection_single(encodings=['x', 'y'])
hover = alt.selection_single(
    fields=[x],
    nearest=True,
    on="mouseover",
    empty="none",
)
lines = (
    alt.Chart(source)
    .mark_line(point="transparent")
    .encode(x=alt.X(x, title="Date", axis=alt.Axis(labelFontSize=15, titleFontSize=17)), 
        y=alt.Y(y, title="Likelyhood to be in Job Posting", 
        axis=alt.Axis(format='%', labelFontSize=17, titleFontSize=17)), 
        color=color) # Modified this
    .transform_calculate(color='datum.delta < 0 ? "red" : "lightblue"') # doesn't show red for negative delta
)
points = (
    lines.transform_filter(hover)
    .mark_circle(size=65)
    .encode(color=alt.Color("color:N", scale=None))
)
tooltips = (
    alt.Chart(source)
    .mark_rule(opacity=0)
    .encode(
        x=x,
        y=y,
        tooltip=[color, alt.Tooltip(y, format=".1%"), x],
    )
    .add_selection(hover)
)
daily_trend_chart = (lines + points + tooltips).interactive().configure_view(strokeWidth=0)

if graph_choice == graph_list[0]:
    st.altair_chart(all_time_chart, use_container_width=True)
else:
    st.altair_chart(daily_trend_chart, use_container_width=True)

# Previous Daily Trend Chart
# selector = alt.selection_single(encodings=['x', 'y'])
# daily_trend_chart = alt.Chart(skill_daily_data).mark_line().encode(
#     x=alt.X('date', title=""),
#     y=alt.Y('percentage', title="Likelyhood to be in Job Posting", axis=alt.Axis(format='%', labelFontSize=17, titleFontSize=17)),
#     strokeDash='keywords',
#     color=alt.condition(selector, 'keywords', alt.value('lightgray')),
#     tooltip=["keywords", alt.Tooltip("percentage", format=".1%"), "date"]
# ).add_selection(
#     selector
# ).configure_view(
#     strokeWidth=0
# )