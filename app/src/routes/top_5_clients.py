from flask import request, render_template
import logging
from db_utils.db import execute_query

def get_top_5_clients():
    query = "SELECT Cliente.nome AS Cliente, COUNT(Historico.livro) AS NumAlugueis FROM Cliente LEFT JOIN Historico ON Cliente.cpf = Historico.cliente GROUP BY Cliente.nome ORDER BY NumAlugueis DESC LIMIT 5"
    tuples = execute_query(query)
    logging.debug(tuples)
    return render_template('top_5_clients.html', liste=tuples)