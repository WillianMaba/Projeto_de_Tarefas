import sqlite3

def criar_conexao():
    conexao = sqlite3.connect('banco_de_dados.db')
    return conexao