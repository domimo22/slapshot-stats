import streamlit as st
import pymysql

st.title("Player Stats")

connection = pymysql.connect(
    host="mysql-slapshot.cho60sekgih0.us-east-1.rds.amazonaws.com",
    user="admin",
    password="BiggestDS4300Fan",
    database="slapshot"
)

#data and id upload
uploaded_file = st.file_uploader("Upload your game data here.", type="csv")
game_id = st.text_input("Game ID")

#if game data and id has been uploaded
# if (uploaded_file is not None) and (game_id is not None):
