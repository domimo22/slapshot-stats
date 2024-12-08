import logging
import boto3
import pandas as pd
import numpy as np
import pymysql
from io import StringIO
import json

s3 = boto3.client('s3')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Default log level is INFO, you can use DEBUG for more details

def lambda_handler(event, context):

    try:
        # Log the event object
        logger.info("Received event: %s", json.dumps(event))

        # Extract bucket name and object key from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        logger.info(f"Bucket: {bucket_name}, Key: {object_key}")

        # Retrieve the CSV object from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        csv_data = response['Body'].read().decode('utf-8')  # Decode the CSV data
        
        # Log the data retrieval
        logger.info(f"CSV data retrieved, length: {len(csv_data)} characters")
        
        # Load the CSV data into a Pandas DataFrame
        dataframe = pd.read_csv(StringIO(csv_data))
        dataframe = dataframe.replace({np.nan: None})  # Replace NaN with None

        # Log the DataFrame head
        logger.info(f"DataFrame loaded with {len(dataframe)} rows.")
        
    except Exception as e:
        logger.error(f"Error processing S3 event: {e}")
        raise e

    # Database connection setup
    try:
        connection = pymysql.connect(
            host="mysql-slapshot.cho60sekgih0.us-east-1.rds.amazonaws.com",
            user="admin",
            password="{PASSWORD}",
            database="slapshot"
        )
        logger.info("Database connection established.")
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        raise e

    # Database insertions
    try:
        column_mapping = {
            'Game_Id': 'game_id',
            'Date': 'date',
            'Period': 'which_period',
            'Event': 'event',
            'Description': 'description',
            'Time_Elapsed': 'time_elapsed',
            'Seconds_Elapsed': 'seconds_elapsed',
            'Strength': 'strength',
            'Ev_Zone': 'ev_zone',
            'Type': 'type',
            'Ev_Team': 'ev_team',
            'Home_Zone': 'home_zone',
            'Away_Team': 'away_team',
            'Home_Team': 'home_team',
            'p1_name': 'p1_name',
            'p1_ID': 'p1_id',
            'p2_name': 'p2_name',
            'p2_ID': 'p2_id',
            'p3_name': 'p3_name',
            'p3_ID': 'p3_id',
            'awayPlayer1': 'away_player1',
            'awayPlayer1_id': 'away_player1_id',
            'awayPlayer2': 'away_player2',
            'awayPlayer2_id': 'away_player2_id',
            'awayPlayer3': 'away_player3',
            'awayPlayer3_id': 'away_player3_id',
            'awayPlayer4': 'away_player4',
            'awayPlayer4_id': 'away_player4_id',
            'awayPlayer5': 'away_player5',
            'awayPlayer5_id': 'away_player5_id',
            'awayPlayer6': 'away_player6',
            'awayPlayer6_id': 'away_player6_id',
            'homePlayer1': 'home_player1',
            'homePlayer1_id': 'home_player1_id',
            'homePlayer2': 'home_player2',
            'homePlayer2_id': 'home_player2_id',
            'homePlayer3': 'home_player3',
            'homePlayer3_id': 'home_player3_id',
            'homePlayer4': 'home_player4',
            'homePlayer4_id': 'home_player4_id',
            'homePlayer5': 'home_player5',
            'homePlayer5_id': 'home_player5_id',
            'homePlayer6': 'home_player6',
            'homePlayer6_id': 'home_player6_id',
            'Away_Players': 'away_players',
            'Home_Players': 'home_players',
            'Away_Score': 'away_score',
            'Home_Score': 'home_score',
            'Away_Goalie': 'away_goalie',
            'Away_Goalie_Id': 'away_goalie_id',
            'Home_Goalie': 'home_goalie',
            'Home_Goalie_Id': 'home_goalie_id',
            'xC': 'xc',
            'yC': 'yc',
            'Home_Coach': 'home_coach',
            'Away_Coach': 'away_coach',
        }

        dataframe.rename(columns=column_mapping, inplace=True)

        insert_query = """
        INSERT INTO Plays (game_id, date, which_period, event, description, time_elapsed, seconds_elapsed,
                   strength, ev_zone, type, ev_team, home_zone, away_team, home_team, p1_name, p1_id,
                   p2_name, p2_id, p3_name, p3_id, away_player1, away_player1_id, away_player2, away_player2_id,
                   away_player3, away_player3_id, away_player4, away_player4_id, away_player5, away_player5_id,
                   away_player6, away_player6_id, home_player1, home_player1_id, home_player2, home_player2_id,
                   home_player3, home_player3_id, home_player4, home_player4_id, home_player5, home_player5_id,
                   home_player6, home_player6_id, away_players, home_players, away_score, home_score,
                   away_goalie, away_goalie_id, home_goalie, home_goalie_id, xc, yc, home_coach, away_coach)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor = connection.cursor()
        logger.info(f"Inserting {len(dataframe)} rows into the database.")
        for _, row in dataframe.iterrows():
            try:
                cursor.execute(insert_query, tuple(row))
            except Exception as e:
                logger.error(f"Error inserting row: {tuple(row)}")
                logger.error(e)
                break

        connection.commit()
        logger.info("Data inserted successfully.")
    except Exception as e:
        logger.error(f"Error during database operation: {e}")
    finally:
        cursor.close()
        connection.close()
        logger.info("Database connection closed.")
