import streamlit as st
import pandas as pd
import datetime
from modules.formater import Title, Footer

# Title page and footer
title = "📊 About"
Title().page_config(title)

st.markdown("## 📊 About")
st.markdown("### 👨🏼‍💻 Goal")
st.markdown("""
Open-sourcing job requirements for aspiring data analysts is necessary for data nerds to focus more efficiently on what skills they need to learn for their future job. This dashboard is only the beginning of that journey. \n 
""")

st.markdown("### 🤖 Resources")
st.markdown(f"""
Thanks to [SerpApi](https://serpapi.com/) for providing the resources to pull this data! 🙌🏼 [You can test out their service here](https://serpapi.com/playground?engine=google_jobs&q=Data+Analyst&location=United+States&gl=us&hl=en).  
SerpApi provides **100 searches** a month for **FREE**. When you [sign up](https://serpapi.com/users/sign_up), make sure you tell them Luke sent you to get an additional **20% OFF** paid plans!
""")

st.markdown("### 📈 Data")
st.markdown(f"""
Data is collected daily from Google job postings search results; specifically, [searching for Data Analyst in the United States](https://serpapi.com/playground?engine=google_jobs&q=Data+Analyst&location=United+States&gl=us&hl=en). As the project grows, we'll expand to other regions and disciplines. More info in links below.👇🏼 \n
""")

st.markdown("### 🔗 Links")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### [🐙 GitHub](https://github.com/lukebarousse/Data_Analyst_Streamlit_App_V1)")
    # st.image('images/octocat.png', width=150)
    st.write("Source code for project")

with col2:
    st.markdown("### [🗂️ Kaggle](https://www.kaggle.com/datasets/lukebarousse/data-analyst-job-postings-google-search)")
    # st.image('images/kaggle.png', width=125)
    st.write("Dataset with further details")

with col3:
    st.markdown("### [📺 YouTube](https://youtu.be/iNEwkaYmPqY)")
    # st.image('images/youtube.png', width=170)   
    st.write("Video about this project")