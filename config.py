import os
from dotenv import load_dotenv

load_dotenv()  # this reads the .env file

TOKEN = os.getenv("BOT_TOKEN")
API_URL = "https://remotive.com/api/remote-jobs?search=devops"
PORT = int(os.getenv("PORT", "8000"))
