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
    query = "SELECT * FROM Autor WHERE nome = %s OR nome = %s;"
    params = ('Agatha Christie', 'Jane Austen')
    tuples = execute_query(query, params)
    logging.debug(tuples)
    return 'Hello, World!'

# @app.route('/clients-crud/', methods=['GET'])
# def show_clients_crud():
#     return render_template('clients_crud.html')

@app.route('/clients-crud/', methods=['GET', 'POST'])
def clients_crud():
    action = request.args.get('action')
    logging.debug(action)
    
    if request.method == 'POST':
        logging.debug('ISSO FOI UM POST')
        if action in ['create', 'update']:
            client_form = request.form
            logging.debug(f'Vamos cadastrar/atualizar um cliente: {client_form["cpf"]}')

            if action == 'create':
                query = f'INSERT INTO Cliente (cpf, nome, data_nascimento, data_registro) VALUES {client_form["cpf"], client_form["nome"], client_form["data_nascimento"], datetime.now().isoformat()}'
                execute_query(query) 
                
                logging.debug('Cliente criado')
                query = f"SELECT * FROM Cliente WHERE cpf = %s;"
                params = (client_form["cpf"],)
                logging.debug(execute_query(query, params))

            elif action == 'update':
                logging.debug('Vamos atualizar o cliente')
                logging.debug(client_form)

                query = """
                    UPDATE Cliente 
                    SET nome = %s, data_nascimento = %s
                    WHERE cpf = %s
                """
                values = (client_form['nome'], client_form['data_nascimento'], client_form['cpf'])
                execute_query(query, values)

                logging.debug('Cliente atualizado')
                query = f"SELECT * FROM Cliente WHERE cpf = %s;"
                params = (client_form["cpf"],)
                logging.debug(execute_query(query, params))

            elif action == 'delete':
                return render_template()

            return redirect('/clients-crud/')

        elif action == 'read':
            clients_info = request.form
            query = f'SELECT * FROM Cliente'
            query, params = format_search_by_params_query(query, clients_info)
            tuples = execute_query(query, params)
            logging.debug(f'MOSTRAREMOS OS RESULTADOS DA BUSCA POR CLIENTES: {tuples}')
            
            return render_template('clients.html', search=tuples)
        
        elif action == 'delete':
            logging.debug('CPF')
            logging.debug(request.form)
            logging.debug(request.form['cpf'])
            #TODO Ver se é possível deletar (se o cliente não tem empréstimos pendentes)
            query = f"DELETE FROM Cliente WHERE cpf = %s;"
            params = (request.form.get('cpf'),)
            execute_query(query, params)
            logging.debug('Cliente deletado')

            query = f'SELECT * FROM Cliente WHERE cpf = %s;'
            params = (request.form.get('cpf'),)
            tuples = execute_query(query, params)

    # If method == 'GET':
    if action:
        client_form={}
        form_title=''
        match action:
            case 'update':
                if 'cpf' in request.args:
                    # try:
                    cpf = request.args.get('cpf')
                    query = f"SELECT * FROM Cliente WHERE cpf = %s;"
                    params = (cpf,)
                    client_form = execute_query(query, params)[0]

                    form_title = 'Atualizar cliente'
                    # except Exception as e:
                    #     return render_template('error.html',
                    #                         msg="Erro ao recuperar o CPF especificado",
                    #                         url_for_link="clients_crud",
                    #                         action_link='update')
                else:
                    clients_list = get_all_registers_in_table('Cliente')
                    return render_template('choose_client.html', clients=clients_list)

            case 'create':
                form_title='Cadastrar cliente'

            case 'read':
                form_title = 'Buscar cliente'

            case 'delete':
                    clients_list = get_all_registers_in_table('Cliente')
                    return render_template('choose_client.html', clients=clients_list)

        
        return render_template('client_form.html',
                                client_form=client_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('clients_crud.html', crud_action=action)


def get_all_registers_in_table(table_name: str) -> 'list[RealDictRow]':
    query = 'SELECT * FROM ' + table_name
    # params = (table_name,)
    tuples = execute_query(query)

    return tuples

@app.route('/authors-crud/', methods=['GET', 'POST'])
def authors_crud():
    action = request.args.get('action')
    logging.debug(action)
    
    if request.method == 'POST':
        logging.debug('ISSO FOI UM POST')
        if action in ['create', 'update']:
            author_form = request.form
            logging.debug(f'Vamos cadastrar/atualizar um autor: {author_form["nome"]}')

            if action == 'create':
                query = f'INSERT INTO Autor (nome, biografia, data_nascimento) VALUES {author_form["nome"], author_form["biografia"], author_form["data_nascimento"]}'
                execute_query(query) 
                
                logging.debug('Autor criado')
                query = f"SELECT * FROM Autor WHERE nome = %s;"
                params = (author_form["nome"],)
                logging.debug(execute_query(query, params))

            elif action == 'update':
                logging.debug('Vamos atualizar o autor')
                logging.debug(author_form)

                query = """
                    UPDATE Autor 
                    SET biografia = %s, data_nascimento = %s
                    WHERE nome = %s
                """
                values = (author_form['biografia'], author_form['data_nascimento'], author_form['nome'])
                execute_query(query, values)

                logging.debug('Autor atualizado')
                query = f"SELECT * FROM Autor WHERE nome = %s;"
                params = (author_form["nome"],)
                logging.debug(execute_query(query, params))

            elif action == 'delete':
                return render_template()
                
            return redirect('/authors-crud/')

        elif action == 'read':
            authors_info = request.form
            query = f'SELECT * FROM Autor'
            query, params = format_search_by_params_query(query, authors_info)
            tuples = execute_query(query, params)
            logging.debug(f'MOSTRAREMOS OS RESULTADOS DA BUSCA POR CLIENTES: {tuples}')
            
            return render_template('authors.html', search=tuples)
        
        elif action == 'delete':
            logging.debug('Nome')
            logging.debug(request.form)
            logging.debug(request.form['nome'])
            #TODO Ver se é possível deletar (se o authore não tem empréstimos pendentes)
            query = f"DELETE FROM Autor WHERE nome = %s;"
            params = (request.form.get('nome'),)
            execute_query(query, params)
            logging.debug('Autor deletado')

            query = f'SELECT * FROM Autor WHERE nome = %s;'
            params = (request.form.get('nome'),)
            tuples = execute_query(query, params)
            

    # If method == 'GET':
    if action:
        author_form={}
        form_title=''
        match action:
            case 'update':
                if 'nome' in request.args:
                    # try:
                    nome = request.args.get('nome')
                    query = f"SELECT (nome, biografia, data_nascimento) FROM Autor WHERE nome = %s;"
                    params = (nome,)
                    tuple = execute_query(query, params)
                    authors_list = get_dicts_from_tuples(tuple, ['nome', 'biografia', 'data_nascimento'])
                    authors_list[0]['nome'] = authors_list[0]['nome'][1:-1]
                    author_form = authors_list[0]
                    form_title = 'Atualizar autor'
                    # except Exception as e:
                    #     return render_template('error.html',
                    #                         msg="Erro ao recuperar o CPF especificado",
                    #                         url_for_link="clients_crud",
                    #                         action_link='update')
                else:
                    authors_list = get_all_registers_in_table('Autor')
                    return render_template('choose_author.html', authors=authors_list)

            case 'create':
                form_title='Cadastrar autor'

            case 'read':
                form_title = 'Buscar autor'

            case 'delete':
                    authors_list = get_all_registers_in_table('Autor')
                    return render_template('choose_author.html', authors=authors_list)

        
        return render_template('author_form.html',
                                author_form=author_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('authors_crud.html', crud_action=action)


@app.route('/publishers-crud/', methods=['GET', 'POST'])
def publishers_crud():
    action = request.args.get('action')
    logging.debug(action)
    
    if request.method == 'POST':
        logging.debug('ISSO FOI UM POST')
        if action in ['create', 'update']:
            publishers_form = request.form
            logging.debug(f'Vamos cadastrar/atualizar uma editora: {publishers_form["nome"]}')

            if action == 'create':
                query = f'INSERT INTO Editora (nome, endereco, contato) VALUES {publishers_form["nome"], publishers_form["endereco"], publishers_form["contato"]}'
                execute_query(query) 
                
                logging.debug('Editora criada')
                query = f"SELECT * FROM Editora WHERE nome = %s;"
                params = (publishers_form["nome"],)
                logging.debug(execute_query(query, params))

            elif action == 'update':
                logging.debug('Vamos atualizar a editora')
                logging.debug(publishers_form)

                query = """
                    UPDATE Editora 
                    SET nome = %s, endereco = %s, contato = %s
                    WHERE id = %s
                """
                values = (publishers_form["nome"], publishers_form["endereco"], publishers_form["contato"], publishers_form['id'])
                execute_query(query, values)

                logging.debug('Editora atualizada')
                query = f"SELECT * FROM Editora WHERE nome = %s;"
                params = (publishers_form["nome"],)
                logging.debug(execute_query(query, params))

            elif action == 'delete':
                return render_template()
                
            return redirect('/publishers-crud/')

        elif action == 'read':
            publishers_info = request.form
            query = f'SELECT * FROM Editora'
            query, params = format_search_by_params_query(query, publishers_info)
            tuples = execute_query(query, params)
            logging.debug(f'MOSTRAREMOS OS RESULTADOS DA BUSCA POR EDITORA: {tuples}')
            
            return render_template('publishers.html', search=tuples)
        
        elif action == 'delete':
            logging.debug('CPF')
            logging.debug(request.form)
            logging.debug(request.form['nome'])
            #TODO Ver se é possível deletar (se o cliente não tem empréstimos pendentes)
            query = f"DELETE FROM Editora WHERE nome = %s;"
            params = (request.form.get('nome'),)
            execute_query(query, params)
            logging.debug('Edutira deletada')

            query = f'SELECT * FROM Editora WHERE nome = %s;'
            params = (request.form.get('nome'),)
            tuples = execute_query(query, params)

    # If method == 'GET':
    if action:
        publisher_form={}
        form_title=''
        match action:
            case 'update':
                if 'nome' in request.args:
                    # try:
                    nome = request.args.get('nome')
                    query = f"SELECT * FROM Editora WHERE nome = %s;"
                    params = (nome,)
                    publisher_form = execute_query(query, params)[0]

                    logging.debug('111111111111111111111111')
                    logging.debug(publisher_form)
                    # publishers_list = get_all_registers_in_table('Editora')
                    # publisher_form = publishers_list[0]
                    form_title = 'Atualizar editora'
                    # except Exception as e:
                    #     return render_template('error.html',
                    #                         msg="Erro ao recuperar o CPF especificado",
                    #                         url_for_link="clients_crud",
                    #                         action_link='update')
                else:
                    publishers_list = get_all_registers_in_table('Editora')
                    return render_template('choose_publisher.html', publishers=publishers_list)

            case 'create':
                form_title='Cadastrar editora'

            case 'read':
                form_title = 'Buscar editora'

            case 'delete':
                    publishers_list = get_all_registers_in_table('Editora')
                    return render_template('choose_publisher.html', publishers=publishers_list)

        
        return render_template('publisher_form.html',
                                publisher_form=publisher_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('publishers_crud.html', crud_action=action)


# def get_dicts_from_tuples(tuples: list[str], keys_list: list[str]) -> list[dict[str | str]]:
#     """
#     Function to transform a result from a db query to a dict based on the specified keys

#     :param tuples: tuples from DB
#     :param keys_list: list with keys, in the order of the tuples resultss
#     :return: the result dict
#     """
#     dicts_list = []
#     for tuple in tuples:
#         logging.debug(tuple)
#         for t in tuple:
#             t = t[1:-1]
#             dicts_list.append(
#                 {keys_list[index]: column for index, column in enumerate(t.split(','))}
#             )
#     return dicts_list
                


def format_search_by_params_query(base_query: str, info: dict[str | str]) -> str | tuple:
    """
    Function to format some SELECT search to READ action on CRUD

    :param query: the base SELECT query
    :param info: dict containing the columns name as keys and search values as values

    eg. {'cpf': '00083993456', 'nome': None}

    :return query and params: query and params, ready to bbe executed by cursor
    """
    conditions, params = [], []
    for k, v in info.items():
        if v:
            conditions.append(f'{k} = %s')
            params.append(v)
    
    if conditions:
        base_query += ' WHERE '
        base_query += " AND ".join(conditions)

    return base_query, tuple(params)
    
    


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