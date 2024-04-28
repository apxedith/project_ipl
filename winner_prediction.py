import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from joblib import load

ipl_df = pd.read_csv("assets/ipl_data_team_wins.csv")

team_mapping = {
    'Kolkata Knight Riders': 1,
    'Chennai Super Kings': 2,
    'Delhi Capitals': 3,
    'Royal Challengers Bangalore': 4,
    'Rajasthan Royals': 5,
    'Punjab Kings': 6,
    'Sunrisers Hyderabad': 7,
    'Mumbai Indians': 8,
    'Rising Pune Supergiant': 9,
    'Kochi Tuskers Kerala': 10,
    'Gujarat Titans': 11,
    'Lucknow Super Giants': 12,
}

toss_decision_mapping = {'field': 0, 'bat': 1}

# Load the machine learning model
model = load('assets/win_predictor.pkl')

def score_predict(team1, team2, toss_winner, toss_decision, model=model):
    team1_numeric = team_mapping.get(team1, -1)
    team2_numeric = team_mapping.get(team2, -1)
    toss_winner_numeric = team_mapping.get(toss_winner, -1)
    toss_decision_numeric = toss_decision_mapping.get(toss_decision, -1)
    
    user_data = pd.DataFrame({
        'team1': [team1_numeric],
        'team2': [team2_numeric],
        'toss_winner': [toss_winner_numeric],
        'toss_decision': [toss_decision_numeric],
    })
    
    predictions = model.predict(user_data)
    return predictions[0]

id_to_team = {v: k for k, v in team_mapping.items()}

def get_match_stats(team1_name, team2_name, df=ipl_df):
    # Filter matches where either 'team1' or 'team2' is "Team X" and 'team2' or 'team1' is "Kochi Tuskers Kerala"
    matches_team1_vs_team2 = ((df['team1'] == team1_name) & (df['team2'] == team2_name)) | ((df['team2'] == team1_name) & (df['team1'] == team2_name))

    # Total matches between the given teams
    total_matches = len(df[matches_team1_vs_team2])

    # Total wins for each team
    team1_wins = len(df[(df['winner'] == team1_name) & matches_team1_vs_team2])
    team2_wins = total_matches - team1_wins

    return total_matches, team1_wins, team2_wins

def get_filtered_match_stats(ipl_df, team1_name, team2_name, toss_winner_name, toss_decision):
    # Filter matches where either 'team1' or 'team2' is "Team X" and 'team2' or 'team1' is "Kochi Tuskers Kerala"
    matches_team1_vs_team2 = ((ipl_df['team1'] == team1_name) & (ipl_df['team2'] == team2_name)) | ((ipl_df['team2'] == team1_name) & (ipl_df['team1'] == team2_name))

    # Filter matches where 'toss_winner' is "Team X" and 'toss_decision' is "bat"
    matches_team_x_toss_bat = (ipl_df['toss_winner'] == toss_winner_name) & (ipl_df['toss_decision'] == toss_decision)

    # Combine the conditions to get the final filtered matches
    filtered_matches = ipl_df[matches_team1_vs_team2 & matches_team_x_toss_bat]

    # Count the number of matches
    num_matches = len(filtered_matches)

    # Count the number of times each team won
    team1_wins = filtered_matches[filtered_matches['winner'] == team1_name].shape[0]
    team2_wins = num_matches - team1_wins


    return num_matches, team1_wins, team2_wins

def app():
    st.markdown("<h1 style='text-align: center; color: white;'> Winner Prediction </h1>", unsafe_allow_html=True)

    team1 = st.selectbox('Team 1', tuple(team_mapping.keys()), index=None)
    team2 = st.selectbox('Team 2', tuple(team_mapping.keys()), index=None)

    if team1 == team2:
        st.error('Team 1 and Team 2 should be different')
        return

    toss_winner_options = [team1, team2] if team1 and team2 else ()
    toss_winner = st.selectbox('Toss Winner', toss_winner_options,)

    toss_decision = st.selectbox('Toss Decision', ('field', 'bat'),)

    if st.button("Predict"):
        predicted = score_predict(team1, team2, toss_winner, toss_decision)
        predicted_team = id_to_team.get(predicted)
        st.success(f'Prediction: {predicted_team}')




        total_matches, team1_wins, team2_wins = get_match_stats(team1, team2)

        # Plotting the graph
        fig, ax = plt.subplots()
        teams = [team1, team2]
        matches = [total_matches, total_matches]
        wins = [team1_wins, team2_wins]
        bar_width = 0.35
        index = range(len(teams))
        bar1 = ax.bar(index, matches, bar_width, label='Total Matches')
        bar2 = ax.bar([p + bar_width for p in index], wins, bar_width, label='Total Wins')
        ax.set_xlabel('Teams')
        ax.set_ylabel('Count')
        ax.set_title('Match Statistics')
        ax.set_xticks([p + 0.5 * bar_width for p in index])
        ax.set_xticklabels(teams)
        ax.legend()

        st.pyplot(fig)

        num_matches, team1_, team2_ = get_filtered_match_stats(ipl_df, team1, team2, toss_winner, toss_decision)

        fig1, ax = plt.subplots()
        teams = [team1, team2]
        matches = [num_matches, num_matches]
        wins = [team1_, team2_]
        bar_width = 0.35
        index = range(len(teams))
        bar1 = ax.bar(index, matches, bar_width, label=f'Total Matches {toss_winner} won toss and chose to {toss_decision}')
        bar2 = ax.bar([p + bar_width for p in index], wins, bar_width, label=f'Total Wins')
        ax.set_xlabel('Teams')
        ax.set_ylabel('Count')
        ax.set_title('Match Statistics')
        ax.set_xticks([p + 0.5 * bar_width for p in index])
        ax.set_xticklabels(teams)
        ax.legend()

        st.pyplot(fig1)



if __name__ == "__main__":
    app()
