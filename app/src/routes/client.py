from flask import request, render_template, redirect
import logging
from psycopg2.errors import UniqueViolation
from datetime import datetime

from db_utils.utils import execute_query
from app_utils import get_registers_in_table

def clients_crud():
    action = request.args.get('action')
    logging.debug(action)
    
    if request.method == 'POST':
        msg, success = '', False
        logging.debug('ISSO FOI UM POST')
        client_form = request.form
    
        if action == 'create':
            query = f'INSERT INTO Cliente (cpf, nome, data_nascimento, data_registro) VALUES {client_form["cpf"], client_form["nome"], client_form["data_nascimento"], datetime.now().isoformat()}'
            
            try:
                execute_query(query) 
                
                logging.debug('Cliente criado')
                query = f"SELECT * FROM Cliente WHERE cpf = %s;"
                params = (client_form["cpf"],)
                logging.debug(execute_query(query, params))
                msg = 'Cliente criado com sucesso'
                success = True
            except UniqueViolation:
                query = """
                UPDATE Cliente
                SET ativo = %s
                WHERE cpf = %s AND nome = %s AND data_nascimento = %s;
                """
                params = ('true', client_form['cpf'], client_form["nome"], client_form["data_nascimento"])
                execute_query(query, params)
                
                msg = 'Cliente existia e foi reativado!'
                success = True
            except Exception as e:
                msg = f'Erro ao criar cliente! {e}'
                success = False

        elif action == 'update':
            logging.debug('Vamos atualizar o cliente')
            logging.debug(client_form)

            query = """
                UPDATE Cliente 
                SET nome = %s, data_nascimento = %s
                WHERE cpf = %s
            """
            values = (client_form['nome'], client_form['data_nascimento'], client_form['cpf'])
            
            
            try:
                execute_query(query, values)

                # logging.debug('Cliente atualizado')
                # query = f"SELECT * FROM Cliente WHERE cpf = %s;"
                # params = (client_form["cpf"],)
                # logging.debug(execute_query(query, params))
                msg = 'Cliente atualizado com sucesso!'
                success = True
            except Exception as e:
                msg = f'Erro ao atulizar autor! {e}'
                success = False


        elif action == 'delete':

            client = get_client_with_open_rents(client_form['cpf'])
            # Se o cliente não tem empréstimos em aberto:
            if not client:
                query = "UPDATE Cliente SET ativo = %s WHERE cpf = %s"
                params = ('false', client_form['cpf'])
                execute_query(query, params)
                success = True
                msg = 'Cliente deletado com sucesso!'
            # Se o cliente tem empréstimos em aberto
            else:
                success = False
                msg = 'Cliente tem empréstimos em aberto e não pode ser deletado!'


        elif action == 'read':
            clients_info = {k: v for k, v in request.form.items() if v}

            try:
                tuples = get_registers_in_table('Cliente', **clients_info)
                
                return render_template('general_read.html',
                                   response_list=tuples,
                                   keys_to_consider=[key for key in tuples[0]],
                                   entity='cliente',
                                   try_again_link='clients_crud')
            except Exception as e:
                msg = 'Erro ao ler cliente'
        

        return render_template('feedback_message.html',
                                msg = msg,
                                action = action,
                                success = success,
                                try_again_link = 'clients_crud')

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

        
        return render_template('form_client.html',
                                client_form=client_form,
                                form_title=form_title,
                                crud_action=action)
    
    return render_template('general_crud.html',
                           crud_action=action,
                           general_btn_name='cliente',
                           url_self_crud='clients_crud'
                           )


def get_client_with_open_rents(cpf: str) -> 'list[RealDictRow]':
    query = """
    SELECT Cliente.cpf AS cpf_cliente, 
    Historico.id AS id_historico 
    FROM Cliente
    JOIN Historico ON Historico.cliente = Cliente.cpf AND Historico.data_devolucao IS NULL
    WHERE Cliente.cpf = %s
    """
    params = (cpf,)

    client = execute_query(query, params)

    return client