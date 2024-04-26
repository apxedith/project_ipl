import streamlit as st
import pandas as pd
from tabulate import tabulate
import json


def display_team_details(team):
    with open('assets/team_stat.json', 'r') as f:
        data = json.load(f)

    team_name = team['Team_Name']
    team_data = next((item for item in data if item["team"] == team_name), None)

    if team_data:
        img_url = team_data.get('img_url')
        if img_url:
            col1, col2 = st.columns([5, 6])  # Adjust the width ratio as needed
            with col1:
                st.image(img_url, width=250)  # Display the image
            with col2:
                st.write(f"## {team_name}")  # Display team name on the right of the image
        else:
            st.write(f"### {team_name}")
            st.write("Image not available")
        # Extract required statistics
        statistics = [
            ("Mat", team_data["matches"]),
            ("Won", team_data["won"]),
            ("Loss",team_data["lost"]),
            ("T/W", team_data["tie_win"]),
            ("T/L", team_data["tie_loss"]),
            ("NR", team_data["nr"]),
            ("Win %", team_data["win_percentage"]),
            ("Loss %", team_data["loss_percentage"]),
            ("Overall %", team_data["overall_percentage"])
        ]
        table = tabulate(statistics, tablefmt="html", headers=["Statistic", "Value"])

        # Increase width of table and columns
        styled_table = f"<style> table {{ width: 70%; }} th, td {{ width: 60%; }} </style>{table}"

        # Display the table
        st.write("<h3>Team Statistics</h3>", unsafe_allow_html=True)
        st.write(styled_table, unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("<h3>Team Season Performance</h3>", unsafe_allow_html=True)
        team_df = pd.read_csv('assets/team_wins_per_season.csv')
        
        selected_team_df = team_df[team_df['team_name'] == team_name]

        # Plot the graph
        selected_team_df = selected_team_df.set_index('team_name')
        selected_team_df = selected_team_df.transpose()  # Transpose to have years as index
        st.line_chart(selected_team_df)


    else:
        st.write("Team statistics not found.")


def app():
    st.markdown("<h1 style='text-align: center; color: white;'> Team Statistics </h1>", unsafe_allow_html=True)

    with open('assets/team_stat.json', 'r') as f:
        data = json.load(f)
    team_names = [team['team'] for team in data]

    # Assuming you have a dropdown to select the team
    team_name = st.selectbox("Select Team", team_names) 
    team = {'Team_Name': team_name} 

    display_team_details(team)


if __name__ == "__main__":
    app()