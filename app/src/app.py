from flask import Flask, render_template, request
from config import create_tables, populate_tables
# from flask_sqlalchemy import SQLAlchemy
from db_utils.db import execute_query
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)s: %(message)s')

app = Flask(
    __name__,
    template_folder='static')


@app.route('/')
def hello():
    query = "SELECT * FROM Autor WHERE nome = 'Agatha Christie';"
    tuples = execute_query(query)
    logging.debug(tuples)
    return 'Hello, World!'

@app.route('/book-by-author/', methods=['GET', 'POST'])
def get_book_by_author(author_name = None):
    if request.method == 'POST':
        author_name = request.form.get('author_name')
        
        if author_name:
            query =f"SELECT Livro.titulo FROM Autor JOIN Escrito_por ON Autor.id = Escrito_por.autor JOIN Livro ON Escrito_por.livro = Livro.id WHERE Autor.nome = '{author_name}'"
            tuples = execute_query(query)
            logging.debug(tuples)
            logging.debug('pesquisa feita')
            return render_template('list.html', liste=tuples)

    return render_template('busca_por_autor.html')
    # query = f'SELECT * FROM Livro WHERE id = (SELECT a.id FROM Autor WHERE a.name = "{author_name}")'
    # query = f'SELECT * FROM Livro WHERE id IN (SELECT livro FROM escrito_por WHERE autor IN (SELECT id FROM Autor WHERE nome = {author_name}))'
        

if __name__ == '__main__':
    create_tables()
    populate_tables()
    app.run(host='0.0.0.0',port=8080)