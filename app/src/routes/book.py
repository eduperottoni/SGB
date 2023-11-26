from flask import request, render_template, redirect
import logging
from datetime import datetime
from psycopg2 import IntegrityError
from db_utils.utils import execute_query
from app_utils import get_registers_in_table

def books_crud():
    action = request.args.get('action')
    logging.debug(action)
    
    if request.method == 'POST':
        msg, success = '', False
        logging.debug('ISSO FOI UM POST')
        book_form = request.form
        logging.debug(book_form)
        logging.debug(request.args)
    
        if action == 'create':
            logging.debug('Criando livro')
            logging.debug(book_form)

            book = get_book_with_params(
                titulo=book_form['titulo'],
                editora=book_form['editora'],
                lancamento=book_form['lancamento']
            )

            logging.debug(book)

            # Caso haja livro com essas informações,
            # ativá-lo e alterar o número de exemplares
            if book:
                logging.debug(book[0]['ativo'])
                if book[0]['ativo'] == False:
                    logging.debug('O LIVRO ESTÁ DESATIVADO! ATIVÁ-LO!')
                    query = "UPDATE Livro SET ativo = %s, num_copias = %s WHERE id = %s"
                    params= ('true', book_form['num_copias'], book[0]['id'])
                    try:
                        execute_query(query, params)
                        msg = 'Livro existia e foi reativado!'
                        success = True
                    except Exception as e:
                        msg = e
                        success = False
                    finally:
                        return render_template(
                            'feedback_message.html',
                            msg = msg,
                            action = action,
                            success = success,
                            try_again_link = 'books_crud'
                        )

                else:
                    return render_template(
                        'feedback_message.html',
                        msg = 'Livro já está criado e é ativo!',
                        action = action,
                        success = False,
                        try_again_link = 'books_crud'
                    )
            # Caso não exista, criar
            else:
                logging.debug('Livro não existe e vamos criá-lo!')

                query = f"INSERT INTO Livro (titulo, lancamento, editora, num_copias) VALUES {book_form['titulo'], book_form['lancamento'], book_form['editora'], book_form['num_copias']}"
                logging.debug(book_form)
                params = ()
                msg, success = '', False
                try:
                    execute_query(query, params)
                    msg = 'Livro inserido com sucesso!'
                    success = True
                except Exception as e:
                    logging.debug('DEU PROBLEM')
                    msg = e
                    success = False
                finally:
                    return render_template(
                        'feedback_message.html',
                        msg = msg,
                        action = action,
                        success = success,
                        try_again_link = 'books_crud'
                    )

        elif action == 'update':
            logging.debug('Vamos atualizar o Livro')
            logging.debug(book_form)

            #1 - Update na tabela de livros
            try:
                query = """
                    UPDATE Livro 
                    SET titulo = %s, lancamento = %s, editora = %s, genero= %s, num_copias = %s
                    WHERE id = %s
                """
                values = (book_form['titulo'], book_form['lancamento'], book_form['editora'], book_form['genero'], book_form['num_copias'], book_form['id'])
                execute_query(query, values)
                # Test
                # query = f"SELECT * FROM Livro WHERE id = %s;"
                # params = (book_form["id"],)
                # logging.debug(execute_query(query, params))

                msg, success = f'Sucesso ao atualizar o livro {book_form["titulo"]}!', True
            except Exception as e:
                msg, success = 'Erro a atualizar o livro! {e}', False

        elif action == 'delete':

            # We check if the book has pending rents
            lendings = get_all_lendings_from_book(int(book_form['id']))

            if lendings:
                msg, success = 'Livro não pode ser deletado, há empréstimos com ele!', False
            else:
                try:
                    query = "UPDATE Livro SET ativo = %s WHERE id = %s"
                    params = ('false', book_form['id'])
                    execute_query(query, params)
                    msg, success = 'Livro deletado com sucesso!', True
                except Exception as e:
                    msg, success = 'Erro no delete do livro!', False


        elif action == 'read':
            books_info = {k: v for k, v in request.form.items() if v}

            tuples = get_registers_in_table('Livro', **books_info)

            logging.debug(f'MOSTRAREMOS OS RESULTADOS DA BUSCA POR Livros: {tuples}')
            
            return render_template('clients.html', search=tuples)
        
        elif action == 'add_remove_author':
            logging.debug('VAMOS ADICIONAR AUTORES AO LIVRO')
            form = request.form
            livro = form['id']

            #1 - Deletamos os escritores dos livros
            query = """
            DELETE FROM Escrito_por
            WHERE livro = %s
            """
            params = (livro,)
            execute_query(query, params)

            #2 - Adicionamos os 
            for k in form:
                if k != 'id':
                    logging.debug(f'iremos adicionar autor {k} ao livro {form["id"]}')
                    try:
                        query = """
                        INSERT INTO Escrito_por (autor, livro) VALUES (%s, %s)
                        """
                        params = (k, livro)
                        execute_query(query, params)
                        msg = 'Sucesso ao adicionar/remover autor(es)!'
                        success = True
                        # Test
                        # query = """
                        # SELECT *
                        # FROM Escrito_por
                        # WHERE livro = %s
                        # """
                        # params = (form['id'],)
                        # logging.debug(execute_query(query, params))
                    except Exception as e:
                        logging.debug(e)
                        msg = f'Erro ao adicionar autor! {e}!'
                        success = False

        return render_template('feedback_message.html',
                                msg = msg,
                                action = action,
                                success = success,
                                try_again_link = 'books_crud')


    # If method == 'GET':
    if action:
        book_form={}
        form_title=''
        if action in ['update', 'delete', 'add_remove_author']:
            if 'id' in request.args:
                if action == 'add_remove_author':
                    book_form['id'] = request.args.get('id')
                    tuples = get_registers_in_table('Autor', ativo = 'true')
                    book_form['autores_totais'] = {k['id']:k['nome'] for k in tuples}
                    id = request.args.get('id')
                    logging.debug(book_form)
                    tuples = get_registers_in_table('Escrito_por', livro=id)
                    book_form['autores_livro'] = [k['autor']for k in tuples]
                    logging.debug(book_form)
                    return render_template('form_authors_in_book.html',
                                            book_form=book_form,
                                            form_title='Modificar autores do livro',
                                            crud_action=action)

                elif action == 'update':
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

            else:
                books_informations = get_books_informations()
                return render_template('choose_book.html', books=books_informations)

        elif action == 'create':
            form_title='Cadastrar Livro'

            # Pega editoras para mostrar nos options dos selects
            tuples = get_registers_in_table('Editora', ativo='true')
            book_form['editoras'] = {k['id']:k['nome'] for k in tuples}
            tuples = get_registers_in_table('Autor', ativo='true')
            book_form['autores'] = {k['id']:k['nome'] for k in tuples}
            tuples = get_registers_in_table('Genero', ativo='true')
            book_form['generos'] = {k['nome']:k['descricao'] for k in tuples}

        elif action == 'read':
                form_title = 'Buscar Livro'

        return render_template('form_book.html',
                                book_form=book_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('general_crud.html',
                           crud_action=action,
                           general_btn_name='livro',
                           url_self_crud='books_crud'
                           )


def get_books_informations() -> 'list[RealDictRow]':
    query = """
    SELECT 
    Livro.id AS livro_id, Livro.titulo AS livro_titulo, Livro.lancamento, Livro.num_copias,
    Autor.nome AS autor_nome,
    Livro.genero AS genero_nome,
    Editora.nome AS editora_nome
    FROM Livro
    JOIN Escrito_por ON Livro.id = Escrito_por.livro
    JOIN Autor ON Escrito_por.autor = Autor.id
    JOIN Editora ON Editora.id = Livro.editora
    WHERE Livro.ativo = %s
    """
    params=('true',)

    books_list = execute_query(query, params)
    return books_list


def get_all_lendings_from_book(id: int) -> 'list[RealDictRow]':
    query = "SELECT * FROM Historico WHERE livro = %s AND data_devolucao IS NULL"
    params = (id,)
    return execute_query(query, params)

def get_book_with_params(**params) -> 'list[RealDictRow]':
    logging.debug(params)
    book = get_registers_in_table('Livro', **params)
    logging.debug('Book reached')
    logging.debug(book)
    return book


def get_autor_by_id(id: int) -> 'list[RealDictRow]':
    author = get_registers_in_table('Autor', id=id)
    return author