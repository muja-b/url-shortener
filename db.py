import os
import psycopg2
from psycopg2 import pool

DATABASE_URL = os.environ.get("DATABASE_URL", "dbname=urlshortener user=postgres password=postgres host=localhost")

connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DATABASE_URL
)

def get_connection():
    return connection_pool.getconn()

def put_connection(conn):
    connection_pool.putconn(conn)
