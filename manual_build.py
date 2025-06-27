import streamlit as st
import warnings 
import pandas as pd
from functions import functions

warnings.filterwarnings("ignore")

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.title(":material/settings: Build Your Healthcare Data Teams")
st.header("Focus on shaping what you might like your team to look like")
# with st.sidebar:
#     st.button("Test Primary Colour")

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
    "Data Analytics",
    "Data Engineering",
    "Data Science",
    "Performance",
    "Quality and Safety",
    "Workforce",
    "Info Governance",
    "Leadership"
]

team_colours = {
    "Data Analytics":"#029e73",     # green
    "Data Engineering":"#de8f05",   # orange
    "Data Science":"#0173b2",       # blue
    "Performance":"#cc78bc",        # mauve
    "Quality and Safety":"#d55e00", # terracotta
    "Workforce":"#ece133",          # yellow
    "Info Governance":"#006374",    # teal
    "Leadership": "#808080"         # black/grey
}

tab_danalytics, tab_dend, tab_dsor, tab_perf, tab_qands, tab_workforce, tab_igov, tab_lead = st.tabs(tab_list)

with tab_danalytics:
    danalytic_total, danalytic_df = functions.build_team_tab("Data Analytics",team_colours["Data Analytics"])     
    tabs_total.append(danalytic_total) 
    danalytic_df['Team'] = "Data Analytics"
    
with tab_dend:
    dend_total, dend_df = functions.build_team_tab("Data Engineering",team_colours["Data Engineering"])     
    tabs_total.append(dend_total) 
    dend_df['Team'] = "Data Engineering"
    
with tab_dsor:
    dsor_total, dsor_df = functions.build_team_tab("Data Science",team_colours["Data Science"])  
    tabs_total.append(dsor_total) 
    dsor_df['Team'] = "Data Science"
    
with tab_perf:
    perf_total, perf_df = functions.build_team_tab("Performance",team_colours["Performance"])     
    tabs_total.append(perf_total) 
    perf_df['Team'] = "Performance"

with tab_qands:
    qands_total, qands_df = functions.build_team_tab("Quality and Safety",team_colours["Quality and Safety"])    
    tabs_total.append(qands_total) 
    qands_df['Team'] = "Quality and Safety"
    
with tab_workforce:
    workforce_total, workforce_df = functions.build_team_tab("Workforce",team_colours["Workforce"])     
    tabs_total.append(workforce_total) 
    workforce_df['Team'] = "Workforce"
    
with tab_igov:
    igov_total, igov_df = functions.build_team_tab("Info Governance",team_colours["Info Governance"])    
    tabs_total.append(igov_total) 
    igov_df['Team'] = "Info Governance"

with tab_lead:
    lead_total, lead_df = functions.build_team_tab("Leadership",team_colours["Leadership"])    
    tabs_total.append(lead_total) 
    lead_df['Team'] = "Leadership"
    

df_list = [danalytic_df, dend_df, dsor_df, perf_df, qands_df, workforce_df, igov_df, lead_df]
combined_df = pd.concat(df_list, axis=0)  
# print(combined_df)

st.session_state.all_tabs_total = sum(tabs_total)
# print(tabs_total)

container_waffle = st.container(border=True)
with container_waffle:
    st.markdown(
        f"### Combined Total Cost Across All Teams: **£{st.session_state.all_tabs_total:,.0f}**"
    )
    # print(tabs_total)
    # print(sum(tabs_total))
    if sum(tabs_total) > 0:
        tb = Budget * 1000000
        total_budget = int(tb)
        functions.calc_budget_percentage(tab_list, tabs_total, total_budget, team_colours) # waffle chart
        
container_combined_org = st.container(border=True)
with container_combined_org:
    st.markdown("### Overall All Data Teams Structure")
    functions.create_combined_org_diagram(combined_df, team_colours)
