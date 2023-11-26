from flask import request, render_template, redirect
import logging
from db_utils.utils import execute_query

def rent_history_view():
    query = """
    SELECT Livro.titulo AS titulo,
    Cliente.nome AS cliente,
    Historico.data_aluguel, Historico.data_devolucao, Historico.valor_pago
    FROM Historico 
    JOIN Livro ON Livro.ID = Historico.livro 
    JOIN Cliente ON Historico.cliente = Cliente.cpf
    ORDER BY data_aluguel
    """
    tuples = execute_query(query)
    logging.debug(tuples)
    keys_to_consider = ['titulo', 'cliente', 'data_aluguel', 'data_devolucao', 'valor_pago']
    return render_template('special_queries_response.html', 
            response_list=tuples, 
            keys_to_consider=keys_to_consider,
            title="Histórico")