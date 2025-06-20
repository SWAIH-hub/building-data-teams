import streamlit as st
import pandas as pd
import json
from pywaffle import Waffle
import matplotlib.pyplot as plt
import networkx as nx

def build_team_tab(team_name: str,team_col:dict ) -> float:
    json_path: str = "data/paybands.json"
    col1, col2, col3 = st.columns([6,2,4])

    with col1:
        container1 = st.container(border=True)
        container1.markdown(f"### Build your {team_name} Team...")
        try:
            with open(json_path, "r") as f:
                pay_progression = json.load(f)

            rows = []
            for band, levels in pay_progression.items():
                rows.append({
                    "Band": band,
                    "Entry Salary": levels["entry"]["salary"],
                    "Entry Qty": 0,
                    "Intermediate Salary": levels["intermediate"]["salary"],
                    "Intermediate Qty": 0,
                    "Top Salary": levels["top"]["salary"],
                    "Top Qty": 0
                })

            df = pd.DataFrame(rows)
            df = df.iloc[::-1].reset_index(drop=True)
            display_df = df.copy()

            for col in ["Entry Salary", "Intermediate Salary", "Top Salary"]:
                display_df[col] = display_df[col].apply(lambda x: f"£{x:,.0f}")

            edited_df = container1.data_editor(
                display_df,
                column_config={
                    "Entry Qty": st.column_config.NumberColumn("Entry Qty", min_value=0),
                    "Intermediate Qty": st.column_config.NumberColumn("Intermediate Qty", min_value=0),
                    "Top Qty": st.column_config.NumberColumn("Top Qty", min_value=0),
                },
                disabled=["Band", "Entry Salary", "Intermediate Salary", "Top Salary"],
                use_container_width=True,
                key=f"{team_name}_editor"
            )

            for col in ["Entry Salary", "Intermediate Salary", "Top Salary"]:
                df[col] = df[col].astype(int)
            for qty_col in ["Entry Qty", "Intermediate Qty", "Top Qty"]:
                df[qty_col] = edited_df[qty_col]

            df["Total Cost"] = (
                df["Entry Salary"] * df["Entry Qty"] +
                df["Intermediate Salary"] * df["Intermediate Qty"] +
                df["Top Salary"] * df["Top Qty"]
            )
        
        except FileNotFoundError:
            st.error(f"File not found: {json_path}")
        except json.JSONDecodeError:
            st.error("Error decoding JSON. Please check the file format.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return 0.0

    with col2:
        container2 = st.container(border=True)

        container2.markdown("### Total Cost by Band")
        container2.dataframe(df[["Band", "Total Cost"]].assign(**{
            "Total Cost": lambda d: d["Total Cost"].apply(lambda x: f"£{x:,.0f}")
        }), hide_index=True)

    container3 = st.container(border=True)
    overall_cost = df["Total Cost"].sum()
    container3.markdown(f"### Overall :blue-background[{team_name} Team] Total Cost: :blue-background[£**{overall_cost:,.0f}**]")
    # print(df)
    
    with col3:
        chart_container = st.container(border=True)
        with chart_container:
            create_org_diagram(df,team_col) # team org chart

    return overall_cost, df


def calc_budget_percentage(team, totals, overall_budget, team_col:dict):
    
    if overall_budget <= 0:
        st.error("Overall budget must be greater than zero")
        return
    
    if len(team) != len(totals):
        st.error("Teams and totals lists must be the same length")
        return
    
    df = pd.DataFrame({'team': team, 'total': totals})
    df = df.dropna()
    
    if df.empty:
        st.error("No valid data to display")
        return
    
    total_used = df["total"].sum()
    remaining_budget = overall_budget - total_used
    
    # Calculate percentages (can be over 100% if over budget)
    df["percent_against_total"] = ((df["total"] / overall_budget) * 100).round(0)
    remaining_percent = (remaining_budget / overall_budget * 100).round(0)
    
    values_dict = dict(zip(df['team'], df['percent_against_total']))

    if remaining_percent > 0:
        values_dict["Remaining"] = remaining_percent
    elif remaining_percent < 0:
        values_dict["Overspend"] = abs(remaining_percent)
    
    colours = []
    for team_name in values_dict.keys():
        if team_name == "Remaining":
            colours.append("lightgrey")
        elif team_name == "Overspend":
            colours.append("red")
        else:
            colours.append(team_col.get(team_name, "lightgrey"))
            
    try:
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=values_dict,
            colors=colours,
            title={'label': 'Budget Allocation (%)', 'loc': 'center'},
            legend={
                'loc': 'upper left', 
                'bbox_to_anchor': (1, 1),
                'labels': [f"{k} ({int(v)}%)" for k, v in values_dict.items()]
            },
            figsize=(10, 4),
            rounding_rule='floor'
        )
        
        return st.pyplot(fig)
    
    except Exception as e:
        st.error(f"Error creating waffle chart: {str(e)}")
        # fallback to bar chart
        fig, ax = plt.subplots(figsize=(10, 4))
        df.plot.bar(x='team', y='percent_against_total', ax=ax)
        if remaining_percent > 0:
            ax.bar("Remaining", remaining_percent, color="lightgrey")
        elif remaining_percent < 0:
            ax.bar("Overspend", abs(remaining_percent), color="red")
        ax.set_title('Budget Allocation (%)')
        ax.set_ylabel('Percentage of Total Budget')
        return st.pyplot(fig)
    
    
