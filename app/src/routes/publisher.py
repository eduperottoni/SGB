from flask import request, render_template
import logging
from datetime import datetime

from db_utils.db import execute_query
from app_utils import get_registers_in_table

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
            publishers_info = {k: v for k, v in request.form.items() if v}
            tuples = get_registers_in_table('Editora', **publishers_info)

            logging.debug(f'MOSTRAREMOS OS RESULTADOS DA BUSCA POR EDITORA: {tuples}')
            
            return render_template('publishers.html', search=tuples)
        
        elif action == 'delete':
            query = f"DELETE FROM Editora WHERE nome = %s;"
            params = (request.form.get('nome'),)
            execute_query(query, params)
            logging.debug('Editora deletada')

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
                    nome = request.args.get('nome')
                    query = f"SELECT * FROM Editora WHERE nome = %s;"
                    params = (nome,)
                    publisher_form = execute_query(query, params)[0]

                    logging.debug('111111111111111111111111')
                    logging.debug(publisher_form)

                    form_title = 'Atualizar editora'

                else:
                    publishers_list = get_registers_in_table('Editora')
                    return render_template('choose_publisher.html', publishers=publishers_list)

            case 'create':
                form_title='Cadastrar editora'

            case 'read':
                form_title = 'Buscar editora'

            case 'delete':
                    publishers_list = get_registers_in_table('Editora')
                    return render_template('choose_publisher.html', publishers=publishers_list)

        
        return render_template('publisher_form.html',
                                publisher_form=publisher_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('publishers_crud.html', crud_action=action)