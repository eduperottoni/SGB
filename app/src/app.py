from flask import Flask, render_template, request, redirect
from config import create_tables, populate_tables
# from flask_sqlalchemy import SQLAlchemy
from db_utils.db import execute_query
from app_utils import get_registers_in_table
from routes import book, author, client, genre, publisher, clients_with_no_rents, rented_books, top_5_clients, book_by_author


from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)s: %(message)s')

app = Flask(
    __name__,
    template_folder='static')


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/clients-with-0-rents/', methods=['GET', 'POST'])
def get_clients_with_0_rents():
    return clients_with_no_rents.get_clients_with_0_rents()

@app.route('/rented-books/', methods=['GET', 'POST'])
def get_rented_books():
    return rented_books.get_rented_books()

@app.route('/top-5-clients/', methods=['GET', 'POST'])
def get_top_5_clients():
    return top_5_clients.get_top_5_clients()

@app.route('/book-by-author/', methods=['GET', 'POST'])
def get_book_by_author(author_name = None):
    return book_by_author.get_book_by_author()

@app.route('/books-crud/', methods=['GET', 'POST'])
def books_crud():
    return book.books_crud()

@app.route('/clients-crud/', methods=['GET', 'POST'])
def clients_crud():
    return client.clients_crud()

@app.route('/authors-crud/', methods=['GET', 'POST'])
def authors_crud():
    return author.authors_crud()

@app.route('/publishers-crud/', methods=['GET', 'POST'])
def publishers_crud():
    return publisher.publishers_crud()

@app.route('/genres-crud/', methods=['GET', 'POST'])
def genres_crud():
    return genre.genres_crud()


@app.route('/book-by-author/', methods=['GET', 'POST'])
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
    # query = f'SELECT * FROM Livro WHERE id = (SELECT a.id FROM Autor WHERE a.name = "{author_name}")'
    # query = f'SELECT * FROM Livro WHERE id IN (SELECT livro FROM escrito_por WHERE autor IN (SELECT id FROM Autor WHERE nome = {author_name}))'
        

if __name__ == '__main__':
    create_tables()
    populate_tables()
    app.run(host='0.0.0.0',port=8080)