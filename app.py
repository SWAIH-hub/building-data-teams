import streamlit as st
import warnings 
import pandas as pd

warnings.filterwarnings("ignore")


st.set_page_config(page_title="Data Teams", page_icon=":muscle:", layout="wide")
# LOGO_FILE = "assets/SWAIH_logo.png"
# st.logo(LOGO_FILE)


with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


pg = st.navigation(

    [st.Page("homepage.py",
             title="Homepage",
             icon=":material/cottage:"),
    st.Page("manual_build.py",
             title="Manually Build Your Teams",
             icon=":material/settings:"),
    st.Page("current_team.py",
             title="Upload Your Current Team",
             icon=":material/publish:"
            ),     
    st.Page("derive_team.py",
             title="Team Derivation Wizard",
             icon=":material/star:"
            ),                                                   
     
     ]
     )

pg.run()


