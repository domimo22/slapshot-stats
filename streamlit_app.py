import streamlit as st

home_page = st.Page("./pages/Home.py", title="Home", icon="🥅")
players_page = st.Page("./pages/Players.py", title="Players", icon="🏒")
games_page = st.Page("./pages/Games.py", title="Games", icon="🏆")
teams_page = st.Page("./pages/Teams.py", title="Teams", icon="🧑‍🧑‍🧒‍🧒")

pg = st.navigation(
        {
            "Home": [home_page],
            "Quick Stats": [players_page, games_page, teams_page],
        }
    )

pg.run()