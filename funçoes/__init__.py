from time import sleep
from database.operaçoes import *
from database import operaçoes
from facilitadores import linha


def menu():
    while True:
        print(linha())
        print('Gerenciador de Tarefas')
        print(linha())
        print('1 - Criar Tarefa\n'
              '2 - Listar Tarefas\n'
              '3 - Atualizar detalhes da Tarefa\n'
              '4 - Atualizar status da Tarefa\n'
              '5 - Deletar Tarefa\n'
              '0 - Sair')
        try:
            opcao = int(input('Escolha uma opção: '))
        except ValueError:
            print('Opcao invalida! Digite apenas as opções acima!')
            continue

        if opcao == 1:
            cadastrar_tarefa()
        elif opcao == 2:
            listar_tarefa()
        elif opcao == 3:
            atualizar_tarefas()
        elif opcao == 4:
            atualizar_status()
        elif opcao == 5:
            deletar_tarefas()
        elif opcao == 0:
            print(linha())
            print('Saindo do sistema')
            print(linha())
            break
        else:
            print('Opção inválida! Digite uma opção válida!')


def pergunta_continuar(msg):
    while True:
        resp = input(msg).strip().lower()
        if resp in ['s', 'sim']:
            return 's'
        elif resp in ['n', 'nao', 'não']:
            return 'n'
        else:
            print('Digite Apenas S, N, Sim, Não')


def cadastrar_tarefa():
    while True:
        print(linha())
        print('Criação de Tarefa')
        print(linha())
        try:
            titulo=input('Digite o titulo do Tarefa: ')
            descricao=input('Descreva a tarefa: ')

            status_opcoes = ['pendente', 'andamento', 'concluido']
            print('\nEscolha o status:')
            for i, opcao in enumerate(status_opcoes, start=1):
                print(f'{i} - {opcao}')

            while True:
                try:
                    escolha = int(input('Opção: '))
                    if 1 <= escolha <= len(status_opcoes):
                        status = status_opcoes[escolha - 1]
                        break
                    else:
                        print('⚠️ Opção inválida!')
                except ValueError:
                    print('⚠️ Digite um número válido!')

            prioridade_opcoes = ['baixa', 'medio', 'alta', 'urgente']
            print('\nEscolha a prioridade:')
            for i, opcao in enumerate(prioridade_opcoes, start=1):
                print(f'{i} - {opcao}')

            while True:
                try:
                    escolha = int(input('Opção: '))
                    if 1 <= escolha <= len(prioridade_opcoes):
                        prioridade = prioridade_opcoes[escolha - 1]
                        break
                    else:
                        print('⚠️ Opção inválida!')
                except ValueError:
                    print('⚠️ Digite um número válido!')


            valido, msg = criar_tarefa(titulo, descricao, status, prioridade)

            if not valido:
                print(f'⚠️ {msg}')
                continue

            print(f'✅ Tarefa "{titulo}" cadastrada com sucesso!')
            sleep(2)

        except Exception:
            print('Erro ao cadastrar tarefa! Tente novamente!')

        if pergunta_continuar('Deseja cadastrar nova tarefa? [S/N]: ') == 'n':
            break


def listar_tarefa():
    print(linha())
    print('LISTA DE TAREFAS'.center(40))
    print(linha())

    resultado, dados = listar_tarefas()

    if not resultado:
        print(f'⚠️ {dados}')
        return

    for t in dados:
        print(linha())
        print(f'ID: {t[0]}')
        print(f'Título: {t[1]}')
        print(f'Descrição: {t[2]}')
        print(f'Status: {t[3]}')
        print(f'Data de criação: {t[4]}')
        print(f'Data de conclusão: {t[5] if t[5] else "—"}')
        print(f'Prioridade: {t[6]}')
    print(linha())


