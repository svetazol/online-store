import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True

BASE_URL = "http://127.0.0.1:8080"
STATIC_URL = f'{BASE_URL}/static/'
STATIC_DIR = os.path.join(os.path.dirname(__file__), '../../frontend/dist/')
