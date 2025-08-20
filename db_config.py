import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "weather_app_db",
    "user": "postgres",
    "password": "1234",
    "port": "5432"
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)
