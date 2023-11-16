from flask import Flask, render_template, request, redirect
from config import create_tables, populate_tables
# from flask_sqlalchemy import SQLAlchemy
from db_utils.db import execute_query

from datetime import datetime
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

# @app.route('/clients-crud/', methods=['GET'])
# def show_clients_crud():
#     return render_template('clients_crud.html')

@app.route('/clients-crud/', methods=['GET', 'POST'])
@app.route('/clients-crud/<cpf>', methods=['GET', 'POST'])
def clients_crud(cpf = None):
    action = request.args.get('action')
    logging.debug(action)
    client_form = {}
    
    if request.method == 'POST':
        if action in ['insert', 'update']:
            client_form = request.form
            logging.debug(f'Vamos cadastrar/atualizar um cliente: {client_form["cpf"]}')

            if action == 'insert':
                query = f'INSERT INTO Cliente (cpf, nome, data_nascimento, data_registro) VALUES {client_form["cpf"], client_form["nome"], client_form["data_nascimento"], datetime.now().isoformat()}'
                execute_query(query)

            return redirect('/clients-crud/')

        elif action == 'read':
            cpf = request.form['cpf']
            query = f"SELECT * FROM Cliente WHERE cpf = '{cpf}'"
            tuples = execute_query(query)
            logging.debug(f'MOSTRAR TEMPLATE COM O CLIENTE: {tuples}')

        elif action == 'delete':
            ...
    
    if action == 'update':
        try:
            query = f"SELECT (cpf, nome, data_nascimento) FROM Cliente WHERE cpf = {cpf}"
            tuples = execute_query(query)
            logging.debug(f'Recuperamos dados do cliente: {tuples}')

        except Exception as e:
            logging.debug(e)

    elif action == 'insert':
        logging.debug('OLÁ')


        return render_template('client_form.html', client_form=client_form)
    
    return render_template('clients_crud.html')
    


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