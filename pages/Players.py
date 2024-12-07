import streamlit as st
import pandas as pd
import pymysql
import tempfile
from boto3_utils import upload_file
import os

st.title("Player Stats")

connection = pymysql.connect(
    host="mysql-slapshot.cho60sekgih0.us-east-1.rds.amazonaws.com",
    user="admin",
    password="BiggestDS4300Fan",
    database="slapshot"
)

#data and id upload
uploaded_file = st.file_uploader("Upload your player data here.", type="csv")
player_id = st.text_input("Player Name")

#if game data and id has been uploaded
if (player_id is not None):

    if (uploaded_file is not None):
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())  # Save file content
            temp_file_path = tmp_file.name

        upload_file(temp_file_path, "hockeyplayersraw")
        os.remove(temp_file_path)
    
    sql_query = """
        SELECT 
            year, overall_pick, team, player_name, nationality, position, 
            age, games_played, goals, assists, points 
        FROM 
            Players 
        WHERE 
            player_name = %s
        LIMIT 10
    """

    with connection.cursor() as cursor:
        cursor.execute(sql_query, (player_id,))
        players_data = cursor.fetchall()

        if players_data:
            df_players = pd.DataFrame(players_data)
            df_players.columns = [
                "Draft Year", "Overall Pick", "Team", "Player", 
                "Nationality", "Position", "Age", "Games Played", 
                "Goals", "Assists", "Points"
            ]

            st.write("### Players Data")
            st.dataframe(df_players)
        else:
            st.write("No player data found.")
