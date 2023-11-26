from flask import request, render_template, redirect
import logging
from datetime import datetime
from psycopg2.errors import UniqueViolation

from db_utils.utils import execute_query
from app_utils import get_registers_in_table

def genres_crud():
    action = request.args.get('action')
    logging.debug(action)
    
    if request.method == 'POST':
        msg, success = '', False
        logging.debug('ISSO FOI UM POST')
        if action in ['create', 'update']:
            genres_form = request.form
            logging.debug(f'Vamos cadastrar/atualizar um genero: {genres_form["nome"]}')

            if action == 'create':
                query = f'INSERT INTO Genero (nome, descricao) VALUES {genres_form["nome"], genres_form["descricao"]}'
                

                try:
                    execute_query(query)
                    msg = 'Genero adicionado com sucesso'
                    success = True
                    # logging.debug('Genero criado')
                    # query = f"SELECT * FROM Genero WHERE nome = %s;"
                    # params = (genres_form["nome"],)
                    # logging.debug(execute_query(query, params))
                except UniqueViolation:
                    query="""
                    UPDATE Genero
                    SET ativo = %s
                    WHERE descricao = %s
                    """
                    params = ('true', genres_form['descricao'])
                    execute_query(query, params)
                    msg = 'Gênero existia e foi reativado!'
                    success = True
                except Exception as e:
                    msg = f'Erro ao criar gênero! {e}'
                    success = False


            elif action == 'update':
                logging.debug('Vamos atualizar o genero')
                logging.debug(genres_form)

                query = """
                    UPDATE Genero 
                    SET nome = %s, descricao = %s
                    WHERE nome = %s
                """
                values = (genres_form["nome"], genres_form["descricao"], genres_form['nome'])
                
                try:
                    execute_query(query, values)
                    msg = 'Gênero atualizado com sucesso!'
                    success = True

                    # logging.debug('Genero atualizado')
                    # query = f"SELECT * FROM Genero WHERE nome = %s;"
                    # params = (genres_form["nome"],)
                    # logging.debug(execute_query(query, params))
                except Exception as e:
                    msg= f'Erro ao atualizar autor! {e}'
                    success = False


        elif action == 'read':
            genres_info = {k: v for k, v in request.form.items() if v}
            
            try:
                tuples = get_registers_in_table('Genero', **genres_info)

                logging.debug(f'MOSTRAREMOS OS RESULTADOS DA BUSCA POR GENERO: {tuples}')
                
                return render_template('general_read.html',
                                   response_list=tuples,
                                   keys_to_consider=[key for key in tuples[0]],
                                   entity='gênero',
                                   try_again_link='genres_crud')
            except Exception as e:
                msg = f'Erro ao ler gênero! {e}'
                success = False
        
        elif action == 'delete':
            
            try:

                query = """
                UPDATE Genero
                SET ativo = %s WHERE nome = %s;
                """
                params = ('false', request.form.get('nome'),)
                execute_query(query, params)
                logging.debug('Genero deletado')

                id = request.args.get('id')
                query = f"SELECT * FROM Livro WHERE id = %s;"
                params = (id,)
                book_form = execute_query(query, params)[0]

                form_title = 'Atualizar Livro'
                # Pega editoras para mostrar nos options dos selects
                tuples = get_registers_in_table('Editora', ativo='true')
                book_form['editoras'] = {k['id']:k['nome'] for k in tuples}
                tuples = get_registers_in_table('Autor', ativo='true')
                book_form['autores'] = {k['id']:k['nome'] for k in tuples}
                tuples = get_registers_in_table('Genero', ativo='true')
                book_form['generos'] = {k['nome']:k['descricao'] for k in tuples}
                # Test
                # query = f'SELECT ativo FROM Genero WHERE nome = %s;'
                # params = (request.form.get('nome'),)
                # tuples = execute_query(query, params)

                msg = 'Gênero deletado com sucesso!'
                success=True
            except Exception as e:
                msg = f'Erro ao deletar gênero! {e}'
                success = False
                

            
        
        return render_template('feedback_message.html',
                        msg = msg,
                        action = action,
                        success = success,
                        try_again_link = 'genres_crud')

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

        
        return render_template('form_genre.html',
                                genre_form=genre_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('general_crud.html',
                           crud_action=action,
                           general_btn_name='Gênero',
                           url_self_crud='genres_crud'
                           )