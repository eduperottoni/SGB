from flask import request, render_template, redirect
import logging
from psycopg2.errors import UniqueViolation
from datetime import datetime

from db_utils.utils import execute_query
from app_utils import get_registers_in_table

def authors_crud():
    action = request.args.get('action')
    logging.debug(action)

    if request.method == 'POST':
        msg, success = '', False
        logging.debug('ISSO FOI UM POST')
        if action in ['create', 'update']:
            author_form = request.form
            logging.debug(f'Vamos cadastrar/atualizar um autor: {author_form["nome"]}')

            if action == 'create':
                query = f'INSERT INTO Autor (nome, biografia, data_nascimento) VALUES {author_form["nome"], author_form["biografia"], author_form["data_nascimento"]}'

                try:
                    execute_query(query)
                    # Just for test pouposes:
                    query = f"SELECT * FROM Autor WHERE nome = %s;"
                    params = (author_form["nome"],)
                    logging.debug(execute_query(query, params))
                    msg = 'Autor criado com sucesso!'
                    success = True
                except UniqueViolation:
                    query = """
                    UPDATE Autor
                    SET ativo = %s
                    WHERE nome = %s AND biografia = %s AND data_nascimento = %s;
                    """
                    params = ('true', author_form["nome"], author_form["biografia"], author_form["data_nascimento"])
                    execute_query(query, params)
                    # Just for test pouposes:
                    # query = f"SELECT * FROM Autor WHERE nome = %s;"
                    # params = (author_form["nome"],)
                    # logging.debug(execute_query(query, params))
                    msg = 'Autor existia e foi reativado!'
                    success = True
                except Exception as e:
                    msg = f'Erro ao criar autor! {e}'
                    success = False


            elif action == 'update':
                logging.debug('Vamos atualizar o autor')
                logging.debug(author_form)

                query = """
                    UPDATE Autor 
                    SET nome = %s, biografia = %s, data_nascimento = %s
                    WHERE id = %s
                """
                values = (author_form["nome"], author_form["biografia"], author_form["data_nascimento"], author_form['id'])
                
                try:
                    execute_query(query, values)
                    msg = 'Autor atualizado com sucesso!'
                    success = True
                    # Test
                    # query = f"SELECT * FROM Autor WHERE nome = %s;"
                    # params = (author_form["nome"],)
                    # logging.debug(execute_query(query, params))
                except Exception as e:
                    msg = f'Erro ao atulizar autor! {e}'
                    success = False


        elif action == 'read':
            authors_info = {k:v for k, v in request.form.items() if v}

            try:
                tuples = get_registers_in_table('Autor', **authors_info)
                return render_template('general_read.html',
                                   response_list=tuples,
                                   keys_to_consider=[key for key in tuples[0]],
                                   entity='autor',
                                   try_again_link='authors_crud')
            except Exception as e:
                msg = 'Erro ao ler cliente'
                success = False            
        

        elif action == 'delete':
            logging.debug(request.form)

            try:
                query = "UPDATE Autor SET ativo = %s WHERE id = %s;"
                params = ('false', request.form.get('id'),)
                execute_query(query, params)
                logging.debug('Autor deletado')

                #Test
                query = f'SELECT * FROM Autor WHERE id = %s;'
                params = (request.form.get('id'),)
                tuples = execute_query(query, params)

                msg='Autor deletado com sucesso'
                success=True
            except:
                msg='Erro ao deletar autor'
                success=False
            

        return render_template('feedback_message.html',
                                msg = msg,
                                action = action,
                                success = success,
                                try_again_link = 'authors_crud')
            

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
                    authors_list = get_registers_in_table('Autor', ativo='true')
                    return render_template('choose_author.html', authors=authors_list)

        
        return render_template('form_author.html',
                                author_form=author_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('general_crud.html',
                           crud_action=action,
                           general_btn_name='autor',
                           url_self_crud='authors_crud'
                           )