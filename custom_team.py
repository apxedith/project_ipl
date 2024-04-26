import json
import streamlit as st

with open('assets/player_data.json') as f:
    player_stats = json.load(f)

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
    st.markdown("<h1 style='text-align: center; color: white;'> Custom Team Win Predictor </h1>", unsafe_allow_html=True)

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
    st.subheader("Select 3 Bowlers for Team 1")
    team1_bowlers = st.multiselect("Select Bowlers", options=filter_players_by_type(players_data, ["Bowler"], team1_selected_players), key="team1_bowlers")
    team1_selected_players.extend(team1_bowlers)
    players_data = update_available_players(team1_selected_players)

    # Select box for batsmen
    st.subheader("Select 3 Batsmen for Team 1")
    team1_batsmen = st.multiselect("Select Batsmen", options=filter_players_by_type(players_data, ["Batsman"], team1_selected_players), key="team1_batsmen")
    team1_selected_players.extend(team1_batsmen)
    players_data = update_available_players(team1_selected_players)

    # Select box for wicketkeeper
    st.subheader("Select 1 Wicketkeeper for Team 1")
    team1_wk = st.selectbox("Select Wicketkeeper", options=filter_players_by_type(players_data, ["Wicket Keeper-Batsman", "Wicket Keeper-Bowler"], team1_selected_players), key="team1_wk")
    team1_selected_players.append(team1_wk)
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
    st.write("Selected players for Team 1:", team1_selected_players)

    # Display player selection for Team 2
    st.header("Team 2 Selection")

    # Select box for bowlers
    st.subheader("Select 3 Bowlers for Team 2")
    team2_bowlers = st.multiselect("Select Bowlers", options=filter_players_by_type(players_data, ["Bowler"], team2_selected_players), key="team2_bowlers",)
    team2_selected_players.extend(team2_bowlers)
    players_data = update_available_players(team2_selected_players)

    # Select box for batsmen
    st.subheader("Select 3 Batsmen for Team 2")
    team2_batsmen = st.multiselect("Select Batsmen", options=filter_players_by_type(players_data, ["Batsman"], team2_selected_players), key="team2_batsmen")
    team2_selected_players.extend(team2_batsmen)
    players_data = update_available_players(team2_selected_players)

    # Select box for wicketkeeper
    st.subheader("Select 1 Wicketkeeper for Team 2")
    team2_wk = st.selectbox("Select Wicketkeeper", options=filter_players_by_type(players_data, ["Wicket Keeper-Batsman", "Wicket Keeper-Bowler"], team2_selected_players), key="team2_wk")
    team2_selected_players.append(team2_wk)
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


    st.write("Selected players for Team 2:", team2_selected_players)
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


if __name__ == "__main__":
    app()
