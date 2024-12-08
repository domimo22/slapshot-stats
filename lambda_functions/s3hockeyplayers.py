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
            'id': 'player_id',
            'year': 'year',
            'overall_pick': 'overall_pick',
            'team': 'team',
            'player': 'player_name',
            'nationality': 'nationality',
            'position': 'position',
            'age': 'age',
            'to_year': 'to_year',
            'amateur_team': 'amateur_team',
            'games_played': 'games_played',
            'goals': 'goals',
            'assists': 'assists',
            'points': 'points',
            'plus_minus': 'plus_minus',
            'penalties_minutes': 'penalty_minutes',
            'goalie_games_played': 'goalie_games_played',
            'goalie_wins': 'goalie_wins',
            'goalie_losses': 'goalie_losses',
            'goalie_ties_overtime': 'goalie_ties_overtime',
            'save_percentage': 'save_percentage',
            'goals_against_average': 'goals_against_average',
            'point_shares': 'point_shares'
        }

        dataframe.rename(columns=column_mapping, inplace=True)

        insert_query = """
        INSERT INTO Players (player_id, year, overall_pick, team, player_name, nationality, position, age, to_year, amateur_team,
                    games_played, goals, assists, points, plus_minus, penalty_minutes, goalie_games_played, goalie_wins,
                    goalie_losses, goalie_ties_overtime, save_percentage, goals_against_average, point_shares)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
