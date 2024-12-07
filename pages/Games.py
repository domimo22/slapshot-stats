import streamlit as st
import pymysql
from boto3_utils import upload_file

st.title("Game Stats")

# connection = pymysql.connect(
#     host="mysql-slapshot.cho60sekgih0.us-east-1.rds.amazonaws.com",
#     user="admin",
#     password="BiggestDS4300Fan",
#     database="slapshot"
# )

#data and id upload
uploaded_file = st.file_uploader("Upload your game data here.", type="csv")
game_id = st.text_input("Game ID")

#if game data and id has been uploaded
if (uploaded_file is not None) and (game_id is not None):
    upload_file(uploaded_file, "hockeygamesraw")
    # with connection.cursor() as cursor:
    #     sql_query = "SELECT * FROM Plays"
    #     cursor.execute(sql_query)
    #     results = cursor.fetchall()
    #     for row in results:
    #         print(row)
