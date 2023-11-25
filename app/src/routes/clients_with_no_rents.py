from flask import request, render_template
import logging
from db_utils.db import execute_query

def get_clients_with_0_rents():
    query = "SELECT Cliente.nome AS Cliente, COUNT(Historico.cliente) AS NumAlugueis FROM Cliente LEFT JOIN Historico ON Cliente.cpf = Historico.cliente WHERE Historico.cliente IS NULL GROUP BY Cliente.nome"
    tuples = execute_query(query)
    logging.debug(tuples)
    return render_template('clients_with_0_rents.html', liste=tuples)