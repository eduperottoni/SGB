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
    query = "SELECT * FROM Autor WHERE nome = %s;"
    params = ('Agatha Christie',)
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
            logging.debug()

    # If method == 'GET':
    if action:
        client_form={}
        form_title=''
        match action:
            case 'update':
                if 'cpf' in request.args:
                    # try:
                    cpf = request.args.get('cpf')
                    query = f"SELECT (cpf, nome, data_nascimento) FROM Cliente WHERE cpf = %s;"
                    params = (cpf,)
                    tuple = execute_query(query, params)
                    clients_list = get_dicts_from_tuples(tuple, ['cpf', 'nome', 'data_nascimento'])
                    clients_list[0]['nome'] = clients_list[0]['nome'][1:-1]
                    client_form = clients_list[0]
                    form_title = 'Atualizar cliente'
                    # except Exception as e:
                    #     return render_template('error.html',
                    #                         msg="Erro ao recuperar o CPF especificado",
                    #                         url_for_link="clients_crud",
                    #                         action_link='update')
                else:
                    clients_list = get_all_clients_from_db()
                    return render_template('choose_client.html', clients=clients_list)

            case 'create':
                form_title='Cadastrar cliente'

            case 'read':
                form_title = 'Buscar cliente'

            case 'delete':
                    clients_list = get_all_clients_from_db()
                    return render_template('choose_client.html', clients=clients_list)

        
        return render_template('client_form.html',
                                client_form=client_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('clients_crud.html', crud_action=action)


def get_all_clients_from_db():
    query = f"SELECT (cpf, nome, data_nascimento) FROM Cliente"
    tuples = execute_query(query)
    clients_list = get_dicts_from_tuples(tuples, ['cpf', 'nome', 'data_nascimento'])
    return clients_list


def get_dicts_from_tuples(tuples: list[str], keys_list: list[str]) -> list[dict[str | str]]:
    """
    Function to transform a result from a db query to a dict based on the specified keys

    :param tuples: tuples from DB
    :param keys_list: list with keys, in the order of the tuples resultss
    :return: the result dict
    """
    dicts_list = []
    for tuple in tuples:
        logging.debug(tuple)
        for t in tuple:
            t = t[1:-1]
            dicts_list.append(
                {keys_list[index]: column for index, column in enumerate(t.split(','))}
            )
    return dicts_list
                


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