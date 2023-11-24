from flask import request, render_template
import logging
from datetime import datetime

from db_utils.db import execute_query
from app_utils import get_registers_in_table

def genres_crud():
    action = request.args.get('action')
    logging.debug(action)
    
    if request.method == 'POST':
        logging.debug('ISSO FOI UM POST')
        if action in ['create', 'update']:
            genres_form = request.form
            logging.debug(f'Vamos cadastrar/atualizar um genero: {genres_form["nome"]}')

            if action == 'create':
                query = f'INSERT INTO Genero (nome, descricao) VALUES {genres_form["nome"], genres_form["descricao"]}'
                execute_query(query) 
                
                logging.debug('Genero criado')
                query = f"SELECT * FROM Genero WHERE nome = %s;"
                params = (genres_form["nome"],)
                logging.debug(execute_query(query, params))

            elif action == 'update':
                logging.debug('Vamos atualizar o genero')
                logging.debug(genres_form)

                query = """
                    UPDATE Genero 
                    SET nome = %s, descricao = %s
                    WHERE nome = %s
                """
                values = (genres_form["nome"], genres_form["endereco"], genres_form['nome'])
                execute_query(query, values)

                logging.debug('Genero atualizado')
                query = f"SELECT * FROM Genero WHERE nome = %s;"
                params = (genres_form["nome"],)
                logging.debug(execute_query(query, params))

            elif action == 'delete':
                return render_template()
                
            return redirect('/genres-crud/')

        elif action == 'read':
            genres_info = {k: v for k, v in request.form.items()}
            tuples = get_registers_in_table('Genero', **genres_info)

            logging.debug(f'MOSTRAREMOS OS RESULTADOS DA BUSCA POR GENERO: {tuples}')
            
            return render_template('genres.html', search=tuples)
        
        elif action == 'delete':
            #TODO Ver se é possível deletar (se o cliente não tem empréstimos pendentes)
            query = f"DELETE FROM Genero WHERE nome = %s;"
            params = (request.form.get('nome'),)
            execute_query(query, params)
            logging.debug('Genero deletada')

            query = f'SELECT * FROM Genero WHERE nome = %s;'
            params = (request.form.get('nome'),)
            tuples = execute_query(query, params)

    # If method == 'GET':
    if action:
        genre_form={}
        form_title=''
        match action:
            case 'update':
                if 'nome' in request.args:
                    nome = request.args.get('nome')
                    query = f"SELECT * FROM Genero WHERE nome = %s;"
                    params = (nome,)
                    genre_form = execute_query(query, params)[0]

                    logging.debug('111111111111111111111111')
                    logging.debug(genre_form)

                    form_title = 'Atualizar genero'

                else:
                    genres_list = get_registers_in_table('Genero')
                    logging.debug(genres_list)
                    return render_template('choose_genre.html', genres=genres_list)

            case 'create':
                form_title='Cadastrar genero'

            case 'read':
                form_title = 'Buscar genero'

            case 'delete':
                    genres_list = get_registers_in_table('Genero')
                    logging.debug(genres_list)
                    return render_template('choose_genre.html', genres=genres_list)

        
        return render_template('genre_form.html',
                                genre_form=genre_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('genres_crud.html', crud_action=action)