from flask import request, render_template
import logging
from db_utils.db import execute_query

def get_top_5_clients():
    query = """
    SELECT Cliente.nome AS Cliente,
    COUNT(Historico.livro) AS num_alugueis 
    FROM Cliente LEFT JOIN Historico ON Cliente.cpf = Historico.cliente 
    GROUP BY Cliente.nome ORDER BY num_alugueis DESC LIMIT 5
    """
    tuples = execute_query(query)
    logging.debug(tuples)
    keys_to_consider=['cliente', 'num_alugueis']
    return render_template('special_queries_response.html', 
                           response_list=tuples, 
                           keys_to_consider=keys_to_consider,
                           title="Maiores clientes")