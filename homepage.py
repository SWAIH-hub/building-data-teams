import streamlit as st
import warnings 

warnings.filterwarnings("ignore")

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
    
    
st.title("Supporting Better Planning for Healthcare Data Teams")

st.header(":muscle: Build Your Healthcare Data Teams!")

st.write("Some info about the app and how it will help you....")