import streamlit as st
import pymysql
import tempfile
from boto3_utils import upload_file
import os

st.title("Player Stats")

# connection = pymysql.connect(
#     host="mysql-slapshot.cho60sekgih0.us-east-1.rds.amazonaws.com",
#     user="admin",
#     password="BiggestDS4300Fan",
#     database="slapshot"
# )

#data and id upload
uploaded_file = st.file_uploader("Upload your player data here.", type="csv")
player_id = st.text_input("Player Name")

#if game data and id has been uploaded
if (uploaded_file is not None) and (player_id is not None):
    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())  # Save file content
        temp_file_path = tmp_file.name

    upload_file(temp_file_path, "hockeyplayersraw")

    os.remove(temp_file_path)
    # with connection.cursor() as cursor:
    #     sql_query = "SELECT * FROM Plays"
    #     cursor.execute(sql_query)
    #     results = cursor.fetchall()
    #     for row in results:
    #         print(row)
