import psycopg2
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

def get_postgres_connection():
    """Create and return a PostgreSQL database connection."""
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        return connection
    except psycopg2.Error as e:
        print(f"Unable to connect to the database due to: {e}")
        return None

def ask_postgres_database(query):
    """Execute a SQL query on the PostgreSQL database and return the results."""
    connection = get_postgres_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            return None
    else:
        return None

def get_database_schema_dict():
    """Retrieve the database schema as a dictionary with schema, tables, and columns."""
    schema_dict = {}
    query = """
    SELECT table_schema, table_name, column_name
    FROM information_schema.columns
    WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
    ORDER BY table_schema, table_name, ordinal_position;
    """
    results = ask_postgres_database(query)
    if results:
        for schema, table, column in results:
            if schema not in schema_dict:
                schema_dict[schema] = {}
            if table not in schema_dict[schema]:
                schema_dict[schema][table] = []
            schema_dict[schema][table].append(column)
    return schema_dict

def get_database_schema_string():
    """Retrieve the database schema as a JSON-formatted string."""
    schema_dict = get_database_schema_dict()
    return json.dumps(schema_dict, indent=4)

# Create the database schema dictionary and string
database_schema_dict = get_database_schema_dict()
database_schema_string = get_database_schema_string()

# Test connection and schema retrieval
if __name__ == "__main__":
    connection = get_postgres_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("Connected to PostgreSQL database:", db_version)
        cursor.close()
        connection.close()
    
    schema_dict = get_database_schema_dict()
    print("Database schema:", json.dumps(schema_dict, indent=4))
    
    schema_string = get_database_schema_string()
    print("Database schema string:", schema_string)
