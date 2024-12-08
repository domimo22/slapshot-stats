<strong>Slapshot Stats</strong>

<strong>Slapshot Stats</strong> <br>
An application that allows users to upload csv hockey data and visualize statistics in real time.

Demo: https://drive.google.com/file/d/1HYKU392WcSrUzj8tdezRvvNpXYSHoMhM/view?usp=sharing 

<strong>Data Overview</strong> <br>
Three datasets from Kaggle were used, one for each of players, games, and teams. <br>
**Players dataset:** Compiled csv NHL draft data from 1963-2022 from user mattop on Kaggle. Includes the player’s name, the team the player was drafted to, the player’s nationality, position, and age, as well as career statistics like goals and assists. <br>
**Teams dataset:** Stanley Cup team performance data by user mattop on Kaggle. Includes data from 1918-2022 with team names, ranking, year, and performance stats like wins, goals scored, shootout wins, etc.<br>
**Games dataset:** 2007 NHL play-by-play data for the entire season from user 903124 on Kaggle. Compilation of every in-game event from the 2007 season organized by game_id. Game events include hits, penalties, goals, assists, missed shots with location and timing data.<br>

Total size of datasets: 3.98GB

Pipeline Overview
- **User Interface (Streamlit App Hosted on EC2)** <br>
Basic Streamlit application that provides a user-friendly interface for uploading CSV files containing hockey data.
Contains players, games, and teams tabs which allow users to upload data in csv form, query for certain uploads, and see visual stat representations.
Handles initial transfer of files to S3.
- **Data Ingestion (S3)** <br>
Includes 3 buckets, one for each of the statistical categories.
The upload event triggers a lambda function for processing.
- **Serverless Processing (Lambda)** <br>
The Lambda function extracts the csv file from the S3 bucket, transforms the data, and processes the data.
Handles column renaming, data cleaning such as removing null rows, and uploading the cleaned data to an RDS instance.
- **Data Storage (RDS)** <br>
The processed data is stored in a MySQL instance. The database includes 3 tables, for each of players, teams, and plays (individual game events in a game).

**AWS Services:** S3, RDS, Lambda, CloudWatch, EC2, IAM <br>
**Libraries:** boto3, PyMySQL, Streamlit <br>
**Other Tools:** AWS CLI, MySQL, Python <br>

![Blank diagram (2)](https://github.com/user-attachments/assets/13eb3797-a4d6-4d82-b002-1c08a7e1922e)

