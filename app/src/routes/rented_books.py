from flask import request, render_template
import logging
from db_utils.db import execute_query

def get_rented_books():
    query = "SELECT Livro.titulo AS Livro, Cliente.nome AS Cliente, Historico.data_aluguel AS Historico FROM Livro JOIN Historico ON Livro.ID = Historico.livro JOIN Cliente ON Historico.cliente = Cliente.cpf WHERE Historico.data_devolucao IS NULL"
    tuples = execute_query(query)
    logging.debug(tuples)
    return render_template('rented_books.html', liste=tuples)