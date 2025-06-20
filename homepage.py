import streamlit as st
import pandas as pd
import json
import os
import streamlit as st
import warnings 
import pandas as pd
from functions import functions

warnings.filterwarnings("ignore")

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
    
    
st.title("Supporting Better Planning for Healthcare Data Teams")

st.header(":muscle: Build Your Healthcare Data Teams!")

st.write("Some info about the app and how it will help you....")