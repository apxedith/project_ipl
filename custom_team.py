import json
import streamlit as st
import matplotlib.pyplot as plt

with open('assets/player_data.json') as f:
    player_stats = json.load(f)
player_stats_dict = {player['Player_Name']: player for player in player_stats}

def calculate_total_score(selected_players):
    total_score = 0
    for player_name in selected_players:
        player_info = next((player for player in player_stats if player['Player_Name'] == player_name), None)
        if player_info:
            total_score += player_info['player_score']
    return total_score
def load_players_data():
    with open('assets/player_data.json', 'r') as f:
        data = json.load(f)
    return data

def filter_players_by_type(players_data, player_types, selected_players):
    return [player["Player_Name"] for player in players_data if player["Type"] in player_types and player["Player_Name"] not in selected_players]

def app():
    st.markdown("<h1 style='text-align: center; color: white;'> Custom Line Up </h1>", unsafe_allow_html=True)

    # Load player data
    players_data = load_players_data()

    # Initialize team selections
    team1_selected_players = []
    team2_selected_players = []

    # Function to update available players based on selected players
    def update_available_players(selected_players):
        return [player for player in players_data if player["Player_Name"] not in selected_players]

    # Display player selection for Team 1
    st.header("Team 1 Selection")
    
    # Select box for bowlers
    
    team1_bowlers = st.multiselect("Select 3 Bowlers", options=filter_players_by_type(players_data, ["Bowler"], team1_selected_players), key="team1_bowlers")
    if len(team1_bowlers) != 3:
        st.warning("Please select exactly 3 bowlers.")
    team1_selected_players.extend(team1_bowlers)
    players_data = update_available_players(team1_selected_players)

    # Select box for batsmen
    team1_batsmen = st.multiselect("Select 3 Batsmen", options=filter_players_by_type(players_data, ["Batsman"], team1_selected_players), key="team1_batsmen")
    if len(team1_batsmen) != 3:
            st.warning("Please select exactly 3 batsmen.")
    team1_selected_players.extend(team1_batsmen)
    players_data = update_available_players(team1_selected_players)

    # Select box for wicketkeeper
    team1_wk = st.selectbox("Select a Wicketkeeper", options=filter_players_by_type(players_data, ["Wicket Keeper-Batsman", "Wicket Keeper-Bowler"], team1_selected_players), key="team1_wk",index=None)
    team1_selected_players.append(team1_wk)
    players_data = update_available_players(team1_selected_players)

    team1_a = st.selectbox("Select a All-Rounder", options=filter_players_by_type(players_data, ["All-rounder"], team1_selected_players), key="team1_a",index=None)
    team1_selected_players.append(team1_a)
    players_data = update_available_players(team1_selected_players)

    # Select box for remaining players for Team 1
    remaining_player_types = ["Bowler", "Batsman", "All-Rounder"]
    remaining_players_team1 = filter_players_by_type(players_data, remaining_player_types, team1_selected_players)
    
    selected_remaining_players_team1 = st.multiselect("Select Remaining Players for Team 1", options=remaining_players_team1, key="team1_remaining")
    team1_selected_players.extend(selected_remaining_players_team1)
    players_data = update_available_players(team1_selected_players)

    # Ensure exactly 11 players are selected for Team 1
    if len(team1_selected_players) < 11:
        st.warning("Please select remaining players for Team 1.")
    elif len(team1_selected_players) > 11:
        st.error("Too many players selected for Team 1. Please review your selections.")
    else:
        st.success("Team 1 selection is complete.")

    # Display selected players for Team 1
    st.write("Selected players for Team 1:",)
    col1, col2 = st.columns([1, 1])

