import streamlit as st
import numpy as np
import joblib
import matplotlib.pyplot as plt

# Function to map team names to prediction arrays
def map_team_to_array(team):
    teams = ['Chennai Super Kings', 'Delhi Capitals', 'Punjab Kings', 
             'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 
             'Royal Challengers Bangalore', 'Sunrisers Hyderabad']
    return [int(team == t) for t in teams]

def app():
    model = joblib.load('assets\model_score_predict.pkl')
    st.markdown("<h1 style='text-align: center;'> IPL Score Predictor </h1>", unsafe_allow_html=True)

    batting_team = st.selectbox('Select the Batting Team', ('Chennai Super Kings', 'Delhi Capitals', 'Punjab Kings', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad'),index=None)

    prediction_array = map_team_to_array(batting_team)

    bowling_team = st.selectbox('Select the Bowling Team', ('Chennai Super Kings', 'Delhi Capitals', 'Punjab Kings', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad'),index=None)
    
    if bowling_team == batting_team:
        st.error('Bowling and Batting teams should be different')
        return

    prediction_array += map_team_to_array(bowling_team)

    col1, col2 = st.columns(2)

    with col1:
        over = st.number_input('Enter Current Over', min_value=5, max_value=19, step=1, format='%i')
        if over % 1 != 0:
            st.error('Please enter a valid over (an integer value)')

    with col2:
        runs = st.number_input('Enter Current Runs', min_value=0, max_value=354, step=1, format='%i')

    wickets = st.slider('Enter Wickets fallen till now', 0, 9)

    prediction_array += [over, runs, wickets]

    prediction_array = np.array([prediction_array])
    pred = model.predict(prediction_array)
    rounded_pred = np.round(pred).astype(int)
    score = np.array(rounded_pred).flatten()

    if st.button('Predict Score'):
        st.success(f'PREDICTED MATCH SCORE: {score[5]}')

        # Plotting the graph
        predicted_runs = score[:6]
        overs = np.arange(15, 21)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(overs, predicted_runs, marker='o', linestyle='-', color='b')
        ax.set_xlabel("Over")
        ax.set_ylabel("Runs")
        ax.set_title("Predicted Runs vs Overs")
        ax.set_xticks(overs)
        ax.grid(True)

        st.pyplot(fig)

if __name__ == "__main__":
    app()
