import logging
from db_utils.db import execute_query

def get_registers_in_table(table_name: str, **extra_specification) -> 'list[RealDictRow]':
    """
    Gets the registers in the specified table and with the specified constraints

    :param table name: name of the table
    :param extra_specification: kwargs specifying rules (column_name = value)
    """
    query = 'SELECT * FROM ' + table_name
    extra_str = ''
    params = None
    if extra_specification:
        extra_str += ' WHERE '
        extra_list = [f'{column_name} = %s' for column_name in extra_specification]
        extra_str += " AND ".join(extra_list)
        params = tuple([value for value in extra_specification.values()])

    logging.debug(extra_str)
    logging.debug(params)
    logging.debug(query + extra_str)

    tuples = execute_query(query + extra_str, params)
    logging.debug(tuples)

    return tuples