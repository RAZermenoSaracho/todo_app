import psycopg2
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def ensure_database_exists(config):
    # Conectarse primero a una base existente como 'postgres'
    conn = psycopg2.connect(
        dbname='postgres',
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        host=config["DB_HOST"],
        port=config["DB_PORT"]
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (config["DB_NAME"],))
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {config['DB_NAME']};")
    conn.close()

def get_connection():
    config = load_config()
    ensure_database_exists(config)
    return psycopg2.connect(
        dbname=config["DB_NAME"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        host=config["DB_HOST"],
        port=config["DB_PORT"]
    )
