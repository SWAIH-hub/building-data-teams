import streamlit as st
import pandas as pd
import json
from functions import functions
from pywaffle import Waffle
import matplotlib.pyplot as plt


st.title("Team Derivation Wizard")
st.markdown("Answer a few questions and we'll build a draft data team for you!")

def get_salary(band, level):
    try:
        return pay_data.get(band, {}).get(level, {}).get("salary", 0)
    except Exception as e:
        st.warning(f"Error fetching salary for {band} ({level}): {e}")
        return 0
    
        
# Clusters
cluster_library = {
    "7,6,5": ["7", "6", "5"],
    "7,6,6": ["7", "6", "6"],
    "7,6,5,5": ["7", "6", "5", "5"],
    "6,5": [ "6", "5"],
    "7,6": ["7", "6"]
}

team_options = {
    "Data Analytics": {},
    "Data Science": {},
    "Data Engineering": {},
    "Performance": {},
    "Quality and Safety": {},
    "Workforce": {},
    "Info Governance": {}
}

selected_teams = st.multiselect("Which teams do you need?", options=list(team_options.keys()))

cluster_df_rows = []

for team in selected_teams:
    st.subheader(team)
    st.markdown("✅ This team will automatically get one Band 8A lead.")

    cluster_df_rows.append({
        "Team": team,
        "Band": "8A",
        "Entry Qty": 1,
        "Intermediate Qty": 0,
        "Top Qty": 0
    })
    
    st.markdown("### Add clusters to build the team:")
    for cluster_name, bands in cluster_library.items():
        count = st.number_input(
            f"How many '{cluster_name}' clusters for {team}?",
            min_value=0,
            step=1,
            key=f"{team}_{cluster_name}"
        )
        for _ in range(count):
            for band in bands:
                cluster_df_rows.append({
                    "Team": team,
                    "Band": band,
                    "Entry Qty": 1,
                    "Intermediate Qty": 0,
                    "Top Qty": 0
                })

# Leadership logic
if len(selected_teams) >= 2:
    st.markdown("---")
    st.subheader("Leadership")
    st.markdown("You've selected multiple teams. We'll add a Band 9 to oversee them.")

    cluster_df_rows.append({
        "Team": "Leadership",
        "Band": "9",
        "Entry Qty": 1,
        "Intermediate Qty": 0,
        "Top Qty": 0
    })

    add_deputy = st.checkbox("Add a Band 8B deputy to support the Band 9?")
    if add_deputy:
        cluster_df_rows.append({
            "Team": "Leadership",
            "Band": "8B",
            "Entry Qty": 1,
            "Intermediate Qty": 0,
            "Top Qty": 0
        })

if cluster_df_rows:
    cluster_df = pd.DataFrame(cluster_df_rows)

    with open("data/paybands.json") as f:
        pay_data = json.load(f)

    cluster_df["Band"] = cluster_df["Band"].astype(str).str.strip().str.lower()
    cluster_df["Band"] = cluster_df["Band"].apply(lambda x: f"Band {x}" if not x.startswith("band") else x.title())

    cluster_df["Entry Salary"] = cluster_df["Band"].apply(lambda b: get_salary(b, "entry"))
    cluster_df["Intermediate Salary"] = cluster_df["Band"].apply(lambda b: get_salary(b, "intermediate"))
    cluster_df["Top Salary"] = cluster_df["Band"].apply(lambda b: get_salary(b, "top"))

    cluster_df["Intermediate Qty"] = 0
    cluster_df["Top Qty"] = 0
    cluster_df["Total Cost"] = (
        cluster_df["Entry Salary"] * cluster_df["Entry Qty"]
    )

    st.markdown("## Derived Team Structure and Costs")
    display_df = cluster_df.copy()
    display_df["Total Cost"] = display_df["Total Cost"].apply(lambda x: f"£{x:,.0f}")

    st.dataframe(display_df[["Team", "Band", "Entry Qty", "Total Cost"]].style.hide(axis="index"))

    # st.dataframe(cluster_df[["Team", "Band", "Entry Qty", "Total Cost"]])

    st.markdown("## Combined Org Chart")
    team_colours = {
        "Data Analytics": "#029e73",
        "Data Engineering": "#de8f05",
        "Data Science": "#0173b2",
        "Performance": "#cc78bc",
        "Quality and Safety": "#d55e00",
        "Workforce": "#ece133",
        "Info Governance": "#006374",
        "Leadership": "#808080"
    }
    functions.create_combined_org_diagram(cluster_df, team_colours)
    
    total_cost = cluster_df["Total Cost"].sum()
    st.markdown(f"## Overall Estimated Total Cost: :blue-background[£**{total_cost:,.0f}**]")
        # st.metric("Total Estimated Annual Cost", f"£{total_cost:,.0f}")

    st.markdown("## Team Composition Breakdown")

    team_costs = cluster_df.groupby("Team")["Total Cost"].sum()
    overall_total_cost = team_costs.sum()
    team_percentages = (team_costs / overall_total_cost * 100).round(0)
    colours = [team_colours.get(team, "lightgrey") for team in team_percentages.index]
    legend_labels = [f"{team} ({int(percent)}%)" for team, percent in team_percentages.items()]

    fig = plt.figure(
        FigureClass=Waffle,
        rows=5,
        values=team_percentages.to_dict(),
        colors=colours,
        title={"label": "Team Composition (%)", "loc": "center"},
        legend={
            'loc': 'upper left',
            'bbox_to_anchor': (1, 1),
            'labels': legend_labels
        },
        figsize=(12, 5),
        rounding_rule='floor'
    )

    st.pyplot(fig)

else:
    st.info("Please select at least one team to build your structure.")
