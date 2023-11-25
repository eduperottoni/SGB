from flask import request, render_template, redirect
import logging
from db_utils.utils import execute_query

def get_rented_books():
    query = """
    SELECT Livro.titulo AS livro, Cliente.nome AS cliente, Historico.data_aluguel AS data
    FROM Livro 
    JOIN Historico ON Livro.ID = Historico.livro 
    JOIN Cliente ON Historico.cliente = Cliente.cpf 
    WHERE Historico.data_devolucao IS NULL
    """
    tuples = execute_query(query)
    keys_to_consider = ['livro', 'cliente', 'data']
    return render_template('special_queries_response.html', 
                        response_list=tuples, 
                        keys_to_consider=keys_to_consider,
                        title="Livros não devolvidos")