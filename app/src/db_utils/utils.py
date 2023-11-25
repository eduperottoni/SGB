from psycopg2.extensions import connection, cursor 
from psycopg2.extras import RealDictCursor
from psycopg2 import connect, ProgrammingError
import os, logging

def connect_to_database() -> connection:
    """
    Function to create database connection to make 

    :return: 
    """
    return connect(host=os.environ.get('POSTGRES_HOST'),
                   port=int(os.environ.get('POSTGRES_PORT')),
                   database=os.environ.get('POSTGRES_DB_NAME'),
                   user=os.environ.get('POSTGRES_USER'),
                   password=os.environ.get('POSTGRES_PASSWORD'))


def connect_and_execute_sql(filepath: str):
    with connect_to_database() as conn:
        with conn.cursor() as cursor:
            with open(filepath, 'r') as file:
                cursor.execute(file.read())
        conn.commit()


def execute_query(query: str, params: tuple[str | int] = None):
    with connect_to_database() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            try:
                rows = cursor.fetchall()
                return rows if rows else None
            except ProgrammingError:
                logging.warning("PROGRAMMING ERROR")

