import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_URL = os.getenv("DB_URL")