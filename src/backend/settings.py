import os

DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@127.0.0.1:{DB_PORT}/{DB_NAME}"

DEBUG = True

BASE_URL = "http://127.0.0.1:8080"
STATIC_URL = f'{BASE_URL}/static/'
STATIC_DIR = os.path.join(os.path.dirname(__file__), '../frontend/dist/')
