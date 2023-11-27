from flask import request, render_template, redirect
import logging
from db_utils.utils import execute_query

def ranking_books_by_money():
    query = """
    SELECT Livro.titulo AS livro,
    SUM(Historico.valor_pago) AS valor_total 
    FROM Livro
    LEFT JOIN Historico ON Livro.id = Historico.livro 
    GROUP BY Livro.id
    ORDER BY valor_total DESC
    """
    tuples = execute_query(query)
    logging.debug(tuples)
    keys_to_consider=['livro', 'valor_total']
    return render_template('special_queries_response.html', 
                           response_list=tuples, 
                           keys_to_consider=keys_to_consider,
                           title="Ranking de livros por rendimento",
                           ranking=True)