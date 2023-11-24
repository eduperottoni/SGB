from flask import request, render_template
import logging
from datetime import datetime

from db_utils.db import execute_query
from app_utils import get_registers_in_table

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
                    SET nome = %s, biografia = %s, data_nascimento = %s
                    WHERE id = %s
                """
                values = (author_form["nome"], author_form["biografia"], author_form["data_nascimento"], author_form['id'])
                execute_query(query, values)

                logging.debug('Autor atualizado')
                query = f"SELECT * FROM Autor WHERE nome = %s;"
                params = (author_form["nome"],)
                logging.debug(execute_query(query, params))

            elif action == 'delete':
                return render_template()
                
            return redirect('/authors-crud/')

        elif action == 'read':
            authors_info = {k:v for k, v in request.form.items() if v}

            tuples = get_registers_in_table('Autor', **authors_info)
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

                    nome = request.args.get('nome')
                    query = f"SELECT * FROM Autor WHERE nome = %s;"
                    params = (nome,)
                    author_form = execute_query(query, params)[0]

                    form_title = 'Atualizar autor'

                else:
                    authors_list = get_registers_in_table('Autor')
                    return render_template('choose_author.html', authors=authors_list)

            case 'create':
                form_title='Cadastrar autor'

            case 'read':
                form_title = 'Buscar autor'

            case 'delete':
                    authors_list = get_registers_in_table('Autor')
                    return render_template('choose_author.html', authors=authors_list)

        
        return render_template('author_form.html',
                                author_form=author_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('authors_crud.html', crud_action=action)