import streamlit as st
import pymysql
import tempfile
from boto3_utils import upload_file
import os
import pandas as pd

st.title("Team Stats")

connection = pymysql.connect(
    host="mysql-slapshot.cho60sekgih0.us-east-1.rds.amazonaws.com",
    user="admin",
    password="BiggestDS4300Fan",
    database="slapshot"
)

#data and id upload
uploaded_file = st.file_uploader("Upload your team data here.", type="csv")
team_id = st.text_input("Team Name")

#if game data and id has been uploaded
if (team_id is not None):

    if (uploaded_file is not None):
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())  # Save file content
            temp_file_path = tmp_file.name
        upload_file(temp_file_path, "hockeyteamsraw")
        os.remove(temp_file_path)
    
    with connection.cursor() as cursor:
        sql_query = """
            SELECT 
                ranking, team_name, year, games, wins, losses, ties, win_loss_percentage, 
                goals_scored, goals_against, goal_differential 
            FROM 
                Teams 
            WHERE 
                team_name = %s
            LIMIT 10
        """ 
        cursor.execute(sql_query, (team_id,))
        teams_data = cursor.fetchall()

    if teams_data:
        # Convert to DataFrame and add column names
        df_teams = pd.DataFrame(teams_data)
        df_teams.columns = [
            "Rank", "Team", "Year", "Games", "Wins", 
            "Losses", "Ties", "Win-Loss %", "Goals Scored", 
            "Goals Against", "Goal Differential"
        ]

        st.write("### Teams Data")
        st.dataframe(df_teams)
    else:
        st.write("No team data found.")