# Loop through each selected player
    for player_name in team1_selected_players:
    # Get player data based on player name
        player = player_stats_dict.get(player_name, None) # You need to implement this function to fetch player data
    
        if player is not None:
            # Create a grid layout for each player
            col1, col2 = st.columns([1, 1])
            
            # Display player image, name, type, and score
            with col1:
                st.subheader(player['Player_Name'])
                if player['img_url'] is not None:
                    st.image(player['img_url'], width=100)
                else:
                    st.write("Image not available")
                
                st.write(player['Type'])
                score = player["player_score"]
                formatted_score = "{:.2f}".format(score)
                st.write(f"Score : {formatted_score}")
            
            # Add a divider between columns
            col1.write("---")

    # Display player selection for Team 2
    st.header("Team 2 Selection")

    # Select box for bowlers
    team2_bowlers = st.multiselect("Select 3 Bowlers", options=filter_players_by_type(players_data, ["Bowler"], team2_selected_players), key="team2_bowlers",)
    if len(team2_bowlers) != 3:
        st.warning("Please select exactly 3 bowlers.")
    team2_selected_players.extend(team2_bowlers)
    players_data = update_available_players(team2_selected_players)

    # Select box for batsmen
    
    team2_batsmen = st.multiselect("Select 3 Batsmen", options=filter_players_by_type(players_data, ["Batsman"], team2_selected_players), key="team2_batsmen")
    if len(team2_batsmen) != 3:
        st.warning("Please select exactly 3 batsmen.")
    team2_selected_players.extend(team2_batsmen)
    players_data = update_available_players(team2_selected_players)

    # Select box for wicketkeeper
    team2_wk = st.selectbox("Select a Wicketkeeper", options=filter_players_by_type(players_data, ["Wicket Keeper-Batsman", "Wicket Keeper-Bowler"], team2_selected_players), key="team2_wk",index=None)
    team2_selected_players.append(team2_wk)
    players_data = update_available_players(team2_selected_players)

    team2_a = st.selectbox("Select an All-Rounder", 
                       options=filter_players_by_type(players_data, ["All-rounder"], team2_selected_players,), 
                       key="team2_a",index=None)
    team2_selected_players.append(team2_a)
    players_data = update_available_players(team2_selected_players)

    # Select box for remaining players for Team 2
    remaining_players_team2 = filter_players_by_type(players_data, remaining_player_types, team2_selected_players)
    selected_remaining_players_team2 = st.multiselect("Select Remaining Players for Team 2", options=remaining_players_team2, key="team2_remaining")
    team2_selected_players.extend(selected_remaining_players_team2)
    players_data = update_available_players(team2_selected_players)

    # Ensure exactly 11 players are selected for Team 2
    if len(team2_selected_players) < 11:
        st.warning("Please select remaining players for Team 2.")
    elif len(team2_selected_players) > 11:
        st.error("Too many players selected for Team 2. Please review your selections.")
    else:
        st.success("Team 2 selection is complete.")


    st.write("Selected players for Team 2:", )
    col3, col4 = st.columns([1, 1])

# Loop through each selected player
    for player_name in team2_selected_players:
    # Get player data based on player name
        player = player_stats_dict.get(player_name, None) # You need to implement this function to fetch player data
    
        if player is not None:
            # Create a grid layout for each player
            col3, col4 = st.columns([1, 1])
            
            # Display player image, name, type, and score
            with col3:
                st.subheader(player['Player_Name'])
                if player['img_url'] is not None:
                    st.image(player['img_url'], width=100)
                else:
                    st.write("Image not available")
                
                st.write(player['Type'])
                score = player["player_score"]
                formatted_score = "{:.2f}".format(score)
                st.write(f"Score : {formatted_score}")
            
            # Add a divider between columns
            col3.write("---")
 # Prediction and outcome
    if st.button("Predict"):
        team1_total_score = calculate_total_score(team1_selected_players)
        team2_total_score = calculate_total_score(team2_selected_players)
        if team1_total_score > team2_total_score:
            st.success("Team 1 is predicted to win!")
        elif team1_total_score < team2_total_score:
            st.success("Team 2 is predicted to win!")
        else:
            st.warning("It's predicted to be a tie!")

        average_score_team1 = team1_total_score / 11
        average_score_team2 = team2_total_score / 11

        # Plot the graph using Streamlit's st.pyplot() function
        
        teams = ['Team 1', 'Team 2']
        average_scores = [average_score_team1, average_score_team2]

        fig, ax = plt.subplots()
        ax.bar(teams, average_scores, color=['blue', 'green'])
        ax.set_xlabel('Team')
        ax.set_ylabel('Average Score per Player')
        ax.set_title('Average Score of Team')

        # Display the plot in Streamlit
        st.pyplot(fig)


if __name__ == "__main__":
    app()
