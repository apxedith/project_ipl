import streamlit as st
import streamlit_shadcn_ui as ui
from streamlit_option_menu import option_menu
from winner_prediction import app as winner_prediction_app
from team_stats import app as team_statistics_app
from player_stats import app as player_statistics_app
from score_prediction import app as score_prediction_app
from custom_team import app as custom_team



st.set_page_config(
    page_title="Indian Premier League"
)

class MultiApp:
    def __init__(self) :
        self.apps=[]
    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })
    def run(self):
        with st.sidebar:        
            app = option_menu(
                menu_title='Main Menu',
                options=['Winner Prediction','Team Statistics','Player Statistics','Score Prediction','Custom Line Up'],
                menu_icon='null',
                default_index=0,
            )

        for item in self.apps:
            if item['title'] == app:
                item['function']()

# Create an instance of MultiApp
app = MultiApp()

# Add each page to the MultiApp instance
app.add_app("Winner Prediction", winner_prediction_app)
app.add_app("Team Statistics", team_statistics_app)
app.add_app("Player Statistics", player_statistics_app)
app.add_app("Score Prediction", score_prediction_app)
app.add_app("Custom Line Up", custom_team)

# Run the MultiApp
app.run()
