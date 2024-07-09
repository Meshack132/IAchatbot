from utils.database_functions import database_schema_string

functions = [
    {
        "name": "ask_postgres_database",
        "description": "Executes a SQL query on the PostgreSQL database and returns the results.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query to execute."
                }
            },
            "required": ["query"]
        }
    }
]
