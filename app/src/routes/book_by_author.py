from flask import request, render_template, redirect
import logging
from db_utils.utils import execute_query

def get_book_by_author(author_name = None):
    if request.method == 'POST':
        author_name = request.form.get('author_name')
        
        if author_name:
            query = """
            SELECT Livro.titulo 
            FROM Autor 
            JOIN Escrito_por ON Autor.id = Escrito_por.autor 
            JOIN Livro ON Escrito_por.livro = Livro.id 
            WHERE Autor.nome = %s
            """
            params = (author_name, )
            tuples = execute_query(query, params)
            keys_to_consider = ['titulo']
            return render_template('special_queries_response.html', 
                    response_list=tuples, 
                    keys_to_consider=keys_to_consider,
                    title=f"Livros de {author_name}")

    return render_template('search_book_by_author.html')