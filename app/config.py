# app/config.py
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Settings:
    ELASTICSEARCH_HOST = "http://elasticsearch:9200"
    ELASTICSEARCH_INDEX = "products"
    ELASTICSEARCH_TIMEOUT = 30

    SECRET_KEY = os.getenv("SECRET_KEY", "DbSLoIREJtu6z3CVnpTd_DdFeMMRoteCU0UjJcNreZI")
    PROJECT_NAME: str = "Search Service"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Sylvian@db:5433/search_service_db")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "Sylvian")
    DATABASE_DB: str = os.getenv("DATABASE_DB", "search_service_db")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "5433"))

settings = Settings()