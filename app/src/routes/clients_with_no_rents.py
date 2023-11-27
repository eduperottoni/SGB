from flask import request, render_template, redirect
import logging
from db_utils.utils import execute_query

def get_clients_with_0_rents():
    query = """
    SELECT Cliente.nome AS cliente, Cliente.data_registro AS data_registro
    FROM Cliente 
    LEFT JOIN Historico ON Cliente.cpf = Historico.cliente 
    WHERE Historico.cliente IS NULL 
    GROUP BY Cliente.nome, Cliente.data_registro
    """
    tuples = execute_query(query)
    logging.debug(tuples)
    keys_to_consider=['cliente', 'data_registro']
    return render_template('special_queries_response.html', 
                           response_list=tuples, 
                           keys_to_consider=keys_to_consider,
                           title="Clientes sem aluguel")