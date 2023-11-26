from flask import request, render_template, redirect
import logging
from datetime import datetime

from db_utils.utils import execute_query
from app_utils import get_registers_in_table

def rent_book():
    action = request.args.get('action')
    logging.debug(action)

    if request.method == 'POST':
        rent_form = request.form
        query = f"INSERT INTO Historico (data_aluguel, data_devolucao, valor_pago, cliente, livro) VALUES ('{datetime.now().isoformat()}', NULL, NULL, '{rent_form['cliente']}', '{rent_form['livro']}')"
        tuples = execute_query(query)
        query = f"UPDATE Livro SET num_copias = num_copias - 1 WHERE id = '{rent_form['livro']}'"
        tuples = execute_query(query)

        success = True
        msg = "Livro alugado com sucesso!"
        return render_template('feedback_message.html',
                                msg = msg,
                                action = action,
                                success = success,
                                try_again_link = 'rent_book')

    rent_form = {}
    form_title='Registrar Empréstimo'
    tuples = get_registers_in_table('Cliente')
    rent_form['clientes'] = {k['cpf']:k['nome'] for k in tuples}
    query = "SELECT * FROM Livro WHERE num_copias > 0"
    tuples = execute_query(query)
    rent_form['livros'] = {k['id']:k['titulo'] for k in tuples}

    return render_template('form_rent.html',
                            rent_form=rent_form,
                            form_title=form_title,
                            crud_action=action)
