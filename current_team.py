import streamlit as st
import warnings 
import pandas as pd

warnings.filterwarnings("ignore")

# st.set_page_config(page_title="Budget Bytes", page_icon=":muscle:", layout="wide")
with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.title("Your Current Healthcare Data Teams")

st.header("Upload Your Current Teams..")

# with st.sidebar:
#     st.button("Test Primary Colour")

st.button("Download Template")
    
if 'all_tabs_total' not in st.session_state:
    st.session_state.all_tabs_total = 0
    
ideal_team_split = {
    "Data Engineering": 20,
    "Data Science": 30,
    "Data Analytics": 40,
    "Data Quailty": 10
    }

st.write("This is just a plcaeholder page and is not functional yet.")

col1, col2 = st.columns([6,6])

with col1:
    container1 = st.container(border=True)
    
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
    
        container1.data_editor(
            # df,
            column_config={
                        "name_job_role": st.column_config.TextColumn("Name/Job Role"),
                        "wte": st.column_config.NumberColumn("WTE", min_value=0),
                        "band": st.column_config.TextColumn("Band"),
                        "core_skill": st.column_config.TextColumn("Core Skills"),
                        "department": st.column_config.TextColumn("Department"),
                        "team": st.column_config.TextColumn("Team"),
                    },
                    use_container_width=True,
                    key=f"data_team_editor"
        )
    
with col2:
    pass