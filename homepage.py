import streamlit as st
import warnings 

warnings.filterwarnings("ignore")

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
    
    
st.title("Supporting Planning for Healthcare Data Teams")

container1 = st.container(border=True)
with container1:
    st.header(":material/settings: Build...")
    st.markdown("""Use to manually design your data teams - Focusing on shaping what you might like your team to look like:""")
    st.markdown("""1. Set a budget""")
    st.markdown("""2. Enter Staff Numbers""")
    st.markdown("""3. Review Budget Porportional Spend""")

container2 = st.container(border=True)
with container2:
    st.header(":material/publish: Upload...")
    st.markdown("""Use to upload and review your data teams - Focusing on reviewing your current Team Stucture:""")
    st.markdown("""1. Upload your current data team""")

container3 = st.container(border=True)
with container3:
    st.header(":material/star: Derive...")
    st.markdown("""Use the wizard to help design the teams that your need - Allow the wizard to guide you through a suggested Team Structure:""")
    st.markdown("""1. Use the wizard prompts to guide you...""")