def atualizar_tarefas():
    while True:
        print(linha())
        print('ATUALIZAR TAREFA'.center(40))
        print(linha())

        try:
            id_tarefa = int(input('Digite o ID da tarefa: '))


            resultado, dados = listar_tarefas()

            if not resultado:
                print(f'⚠️ {dados}')
                continue

            tarefa_encontrada = None
            for t in dados:
                if t[0] == id_tarefa:
                    tarefa_encontrada = t
                    break

            if not tarefa_encontrada:
                print('⚠️ Tarefa não encontrada!')
                continue


            print('\nDados atuais:')
            print(f'Título: {tarefa_encontrada[1]}')
            print(f'Descrição: {tarefa_encontrada[2]}')
            print(f'Prioridade: {tarefa_encontrada[6]}')

            print('\nDeixe vazio para manter o valor atual.\n')


            novo_titulo = input('Novo título: ').strip() or None
            nova_descricao = input('Nova descrição: ').strip() or None


            prioridade_opcoes = ['baixa', 'medio', 'alta', 'urgente']

            print('\nDeseja alterar a prioridade?')
            print('1 - Sim')
            print('2 - Não')

            alterar = input('Opção: ')

            nova_prioridade = None

            if alterar == '1':
                print('\nEscolha a nova prioridade:')
                for i, opcao in enumerate(prioridade_opcoes, start=1):
                    print(f'{i} - {opcao}')

                while True:
                    try:
                        escolha = int(input('Opção: '))
                        if 1 <= escolha <= len(prioridade_opcoes):
                            nova_prioridade = prioridade_opcoes[escolha - 1]
                            break
                        else:
                            print('⚠️ Opção inválida!')
                    except ValueError:
                        print('⚠️ Digite um número válido!')


            valido, msg = atualizar_tarefa(
                id_tarefa,
                novo_titulo,
                nova_descricao,
                nova_prioridade
            )

            if not valido:
                print(f'⚠️ {msg}')
                continue

            print('✅ Tarefa atualizada com sucesso!')
            sleep(2)

        except Exception:
            print('Erro ao atualizar tarefa!')

        if pergunta_continuar('Deseja atualizar outra tarefa? [S/N]: ') == 'n':
            break


def atualizar_status():
    while True:
        print(linha())
        print('ATUALIZAR STATUS DA TAREFA'.center(40))
        print(linha())

        try:
            id_tarefa = int(input('Digite o ID da tarefa: '))


            resultado, dados = listar_tarefas()

            if not resultado:
                print(f'⚠️ {dados}')
                continue

            tarefa_encontrada = None
            for t in dados:
                if t[0] == id_tarefa:
                    tarefa_encontrada = t
                    break

            if not tarefa_encontrada:
                print('⚠️ Tarefa não encontrada!')
                continue


            print(f'\nStatus atual: {tarefa_encontrada[3]}')


            status_opcoes = ['pendente', 'andamento', 'concluido']

            print('\nEscolha o novo status:')
            for i, opcao in enumerate(status_opcoes, start=1):
                print(f'{i} - {opcao}')

            while True:
                try:
                    escolha = int(input('Opção: '))
                    if 1 <= escolha <= len(status_opcoes):
                        novo_status = status_opcoes[escolha - 1]
                        break
                    else:
                        print('⚠️ Opção inválida!')
                except ValueError:
                    print('⚠️ Digite um número válido!')


            valido, msg = atualizar_status_tarefa(id_tarefa, novo_status)

            if not valido:
                print(f'⚠️ {msg}')
                continue

            print('✅ Status atualizado com sucesso!')
            sleep(2)

        except Exception:
            print('Erro ao atualizar status!')

        if pergunta_continuar('Deseja atualizar outro status? [S/N]: ') == 'n':
            break


def deletar_tarefas():
    while True:
        print(linha())
        print('DELETAR TAREFA'.center(40))
        print(linha())

        try:
            id_tarefa = int(input('Digite o ID da tarefa: '))


            resultado, dados = listar_tarefas()

            if not resultado:
                print(f'⚠️ {dados}')
                continue

            tarefa_encontrada = None
            for t in dados:
                if t[0] == id_tarefa:
                    tarefa_encontrada = t
                    break

            if not tarefa_encontrada:
                print('⚠️ Tarefa não encontrada!')
                continue


            print('\nTarefa encontrada:')
            print(f'ID: {tarefa_encontrada[0]}')
            print(f'Título: {tarefa_encontrada[1]}')
            print(f'Status: {tarefa_encontrada[3]}')
            print(f'Prioridade: {tarefa_encontrada[6]}')


            print('\n⚠️ ATENÇÃO: Essa ação não pode ser desfeita!')
            confirmacao = input('Deseja realmente deletar? [S/N]: ').strip().lower()

            if confirmacao not in ['s', 'sim']:
                print('Operação cancelada.')
                continue


            valido, msg = deletar_tarefa(id_tarefa)

            if not valido:
                print(f'⚠️ {msg}')
                continue

            print('✅ Tarefa deletada com sucesso!')
            sleep(2)

        except ValueError:
            print('⚠️ Digite um ID válido!')
        except Exception:
            print('Erro ao deletar tarefa!')

        if pergunta_continuar('Deseja deletar outra tarefa? [S/N]: ') == 'n':
            break