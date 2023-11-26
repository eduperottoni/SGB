from flask import request, render_template, redirect
import logging
from datetime import datetime

from db_utils.utils import execute_query
from app_utils import get_registers_in_table

def return_book():
    action = request.args.get('action')
    logging.debug(action)

    if request.method == 'POST':
        logging.debug('ISSO FOI A MERDA DE UM POST')
        return_form = request.form
        if 'id_historico' in return_form:
            query = f"SELECT livro FROM Historico WHERE id = '{return_form['id_historico']}'"
            tuples = execute_query(query)
            query = f"UPDATE Livro SET num_copias = num_copias + 1 WHERE id = '{tuples[0]['livro']}'"
            tuples = execute_query(query)
            query = f"""UPDATE Historico 
            SET data_devolucao = '{datetime.now().isoformat()}', 
            valor_pago = '{return_form['valor_pago']}' 
            WHERE id = '{return_form['id_historico']}'"""
            tuples = execute_query(query)

        elif 'cliente' in return_form:
            query = f"""SELECT livro.id, livro.titulo, historico.id AS id_historico
            FROM Historico JOIN Livro ON Historico.livro = livro.id
            WHERE historico.data_devolucao IS NULL 
            AND historico.cliente = '{return_form['cliente']}'"""
            tuples = execute_query(query)
            if tuples != None:
                form = {}
                form['livros'] = {k['id_historico']:k['titulo'] for k in tuples}
                form_title = 'Devolver livro'
                return render_template('form_return_step_2.html',
                                        return_form=form,
                                        form_title=form_title,
                                        crud_action=action)

    return_form = {}
    form_title='Registrar Devolução'
    tuples = get_registers_in_table('Cliente')
    return_form['clientes'] = {k['cpf']:k['nome'] for k in tuples}

    return render_template('form_return_step_1.html',
                            return_form=return_form,
                            form_title=form_title,
                            crud_action=action)
