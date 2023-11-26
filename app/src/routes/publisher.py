from flask import request, render_template, redirect
import logging
from datetime import datetime
from psycopg2.errors import UniqueViolation
from db_utils.utils import execute_query
from app_utils import get_registers_in_table

def publishers_crud():
    action = request.args.get('action')
    logging.debug(action)
    
    if request.method == 'POST':
        logging.debug('ISSO FOI UM POST')
        msg, success = '', False

        if action in ['create', 'update']:
            publishers_form = request.form
            logging.debug(f'Vamos cadastrar/atualizar uma editora: {publishers_form["nome"]}')

            if action == 'create':
                query = f'INSERT INTO Editora (nome, endereco, contato) VALUES {publishers_form["nome"], publishers_form["endereco"], publishers_form["contato"]}'
                
                try:
                    execute_query(query) 
                    success, msg = True, 'Editora inserida com sucesso!'
                    
                    #Test
                    # logging.debug('Editora criada')
                    # query = f"SELECT * FROM Editora WHERE nome = %s;"
                    # params = (publishers_form["nome"],)
                    # logging.debug(execute_query(query, params))
                except UniqueViolation:
                    query = """
                    UPDATE Editora
                    SET ativo = %s
                    WHERE nome = %s AND endereco = %s AND contato = %s;
                    """
                    params = ('true', publishers_form["nome"], publishers_form["endereco"], publishers_form["contato"])
                    execute_query(query, params)
                    # Just for test pouposes:
                    # query = f"SELECT * FROM Autor WHERE nome = %s;"
                    # params = (author_form["nome"],)
                    # logging.debug(execute_query(query, params))
                    msg = 'Editora existia e foi reativada!'
                    success = True
                except Exception as e:
                    msg = f'Erro ao criar editora! {e}'
                    success = False

            elif action == 'update':
                logging.debug('Vamos atualizar a editora')
                logging.debug(publishers_form)

                query = """
                    UPDATE Editora 
                    SET nome = %s, endereco = %s, contato = %s
                    WHERE id = %s
                """
                values = (publishers_form["nome"], publishers_form["endereco"], publishers_form["contato"], publishers_form['id'])
                
                try:
                    execute_query(query, values)
                    success, msg = True, 'Editora modificada com sucesso!'

                    #Test
                    # logging.debug('Editora atualizada')
                    # query = f"SELECT * FROM Editora WHERE nome = %s;"
                    # params = (publishers_form["nome"],)
                    # logging.debug(execute_query(query, params))
                except Exception as e:
                    success, msg = False, f'Erro ao modificar editora! {e}'

        elif action == 'read':
            publishers_info = {k: v for k, v in request.form.items() if v}
            
            try:
                tuples = get_registers_in_table('Editora', **publishers_info)

                return render_template('general_read.html',
                                   response_list=tuples,
                                   keys_to_consider=[key for key in tuples[0]],
                                   entity='editora',
                                   try_again_link='publishers_crud')
            except Exception as e:
                success, msg = f'Erro ao ler editora! {e}'
        
        elif action == 'delete':
            logging.debug('ID', request.form.get('id'))

            try:
                query = "UPDATE Editora SET ativo = %s WHERE id = %s;"
                params = ('false', request.form.get('id'))
                execute_query(query, params)
                logging.debug('Editora deletada')

                #Test
                # query = f'SELECT * FROM Editora WHERE nome = %s;'
                # params = (request.form.get('nome'),)
                # tuples = execute_query(query, params)
                success, msg = True, 'Editora deletada com sucesso!'
            except Exception as e:
                success, msg = False, f'Erro em deletar a editora! {e}'


        return render_template('feedback_message.html',
                                msg = msg,
                                action = action,
                                success = success,
                                try_again_link = 'publishers_crud')

    # If method == 'GET':
    if action:
        publisher_form={}
        form_title=''
        match action:
            case 'update':
                if 'nome' in request.args:
                    nome = request.args.get('nome')
                    query = f"SELECT * FROM Editora WHERE nome = %s;"
                    params = (nome,)
                    publisher_form = execute_query(query, params)[0]

                    logging.debug('111111111111111111111111')
                    logging.debug(publisher_form)

                    form_title = 'Atualizar editora'

                else:
                    publishers_list = get_registers_in_table('Editora', ativo='true')
                    return render_template('choose_publisher.html', publishers=publishers_list)

            case 'create':
                form_title='Cadastrar editora'

            case 'read':
                form_title = 'Buscar editora'

            case 'delete':
                    publishers_list = get_registers_in_table('Editora', ativo='true')
                    return render_template('choose_publisher.html', publishers=publishers_list)

        
        return render_template('form_publisher.html',
                                publisher_form=publisher_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('general_crud.html',
                           crud_action=action,
                           general_btn_name='editora',
                           url_self_crud='publishers_crud'
                           )