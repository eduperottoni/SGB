from flask import request, render_template
import logging
from db_utils.db import execute_query

def get_clients_with_0_rents():
    query = """
    SELECT Cliente.nome AS cliente, COUNT(Historico.cliente) AS num_alugueis 
    FROM Cliente 
    LEFT JOIN Historico ON Cliente.cpf = Historico.cliente 
    WHERE Historico.cliente IS NULL 
    GROUP BY Cliente.nome
    """
    tuples = execute_query(query)
    logging.debug(tuples)
    keys_to_consider=['cliente']
    return render_template('special_queries_response.html', 
                           response_list=tuples, 
                           keys_to_consider=keys_to_consider,
                           title="Clientes sem aluguel")