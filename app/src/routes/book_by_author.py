from flask import request, render_template
import logging
from db_utils.db import execute_query

def get_book_by_author(author_name = None):
    if request.method == 'POST':
        author_name = request.form.get('author_name')
        
        if author_name:
            query =f"SELECT Livro.titulo FROM Autor JOIN Escrito_por ON Autor.id = Escrito_por.autor JOIN Livro ON Escrito_por.livro = Livro.id WHERE Autor.nome = '{author_name}'"
            tuples = execute_query(query)
            logging.debug(tuples)
            logging.debug('pesquisa feita')
            return render_template('books_list.html', liste=tuples)

    return render_template('busca_por_autor.html')