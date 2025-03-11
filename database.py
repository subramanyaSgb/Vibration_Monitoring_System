import psycopg2
from psycopg2 import sql
from datetime import datetime
from logging_config import logger
import os
import traceback

# Database configuration
DB_NAME = "deevia_vms"
TABLE_NAME = "vms"
COLUMN_NAME = "vibration_stopped_date_time"
DB_USER = "postgres"    # Replace with your PostgreSQL username
DB_PASSWORD = "root"  # Replace with your PostgreSQL password
DB_HOST = "localhost"  # Adjust if your PostgreSQL is hosted elsewhere
DB_PORT = "5432"  # Default PostgreSQL port

# Function to create the database if it does not exist
def create_db_if_not_exists():
    try:
        # Connect to PostgreSQL server (not the actual DB)
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if the database exists, if not, create it
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        if cursor.fetchone() is None:
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            logger.info(f"Database '{DB_NAME}' created.")
        else:
            logger.info(f"Database '{DB_NAME}' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        logger.error(traceback.format_exc())

# Function to create table if it does not exist
def create_table_if_not_exists():
    try:
        # Connect to the actual database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Create the table if it does not exist
        create_table_query = sql.SQL(""" 
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                {} TEXT
            );
        """).format(sql.Identifier(TABLE_NAME), sql.Identifier(COLUMN_NAME))

        cursor.execute(create_table_query)
        conn.commit()
        logger.info(f"Table '{TABLE_NAME}' is ready.")
        print(f"Table '{TABLE_NAME}' is ready.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        logger.error(traceback.format_exc())

# Function to store the current time into the database
def store_vibration_stopped_time():
    try:
        # Get the current time in string format
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Insert the current time into the table
        insert_query = sql.SQL(""" 
            INSERT INTO {} ({})
            VALUES (%s);
        """).format(sql.Identifier(TABLE_NAME), sql.Identifier(COLUMN_NAME))

        cursor.execute(insert_query, (current_time,))
        conn.commit()
        logger.info(f"Vibration stopped time '{current_time}' stored in the database.")
        print(f"Vibration stopped time '{current_time}' stored in the database.")

        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error storing time: {e}")
        logger.error(traceback.format_exc())

# Main function to set up the database and store time
if __name__ == "__main__":
    try:
        # Create DB if it does not exist
        create_db_if_not_exists()

        # Create Table if it does not exist
        create_table_if_not_exists()

        # Call the function to store the current time
        store_vibration_stopped_time()
    
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        logger.error(traceback.format_exc())
