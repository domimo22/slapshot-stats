import streamlit as st
import pymysql
from boto3_utils import upload_file
import tempfile
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

st.title("Game Stats")

connection = pymysql.connect(
    host="mysql-slapshot.cho60sekgih0.us-east-1.rds.amazonaws.com",
    user="admin",
    password="{PASSWORD}",
    database="slapshot"
)

#data and id upload
uploaded_file = st.file_uploader("Upload your game data here.", type="csv")
game_id = st.text_input("Game ID")

#if game data and id has been uploaded
if (game_id is not None):

    st.subheader("Game Breakdown")

    if (uploaded_file is not None):
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())  # Save file content
            temp_file_path = tmp_file.name

        upload_file(temp_file_path, "hockeygamesraw")
        os.remove(temp_file_path)

    with connection.cursor() as cursor:
        sql_query = """
            SELECT 
                home_team, away_team, 
                SUM(CASE WHEN event = 'GOAL' AND ev_team = home_team THEN 1 ELSE 0 END) AS Home_Goals,
                SUM(CASE WHEN event = 'GOAL' AND ev_team = away_team THEN 1 ELSE 0 END) AS Away_Goals,
                SUM(CASE WHEN event = 'HIT' AND ev_team = home_team THEN 1 ELSE 0 END) AS Home_Hits,
                SUM(CASE WHEN event = 'HIT' AND ev_team = away_team THEN 1 ELSE 0 END) AS Away_Hits,
                SUM(CASE WHEN event = 'SHOT' AND ev_team = home_team THEN 1 ELSE 0 END) AS Home_Shots,
                SUM(CASE WHEN event = 'SHOT' AND ev_team = away_team THEN 1 ELSE 0 END) AS Home_Shots,
                SUM(CASE WHEN event = 'PENL' AND ev_team = home_team THEN 1 ELSE 0 END) AS Home_Penalties,
                SUM(CASE WHEN event = 'PENL' AND ev_team = away_team THEN 1 ELSE 0 END) AS Home_Penalties
            FROM 
                Plays
            WHERE 
                game_id = %s
            GROUP BY 
                home_team, away_team
        """
        cursor.execute(sql_query, (game_id,))
        results = cursor.fetchall()

        
    if results:
        for row in results:
            home_team = row[0]
            away_team = row[1]
            home_goals = row[2]
            away_goals = row[3]
            home_hits = row[4]
            away_hits = row[5]
            home_shots = row[6]
            away_shots = row[7]
            home_penalties = row[8]
            away_penalties = row[9]

            st.write(f"Game {game_id}: {home_team} vs {away_team}")
            st.write(f"Goals scored by {home_team}: {home_goals}")
            st.write(f"Goals scored by {away_team}: {away_goals}")
            st.write(f"Hits delivered by {home_team}: {home_hits}")
            st.write(f"Assists delivered by {away_team}: {away_hits}")
            st.write(f"Shots taken by {home_team}: {home_shots}")
            st.write(f"Shots taken by {away_team}: {away_shots}")
            st.write(f"Penalties committed by {home_team}: {home_penalties}")
            st.write(f"Penalties committed by {away_team}: {away_penalties}")
    else:
        st.write(f"No data found for Game ID {game_id}.")

    with connection.cursor() as cursor:
        sql_query = """
            SELECT 
                which_period,
                SUM(CASE WHEN event = 'GOAL' AND ev_Team = home_Team THEN 1 ELSE 0 END) AS Home_Goals,
                SUM(CASE WHEN event = 'GOAL' AND ev_Team = away_Team THEN 1 ELSE 0 END) AS Away_Goals,
                SUM(CASE WHEN event = 'SHOT' AND ev_Team = home_Team THEN 1 ELSE 0 END) AS Home_Shots,
                SUM(CASE WHEN event = 'SHOT' AND ev_Team = away_Team THEN 1 ELSE 0 END) AS Away_Shots
            FROM 
                Plays
            WHERE 
                game_id = %s
            GROUP BY 
                which_period
            ORDER BY 
                which_period
        """
        cursor.execute(sql_query, (game_id,))
        results = cursor.fetchall()

    if results:
        periods = []
        home_goals = []
        away_goals = []
        home_shots = []
        away_shots = []

        for row in results:
            periods.append(row[0])
            home_goals.append(row[1])
            away_goals.append(row[2])
            home_shots.append(row[3])
            away_shots.append(row[4])

        fig, ax = plt.subplots(2, 1, figsize=(10, 10))

        ax[0].plot(periods, home_goals, label="Home Goals", marker='o', color='blue')
        ax[0].plot(periods, away_goals, label="Away Goals", marker='o', color='red')
        ax[0].set_title("Goals per Period")
        ax[0].set_xlabel("Period")
        ax[0].set_ylabel("Goals")
        ax[0].legend()
        ax[0].set_xticks([1, 2, 3, 4])
        ax[0].yaxis.set_major_locator(MaxNLocator(integer=True))

        ax[1].plot(periods, home_shots, label="Home Shots", marker='o', color='blue')
        ax[1].plot(periods, away_shots, label="Away Shots", marker='o', color='red')
        ax[1].set_title("Shots per Period")
        ax[1].set_xlabel("Period")
        ax[1].set_ylabel("Shots")
        ax[1].legend()
        ax[1].set_xticks([1, 2, 3, 4])
        ax[1].yaxis.set_major_locator(MaxNLocator(integer=True))

        st.pyplot(fig)
            
