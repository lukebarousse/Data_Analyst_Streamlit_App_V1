import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title='📊 About', page_icon = 'images/luke_Favicon.png')

# import and cleanup
data_url = 'https://storage.googleapis.com/gsearch_share/gsearch_jobs.csv'
jobs_all = pd.read_csv(data_url)
jobs_all.date_time = pd.to_datetime(jobs_all.date_time) # convert to date time
jobs_all = jobs_all.drop(labels=['Unnamed: 0', 'index'], axis=1, errors='ignore')

st.markdown("## 👨🏼‍💻 About the Project")
st.markdown("""
Open-sourcing job requirements for data analysts is necessary for aspiring data nerds to more efficently learn what they need to know for their future job. This dashboard is only the beginning of that journey. \n 
Thanks for checking this out! 🤙🏼 -Luke""")

st.markdown("## 📊 About the Data")
st.markdown(f"""
Data is collected from Google job postings search results; specifically, searching for Data Analyst in the United States. As the project grows, we'll expand to other regions and disciplines. More info on [Kaggle](https://www.kaggle.com/datasets/lukebarousse/data-analyst-job-postings-google-search). \n
Thanks to [SerpAPI](https://serpapi.com/) for providing the resources to pull this data!
""")

st.header("🔗 Links")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### [GitHub](https://github.com/lukebarousse)")
    st.image('images/octocat.png', width=150)
    st.write("Source code for project")

with col2:
    st.markdown("### [Kaggle](https://www.kaggle.com/datasets/lukebarousse/data-analyst-job-postings-google-search)")
    st.image('images/kaggle.png', width=125)
    st.write("Dataset with further details")

with col3:
    st.markdown("### [YouTube](https://www.youtube.com/lukebarousse)")
    st.image('images/youtube.png', width=170)   
    st.write("Video about this project")