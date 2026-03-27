from database.conexao import criar_conexao
from datetime import datetime

def criar_tarefa(titulo,descricao,status,prioridade):

    status= status.lower()
    prioridade = prioridade.lower()

    status_validos = ['pendente', 'andamento', 'concluido']
    prioridade_valido = ['baixa', 'medio', 'alta', 'urgente']

    if status not in status_validos:
        return False, 'Status inválido'

    if prioridade not in prioridade_valido:
        return False, 'Prioridade inválida'

    if not titulo.strip():
        return False,'Título não pode ser vazio'

    data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if status == 'concluido':
        data_conclusao = data_criacao
    else:
        data_conclusao = None


    con = criar_conexao()
    cur = con.cursor()

    try:
        cur.execute('''
        INSERT INTO tarefa(titulo,descricao,status,data_criacao, data_conclusao,prioridade)
        VALUES (?,?,?,?,?,?)
        ''',(titulo,descricao,status,data_criacao, data_conclusao,prioridade))

        con.commit()
        return True, 'Tarefa criada com sucesso'
    except Exception as e:
        return False, f'Erro ao criar tarefa: {e}'
    finally:
        con.close()


def listar_tarefas():
    con = criar_conexao()
    cur = con.cursor()

    try:
        cur.execute('''SELECT * FROM tarefa ORDER BY data_criacao DESC''')
        tarefas = cur.fetchall()

        if not tarefas:
            return False, 'Nenhuma tarefa encontrada'

        return True, tarefas

    except Exception as e:
        return False, f'Erro ao listar tarefa: {e}'
    finally:
        con.close()


def atualizar_tarefa(id_tarefa,titulo=None, descricao=None, prioridade=None):

    con = criar_conexao()
    cur = con.cursor()

    try:
        cur.execute('SELECT * FROM tarefa WHERE id = ?', (id_tarefa,))
        tarefa = cur.fetchone()

        if not tarefa:
            return False,'Tarefa não encontrada'

        campos = []
        valores = []

        if titulo is not None:
            if not titulo.strip():
                return False,'Título não pode ser vazio'
            campos.append('titulo = ?')
            valores.append(titulo)

        if descricao is not None:
            campos.append('descricao = ?')
            valores.append(descricao)

        if prioridade is not None:
            prioridade = prioridade.lower()
            prioridade_valido = ['baixa', 'medio', 'alta', 'urgente']

            if prioridade not in prioridade_valido:
                return False,'Prioridade inválida'
            campos.append('prioridade = ?')
            valores.append(prioridade)

        if not campos:
            return False,'Nenhum dado para atualizar'

        query = f'''
            UPDATE tarefa
            SET {', '.join(campos)}
            WHERE id = ?
        '''

        valores.append(id_tarefa)

        cur.execute(query, valores)
        con.commit()

        return True, 'Tarefa atualizada com sucesso'

    except Exception as e:
        return False, f'Erro ao atualizar tarefa: {e}'
    finally:
        con.close()

def atualizar_status_tarefa(id_tarefa,novo_status):

    novo_status = novo_status.lower()

    status_validos = ['pendente', 'andamento', 'concluido']

    if novo_status not in status_validos:
        return False, 'Status inválido'

    con = criar_conexao()
    cur = con.cursor()

    try:
        cur.execute('SELECT * FROM tarefa WHERE id = ?', (id_tarefa,))
        tarefa = cur.fetchone()

        if not tarefa:
            return False,'Tarefa não encontrada'

        if novo_status == 'concluido':
            data_conclusao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            data_conclusao = None

        cur.execute('''
        UPDATE tarefa
        SET status = ?, data_conclusao = ?
        WHERE id = ?
        ''',(novo_status,data_conclusao,id_tarefa))

        con.commit()
        return True, 'Status atualizado com sucesso'

    except Exception as e:
        return False, f'Erro ao atualizar status: {e}'
    finally:
        con.close()


def deletar_tarefa(id_tarefa):

    con = criar_conexao()
    cur = con.cursor()

    try:
        cur.execute('SELECT * FROM tarefa WHERE id = ?', (id_tarefa,))
        tarefa = cur.fetchone()

        if not tarefa:
            return False, 'Tarefa não encontrada'

        cur.execute('''DELETE FROM tarefa WHERE id = ?''', (id_tarefa,))
        con.commit()

        return True, 'Tarefa deletada com sucesso'

    except Exception as e:
        return False, f'Erro ao deletar tarefa: {e}'
    finally:
        con.close()