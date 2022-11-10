import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title='🛠️ Skills', page_icon = 'images/luke_Favicon.png')

# import and cleanup dataframe
@st.experimental_memo
def fetch_and_clean_data():
    data_url = 'https://storage.googleapis.com/gsearch_share/gsearch_jobs.csv'
    jobs_data = pd.read_csv(data_url).replace("'","", regex=True)
    jobs_data.date_time = pd.to_datetime(jobs_data.date_time) # convert to date time
    jobs_data = jobs_data.drop(labels=['Unnamed: 0', 'index'], axis=1, errors='ignore')
    jobs_data.description_tokens = jobs_data.description_tokens.str.strip("[]").str.split(",") # fix major formatting issues with tokens
    jobs_data.description_tokens = jobs_data.description_tokens.apply(lambda row: [x.strip(" ") for x in row]) # remove whitespace from tokens
    return jobs_data

jobs_all = fetch_and_clean_data()

# Skill sort, count, and filter list data
def agg_skill_data(jobs_df):
    skill_data = pd.DataFrame(jobs_df.description_tokens.sum()).value_counts().rename_axis('keywords').reset_index(name='counts')
    skill_data = skill_data[skill_data.keywords != '']
    skill_data['percentage'] = skill_data.counts / len(jobs_df)
    return skill_data

skill_count = agg_skill_data(jobs_all)

# Top page build
st.markdown("## 🛠️ What is the TOP skill for data analyts?!?")
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
keywords_programming = [
'sql', 'python', 'r', 'c', 'c#', 'javascript', 'js',  'java', 'scala', 'sas', 'matlab', 'c++', 'c/c++', 'perl', 'go', 'typescript', 'bash', 'html', 
'css', 'php', 'powershell', 'rust', 'kotlin', 'ruby',  'dart', 'assembly', 'swift', 'vba', 'lua', 'groovy', 'delphi', 'objective-c', 'haskell', 
'elixir', 'julia', 'clojure', 'solidity', 'lisp', 'f#', 'fortran', 'erlang', 'apl', 'cobol', 'ocaml', 'crystal', 'javascript/typescript', 'golang',]
skill_all_time = agg_skill_data(jobs_all)
skill_filter = skill_dict[top_n_choice]
if keyword_choice != keyword_list[0]:
    skill_all_time = skill_all_time[skill_all_time.keywords.isin(keywords_programming)]
skill_all_time = skill_all_time.head(skill_filter)
skill_all_time_list = list(skill_all_time.keywords)

# All time line chart
all_time_chart = alt.Chart(skill_all_time).mark_bar(
    cornerRadiusTopLeft=10,
    cornerRadiusTopRight=10    
).encode(
    x=alt.X('keywords', sort=None, title="", axis=alt.Axis(labelFontSize=20) ),
    y=alt.Y('percentage', title="Likelyhood to be in Job Posting", axis=alt.Axis(format='%', labelFontSize=17, titleFontSize=17)),
)

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

skill_daily_data = agg_skill_daily_data(jobs_all)
skill_daily_data = skill_daily_data[skill_daily_data.keywords.isin(skill_all_time_list)]

# Daily trend line chart
daily_trend_chart = alt.Chart(skill_daily_data).mark_line().encode(
    x=alt.X('date', title=""),
    y=alt.Y('percentage', title="Likelyhood to be in Job Posting", axis=alt.Axis(format='%', labelFontSize=17, titleFontSize=17)),
    color='keywords',
    strokeDash='keywords',
)

if graph_choice == graph_list[0]:
    st.altair_chart(all_time_chart, use_container_width=True)
else:
    st.altair_chart(daily_trend_chart, use_container_width=True)

# Streamlit chart fail... can't sort
# st.bar_chart(data=skill_updated.head(10), x='keywords', y='percentage')

# Matplotlib fail... too complicated
# fig, ax = plt.subplots()
# color = np.random.rand(len(skill_updated.keywords), 3)
# ax.bar(x="keywords", height="percentage", data=skill_updated.head(10) , color=color).xticks(rotation = 45, ha='right')
# st.pyplot(fig)


##########
# Footer #                         #  https://discuss.streamlit.io/t/st-footer/6447
##########
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):
    style = """
    <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp { bottom: 0px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        right=0,
        bottom=0,
        margin=px(0, 100, 0, 0),
        text_align="center",
        opacity=1,
    )

    body = p()
    foot = div(
        style=style_div
    )(
        body
    )

    st.markdown(style, unsafe_allow_html=True)
    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)
    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    myargs = [
        link("https://serpapi.com/", image('https://github.com/lukebarousse/Data_Analyst_Streamlit_App_V1/raw/main/images/SerpAPI_v1.png',)),
    ]
    layout(*myargs)

if __name__ == "__main__":
    footer()