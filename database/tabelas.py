from database.conexao import criar_conexao


def criar_tarefa():
    con = criar_conexao()
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS tarefa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                status TEXT NOT NULL CHECK(
                    status IN ('pendente','andamento','concluido')
                ),
                data_criacao TEXT NOT NULL,
                data_conclusao TEXT,
                prioridade TEXT NOT NULL CHECK(
                    prioridade IN ('baixa','medio','alta','urgente')
                )
                )
    ''')

    con.commit()
    con.close()