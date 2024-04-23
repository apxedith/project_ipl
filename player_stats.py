import streamlit as st
import json
import pandas as pd
from tabulate import tabulate

def display_player_details(player):
    df = pd.read_csv('assets/stat_df.csv')
    playerName = player['Player_Name']
    # Filter the DataFrame for the selected player
    player_df = df[df['Player_Name'] == playerName]

    # Convert DataFrame to a tabular format
    batting_fielding_table = tabulate(player_df[['Year', 'Mat', 'NO', 'Runs', 'HS', 'BAvg', 'BF', 'BSR', '100s', '50s', '4s', '6s', 'CT', 'S']], headers='keys', tablefmt='html', showindex=False)
    bowling_table = tabulate(player_df[['Year', 'Mat', 'Balls', 'RC', 'W', 'BoAvg', 'E', 'BoSR', '4W', '5W']], headers='keys', tablefmt='html', showindex=False)

    table_style = '<style> table {border-collapse: collapse;} th, td {border: 1px solid black; padding: 8px;} </style>'
    
    # Display Batting and Fielding table
    st.subheader("Batting and Fielding")
    st.write(table_style, unsafe_allow_html=True)
    st.write(batting_fielding_table, unsafe_allow_html=True)

    # Display Bowling table
    st.subheader("Bowling")
    st.write(table_style, unsafe_allow_html=True)
    st.write(bowling_table, unsafe_allow_html=True)

def app():
    st.markdown("<h1 style='text-align: center; color: white;'> Player Statistics </h1>", unsafe_allow_html=True)
    # Read player data from JSON file
    with open('assets/player_data.json') as f:
        players = json.load(f)
    
    # Filter search based on player name
    search_query = st.text_input("Search for a player")
    
    # Iterate through each player and display details
    for player in players:
        # Check if the player matches the search query
        if search_query.lower() in player['Player_Name'].lower():
            # Create two columns for image and statistics
            col1, col2 = st.columns([1, 1])
            # Display player image and name in the first column
            with col1:
                st.subheader(player['Player_Name'])
                if player['img_url'] is not None:
                    st.image(player['img_url'], width=100)
                else:
                    st.write("Image not available")
                
                st.write(player['Type'])
                
            # Display player statistics in the second column
            with col2:
                stats_table = """
                | Statistic           | Value   |
                |---------------------|---------|
                | Matches             | {}      |
                | Runs                | {}      |
                | Batting Strike Rate | {:.2f}  |
                | Wickets             | {}      |
                | Bowling Strike Rate | {:.2f}  |
                """.format(player['Matches_Batted'], player['Runs_Scored'], player['Batting_Strike_Rate'], player['Wickets_Taken'], player['Bowling_Strike_Rate'],)
                
                st.markdown(stats_table, unsafe_allow_html=True)
                

            st.write("")
            st.write("")
            button_key = f"view_more_{player['Player_Name']}"  # Unique key for each button
            view_more_pressed = st.button("View More", key=button_key)
            if view_more_pressed:
                display_player_details(player)
            elif not view_more_pressed:
                st.empty()  # Remove the displayed player details
                    
            st.write("---")

if __name__ == "__main__":
    app()