def create_org_diagram(df, team_colour):
    G = nx.DiGraph()
    node_labels = {}
    node_colours = []
    node_sizes = []
    pos = {}

    active_bands = df[(df['Entry Qty'] + df['Intermediate Qty'] + df['Top Qty']) > 0]
    if active_bands.empty:
        st.warning("No active staff in this team.")
        return

    band_hierarchy = sorted(active_bands['Band'].unique().tolist(), reverse=True)
    team_name = df['Team'].iloc[0] if 'Team' in df.columns else "Team"

    previous_node = None
    for i, band in enumerate(band_hierarchy):
        node_id = f"{team_name}_{band}"
        total_qty = df.loc[df['Band'] == band, ['Entry Qty', 'Intermediate Qty', 'Top Qty']].sum().sum()

        node_labels[node_id] = f"{band}\n({int(total_qty)} ppl)\n{team_name}"
        G.add_node(node_id)
        node_colours.append(team_colour)
        node_sizes.append(1500)

        pos[node_id] = (0, -i * 3)  # y spacing of 3 units per level

        if previous_node:
            G.add_edge(previous_node, node_id)
        previous_node = node_id

    height = max(2.5, len(band_hierarchy) * 1.2)

    fig, ax = plt.subplots(figsize=(4.5, height))

    nx.draw_networkx(
        G,
        pos=pos,
        labels=node_labels,
        arrows=True,
        node_size=node_sizes,
        node_color=node_colours,
        font_size=7,
        edge_color="gray",
        ax=ax,
        bbox=dict(facecolor="white", boxstyle="round", ec="gray", pad=0.3)
    )

    ax.set_axis_off()
    plt.title(f"Organisational Structure: {team_name}", fontsize=10)

    y_min = min(y for (_, y) in pos.values()) - 2
    y_max = max(y for (_, y) in pos.values()) + 2
    ax.set_ylim(y_min, y_max)
    ax.set_xlim(-2, 2)

    st.pyplot(fig)

    
def create_combined_org_diagram(df, team_colours):
    G = nx.DiGraph()
    node_labels = {}
    node_colours = []
    node_sizes = []
    pos = {}

    x_offset = 0
    team_spacing = 8

    for team_idx, (team, colour) in enumerate(team_colours.items()):
        team_df = df[df['Team'] == team]

        active_bands_df = team_df[
            (team_df['Entry Qty'] + team_df['Intermediate Qty'] + team_df['Top Qty']) > 0
        ]

        if active_bands_df.empty:
            continue

        band_hierarchy = sorted(active_bands_df['Band'].unique().tolist(), reverse=True)

        previous_node = None
        for i, band in enumerate(band_hierarchy):
            node_id = f"{team}_{band}"
            band_row = active_bands_df[active_bands_df['Band'] == band]
            total_qty = band_row[['Entry Qty', 'Intermediate Qty', 'Top Qty']].sum().sum()

            node_labels[node_id] = f"{band}\n({int(total_qty)} ppl)\n{team}"
            G.add_node(node_id)
            node_colours.append(colour)
            node_sizes.append(1500)

            pos[node_id] = (x_offset, 10 - i * 2)

            if previous_node:
                G.add_edge(previous_node, node_id)

            previous_node = node_id

        x_offset += team_spacing  # Move right for next team

    fig, ax = plt.subplots(figsize=(min(15, x_offset), 6))

    nx.draw_networkx(
        G,
        pos=pos,
        labels=node_labels,
        arrows=True,
        node_size=node_sizes,
        node_color=node_colours,
        font_size=6,
        edge_color="gray",
        ax=ax,
        bbox=dict(facecolor="white", boxstyle="round", ec="gray", pad=0.3)
    )

    ax.set_axis_off()
    plt.title("Combined Organisational Structure by Band and Team", fontsize=10)
    st.pyplot(fig)