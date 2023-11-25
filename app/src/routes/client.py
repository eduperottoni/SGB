from flask import request, render_template
import logging
from datetime import datetime

from db_utils.db import execute_query
from app_utils import get_registers_in_table

def clients_crud():
    action = request.args.get('action')
    logging.debug(action)
    
    if request.method == 'POST':
        logging.debug('ISSO FOI UM POST')
        client_form = request.form
    
        if action == 'create':
            query = f'INSERT INTO Cliente (cpf, nome, data_nascimento, data_registro) VALUES {client_form["cpf"], client_form["nome"], client_form["data_nascimento"], datetime.now().isoformat()}'
            execute_query(query) 
            
            logging.debug('Cliente criado')
            query = f"SELECT * FROM Cliente WHERE cpf = %s;"
            params = (client_form["cpf"],)
            logging.debug(execute_query(query, params))

        elif action == 'update':
            logging.debug('Vamos atualizar o cliente')
            logging.debug(client_form)

            query = """
                UPDATE Cliente 
                SET nome = %s, data_nascimento = %s
                WHERE cpf = %s
            """
            values = (client_form['nome'], client_form['data_nascimento'], client_form['cpf'])
            execute_query(query, values)

            logging.debug('Cliente atualizado')
            query = f"SELECT * FROM Cliente WHERE cpf = %s;"
            params = (client_form["cpf"],)
            logging.debug(execute_query(query, params))

        elif action == 'delete':
            logging.debug(request.form)
            #FIXME Ver se é possível deletar (se cliente não tem empréstimos pendentes, por exemplo)
            query = "UPDATE Cliente SET ativo = %s WHERE cpf = %s"
            params = ('false', client_form['cpf'])
            execute_query(query, params)

            return render_template('feedback_message.html',
                                    msg = 'Cliente deletado com sucesso!',
                                    action = action,
                                    success = True,
                                    try_again_link = 'clients_crud')

            return redirect('/clients-crud/')


        elif action == 'read':
            clients_info = {k: v for k, v in request.form.items() if v}

            tuples = get_registers_in_table('Cliente', **clients_info)

            logging.debug(f'MOSTRAREMOS OS RESULTADOS DA BUSCA POR CLIENTES: {tuples}')
            
            return render_template('clients.html', search=tuples)

    # If method == 'GET':
    if action:
        client_form={}
        form_title=''
        match action:
            case 'update':
                if 'cpf' in request.args:
                    # try:
                    cpf = request.args.get('cpf')
                    query = f"SELECT * FROM Cliente WHERE cpf = %s;"
                    params = (cpf,)
                    client_form = execute_query(query, params)[0]

                    form_title = 'Atualizar cliente'
                    # except Exception as e:
                    #     return render_template('error.html',
                    #                         msg="Erro ao recuperar o CPF especificado",
                    #                         url_for_link="clients_crud",
                    #                         action_link='update')
                else:
                    clients_list = get_registers_in_table('Cliente')
                    return render_template('choose_client.html', clients=clients_list)

            case 'create':
                form_title='Cadastrar cliente'

            case 'read':
                form_title = 'Buscar cliente'

            case 'delete':
                    clients_list = get_registers_in_table('Cliente', ativo='true')
                    return render_template('choose_client.html', clients=clients_list)

        
        return render_template('client_form.html',
                                client_form=client_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('general_crud.html',
                           crud_action=action,
                           general_btn_name='Client',
                           url_self_crud='clients_crud'
                           )