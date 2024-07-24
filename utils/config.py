from dotenv import load_dotenv
import os

db_credentials = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

# Other configurations
MAX_TOKENS_ALLOWED = 1000
MAX_MESSAGES_TO_OPENAI = 10
TOKEN_BUFFER = 100  # Add this line

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AI_MODEL = 'gpt-4'  # or whichever model you're using
