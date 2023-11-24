from flask import request, render_template
import logging
from datetime import datetime

from db_utils.db import execute_query
from app_utils import get_registers_in_table

def books_crud():
    action = request.args.get('action')
    logging.debug(action)
    
    if request.method == 'POST':
        logging.debug('ISSO FOI UM POST')
        book_form = request.form
    
        if action == 'create':
            query = f'INSERT INTO Livro (id, nome, data_nascimento, data_registro) VALUES {book_form["id"], book_form["nome"], book_form["data_nascimento"], datetime.now().isoformat()}'
            execute_query(query) 
            
            logging.debug('Livro criado')
            query = f"SELECT * FROM Livro WHERE id = %s;"
            params = (book_form["id"],)
            logging.debug(execute_query(query, params))

        elif action == 'update':
            logging.debug('Vamos atualizar o Livro')
            logging.debug(book_form)

            query = """
                UPDATE Livro 
                SET nome = %s, data_nascimento = %s
                WHERE id = %s
            """
            values = (book_form['nome'], book_form['data_nascimento'], book_form['id'])
            execute_query(query, values)

            logging.debug('Livro atualizado')
            query = f"SELECT * FROM Livro WHERE id = %s;"
            params = (book_form["id"],)
            logging.debug(execute_query(query, params))

        elif action == 'delete':
            logging.debug(request.form)
            #FIXME Ver se é possível deletar (se Livro não tem empréstimos pendentes, por exemplo)
            query = "UPDATE Livro SET ativo = %s WHERE id = %s"
            params = ('false', book_form['id'])
            execute_query(query, params)

            return render_template('feedback_message.html',
                                    msg = 'Livro deletado com sucesso!',
                                    action = action,
                                    success = True,
                                    try_again_link = 'books_crud')

            return redirect('/clients-crud/')


        elif action == 'read':
            books_info = {k: v for k, v in request.form.items() if v}

            tuples = get_registers_in_table('Livro', **books_info)

            logging.debug(f'MOSTRAREMOS OS RESULTADOS DA BUSCA POR Livros: {tuples}')
            
            return render_template('clients.html', search=tuples)

    # If method == 'GET':
    if action:
        book_form={}
        form_title=''
        match action:
            case 'update':
                if 'id' in request.args:
                    id = request.args.get('id')
                    query = f"SELECT * FROM Livro WHERE id = %s;"
                    params = (id,)
                    book_form = execute_query(query, params)[0]

                    form_title = 'Atualizar Livro'
                else:
                    query = """
                    SELECT 
                    Livro.id AS livro_id, Livro.titulo AS livro_titulo, Livro.lancamento, Livro.num_copias,
                    Autor.nome AS autor_nome,
                    Genero.nome AS genero_nome,
                    Editora.nome AS editora_nome
                    FROM Livro
                    JOIN Escrito_por ON Livro.id = Escrito_por.livro
                    JOIN Autor ON Escrito_por.autor = Autor.id
                    JOIN Editora ON Editora.id = Livro.editora
                    JOIN Sobre ON Livro.id = Sobre.livro
                    JOIN Genero ON Sobre.genero = Genero.nome
                    """
                    books_list = execute_query(query)
                    logging.debug(books_list)

                    return render_template('choose_book.html', books=books_list)

            case 'create':
                form_title='Cadastrar Livro'

                # Pega editoras para mostrar nos options dos selects
                tuples = get_registers_in_table('Editora')
                book_form['editoras'] = {k['id']:k['nome'] for k in tuples}
                tuples = get_registers_in_table('Autor')
                book_form['autores'] = {k['id']:k['nome'] for k in tuples}
                tuples = get_registers_in_table('Genero')
                book_form['generos'] = {k['nome']:k['descricao'] for k in tuples}

            case 'read':
                form_title = 'Buscar Livro'

            case 'delete':
                    books_list = get_registers_in_table('Livro', ativo='true')
                    return render_template('choose_book.html', clients=books_list)

        
        return render_template('book_form.html',
                                book_form=book_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('general_crud.html',
                           crud_action=action,
                           general_btn_name='Book',
                           url_self_crud='books_crud'
                           )