import sqlite3
import pandas as pd

class ContaPessoal:
    def __init__(self, nome, sobrenome):
        self.nome = nome
        self.sobrenome = sobrenome
        self.receita = []
        self.despesas = []

    def renda_total(self):
        return sum(transacao[1] for transacao in self.receita)

    def despesa_total(self):
        return sum(transacao[1] for transacao in self.despesas)

    def informacao_conta(self):
        return f"Nome: {self.nome} {self.sobrenome}\nRenda Total: {self.renda_total()}\nDespesa Total: {self.despesa_total()}\nSaldo: {self.saldo_conta()}"

    def adicionar_renda(self, descricao, valor):
        self.receita.append((descricao, valor))

    def adicionar_despesa(self, descricao, valor):
        self.despesas.append((descricao, valor))

    def saldo_conta(self):
        return self.renda_total() - self.despesa_total()

# Conexão com o banco de dados local
conn = sqlite3.connect("conta_pessoal.db")
cursor = conn.cursor()

# Tabela de cadastro de pessoa
cursor.execute('''CREATE TABLE IF NOT EXISTS cadastro (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    sobrenome TEXT NOT NULL
                )''')

# Tabela de transações
cursor.execute('''CREATE TABLE IF NOT EXISTS transacoes (
                    id INTEGER PRIMARY KEY,
                    pessoa_id INTEGER NOT NULL,
                    descricao TEXT NOT NULL,
                    valor REAL NOT NULL,
                    FOREIGN KEY (pessoa_id) REFERENCES cadastro (id)
                )''')

# Tabela de tipo de transações
cursor.execute('''CREATE TABLE IF NOT EXISTS tipo_transacoes (
                    id INTEGER PRIMARY KEY,
                    descricao TEXT NOT NULL
                )''')

# Exemplo de inserção de dados
cursor.execute("INSERT INTO cadastro (nome, sobrenome) VALUES (?, ?)", ("João", "Silva"))
conn.commit()

cursor.execute("INSERT INTO tipo_transacoes (descricao) VALUES (?)", ("Salário",))
cursor.execute("INSERT INTO tipo_transacoes (descricao) VALUES (?)", ("Bolsa",))
cursor.execute("INSERT INTO tipo_transacoes (descricao) VALUES (?)", ("Gorjeta",))
conn.commit()

cursor.execute("INSERT INTO transacoes (pessoa_id, descricao, valor) VALUES (?, ?, ?)",
               (1, "Salário", 3000.0))
cursor.execute("INSERT INTO transacoes (pessoa_id, descricao, valor) VALUES (?, ?, ?)",
               (1, "Bolsa", 500.0))
cursor.execute("INSERT INTO transacoes (pessoa_id, descricao, valor) VALUES (?, ?, ?)",
               (1, "Gorjeta", 200.0))
conn.commit()

# Exemplo de uso da classe ContaPessoal
conta_joao = ContaPessoal("João", "Silva")

cursor.execute("SELECT descricao, valor FROM transacoes WHERE pessoa_id = 1")
transacoes = cursor.fetchall()

for transacao in transacoes:
    descricao, valor = transacao
    if valor > 0:
        conta_joao.adicionar_renda(descricao, valor)
    else:
        conta_joao.adicionar_despesa(descricao, valor)

#print(conta_joao.informacao_conta())

print(pd.read_sql("SELECT * FROM transacoes WHERE pessoa_id = 1",con=conn))

conn.close()
