import streamlit as st
import warnings 
import pandas as pd
from functions import functions

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Budget Bytes", page_icon=":robot:", layout="wide")
st.logo("assets\SWAIH_logo.png", size="large") # SWAIH / Data Hub Logo 

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.title("🤖 Budget Byte - Helping Plan Your Data Teams")

st.header(":muscle: Build Your Data Teams!")

#with st.sidebar:


Budget = st.slider(
    "Budget (x £1m)",
    1.0,
    10.0,
    step=0.5,
    key="Budget",
    value=5.0
)
    
    
if 'all_tabs_total' not in st.session_state:
    st.session_state.all_tabs_total = 0
    
# st.button("Test Primary Colour")

tabs_total = []
tab_list = [
    "Data Science",
    "Data Engineering",
    "Data Analytics",
    "Audit",
    "Info Governance",
    "Performance",
    "Workforce"
]

team_colours = {
    "Data Science":"#0173b2",       # blue
    "Data Engineering":"#de8f05",   # orange
    "Data Analytics":"#029e73",     # green
    "Audit":"#d55e00",              # terracotta
    "Info Governance":"#006374",    # teal
    "Performance":"#cc78bc",        # mauve
    "Workforce":"#ece133"           # yellow
}

tab_dsor, tab_dend, tab_danalytics, tab_audit, tab_igov, tab_perf, tab_workforce = st.tabs(tab_list)

with tab_dsor:
    dsor_total, dsor_df = functions.build_team_tab("Data Science",team_colours["Data Science"])  
    tabs_total.append(dsor_total) 
    dsor_df['Team'] = "Data Science"
    

with tab_dend:
    dend_total, dend_df = functions.build_team_tab("Data Engineering",team_colours["Data Engineering"])     
    tabs_total.append(dend_total) 
    dend_df['Team'] = "Data Engineering"
    
    
with tab_danalytics:
    danalytic_total, danalytic_df = functions.build_team_tab("Data Analytics",team_colours["Data Analytics"])     
    tabs_total.append(danalytic_total) 
    danalytic_df['Team'] = "Data Analytics"
    

with tab_audit:
    audit_total, audit_df = functions.build_team_tab("Audit",team_colours["Audit"])    
    tabs_total.append(audit_total) 
    audit_df['Team'] = "Audit"
    

with tab_igov:
    igov_total, igov_df = functions.build_team_tab("Info Governance",team_colours["Info Governance"])    
    tabs_total.append(igov_total) 
    igov_df['Team'] = "Info Governance"
    

with tab_perf:
    perf_total, perf_df = functions.build_team_tab("Performance",team_colours["Performance"])     
    tabs_total.append(perf_total) 
    perf_df['Team'] = "Performance"
    

with tab_workforce:
    workforce_total, workforce_df = functions.build_team_tab("Workforce",team_colours["Workforce"])     
    tabs_total.append(workforce_total) 
    workforce_df['Team'] = "Workforce"
      


df_list = [dsor_df, dend_df, danalytic_df, audit_df, igov_df, perf_df, workforce_df]
combined_df = pd.concat(df_list, axis=0)  
print(combined_df)

st.session_state.all_tabs_total = sum(tabs_total)
print(tabs_total)

container_waffle = st.container(border=True)
with container_waffle:
    st.markdown(
        f"### 🏦 Combined Total Cost Across All Teams (year one): **£{st.session_state.all_tabs_total:,.0f}**"
    )
    # print(tabs_total)
    print(sum(tabs_total))
    if sum(tabs_total) > 0:
        tb = Budget * 1000000
        total_budget = int(tb)
        functions.calc_budget_percentage(tab_list, tabs_total, total_budget, team_colours) # waffle chart
        
container_combined_org = st.container(border=True)
with container_combined_org:
    st.markdown("### 👥 Overall All Data Teams Structure")
    functions.create_combined_org_diagram(combined_df, team_colours)
