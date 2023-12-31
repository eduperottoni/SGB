from db_utils.utils import connect_and_execute_sql
import logging

def create_tables():
    """
    Function to create tables in the database
    """
    connect_and_execute_sql('db_utils/create_tables.sql')
    logging.debug('TABELAS CRIADAS')


def populate_tables():
    """
    Function to populate the database
    """
    connect_and_execute_sql('db_utils/populate_tables.sql')
    logging.debug('TABELAS POPULADAS') 