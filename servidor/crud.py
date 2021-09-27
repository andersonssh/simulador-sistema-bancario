from hashlib import sha256
import sqlite3
#criando controladores para o bd
con = sqlite3.connect('banco.db')
cur = con.cursor()
debug = False

def start_bd():
    #criar tabelas
    cur.execute('create table if not exists usuarios(email PRIMARY KEY, nome TEXT NOT NULL, senha TEXT NOT NULL, saldo DECIMAL(20,2));')
    cur.execute('create table if not exists transacoes(emailUsuario TEXT, transacao TEXT NOT NULL, FOREIGN KEY (emailUsuario) REFERENCES usuarios(email))')

    #adicionando usuarios
    try:
        cur.execute('INSERT INTO usuarios (email, nome, senha, saldo) VALUES ("user1@gmail.com", "user bot 1", "hashdasenha", 0)')
        cur.execute('INSERT INTO usuarios (email, nome, senha, saldo) VALUES ("user2@gmail.com", "user bot 2", "hashdasenha", 0)')
        cur.execute('INSERT INTO usuarios (email, nome, senha, saldo) VALUES ("user3@gmail.com", "user bot 3", "hashdasenha", 0)')
    except sqlite3.IntegrityError:
        # if debug:
        #     print('Criacao de Usuarios falhou, pois eles já existem!')
        pass

    con.commit()
    return None

def cadastrar(email, nome, senha, saldo=0):
    senha = sha256(senha.encode('utf-8')).hexdigest()
    try:
        cur.execute('INSERT INTO usuarios (email, nome, senha, saldo) '
                    f'VALUES ("{email}", "{nome}", "{senha}", {saldo})')
        con.commit()
    except Exception as e:
        if debug:
            print('Erro em cadastro: ', end='')
            print(e)
        return False
    return True

def login(email, senha):
    #return True para sucesso no login e false caso contrario
    if debug:
        for i in cur.execute(f'SELECT * FROM usuarios WHERE email="{email}" and senha="{senha}"'):
            print(i)

    if tuple(cur.execute(f'SELECT * FROM usuarios WHERE email="{email}" and senha="{senha}"')):
        return True
    else:
        return False

def alterar_senha(email, senha_antiga, senha_nova):
    if debug:
        print('Senha antiga: ',senha_antiga)
        print('Senha nova: ', senha_nova)

    #se email True entao atualiza a senha
    if login(email, senha_antiga):
        cur.execute(f'UPDATE usuarios SET senha="{senha_nova}" WHERE email="{email}"')
        con.commit()
        if debug:
            print('Senha Alterada com sucesso!')
        return True
    else:
        if debug:
            print('A senha nao foi alterada!')
        return False

def sacar(email, senha, valor):
    if login(email, senha):
        valor_atual = tuple(cur.execute(f'SELECT saldo FROM usuarios WHERE email="{email}"'))[0][0]
        if valor_atual < valor or valor <= 0:
            if debug:
                print('Valor inserido nao pode ser sacado!')
            return False
        else:
            cur.execute(f'UPDATE usuarios  SET saldo={valor_atual - valor} where email="{email}"')
            con.commit()
            _transacao_efetuada(email, f'Saque de R$ {valor}')
            return True
    else:
        if debug:
            print('Login invalido')
        return False

def depositar(email, senha, valor):
    if login(email, senha):
        valor_atual = tuple(cur.execute(f'SELECT saldo FROM usuarios WHERE email="{email}"'))[0][0]
        if valor <= 0:
            if debug:
                print('Valor inserido nao pode ser depositado')
            return False
        else:
            if debug:
                print(f'Depositado R$ {valor}')
            cur.execute(f'UPDATE usuarios  SET saldo={valor_atual + valor} where email="{email}"')
            con.commit()
            _transacao_efetuada(email, f'Depósito de R$ {valor}')
            return True
    else:
        if debug:
            print('Login invalido')
        return False

def transferir(email, senha, valor, email_destino):
    if login(email, senha):
        valor_atual = tuple(cur.execute(f'SELECT saldo FROM usuarios WHERE email="{email}"'))[0][0]
        if valor_atual < valor or valor <= 0:
            if debug:
                print('Valor inserido nao pode ser transferido!')
            return False
        else:
            #depositando para o destino
            valor_atual_destino = tuple(cur.execute(f'SELECT saldo FROM usuarios WHERE email="{email_destino}"'))[0][0]
            cur.execute(f'UPDATE usuarios  SET saldo={valor_atual_destino + valor} where email="{email_destino}"')
            #sacando do usuario atual
            cur.execute(f'UPDATE usuarios  SET saldo={valor_atual - valor} where email="{email}"')
            con.commit()
            if debug:
                print('Valor transferido!')
            #registrando email do usuario
            _transacao_efetuada(email, f'Transferencia de R$ {valor} realizada para {email_destino}')
            _transacao_efetuada(email_destino, f'Transferencia de R$ {valor} recebida de {email}')
            return True
    else:
        if debug:
            print('Login invalido')

def _transacao_efetuada(email, ocorrencia):
    #adiciona a tabela transacoes um registro com a ocorrencia da transacao
    try:
        cur.execute(f'INSERT INTO transacoes (emailUsuario, transacao) VALUES ("{email}", "{ocorrencia}")')
        con.commit()
        return True
    except Exception as e:
        if debug:
            print('Falha no registro de transacao efetuada: ', e)
        return False

def get_conta(email, senha):
    #retorna dicionario com a dados de conta -> email:str, nome:str, saldo:float, transacoes:lista
    if login(email, senha):
        #pegando dados da conta
        dados = tuple(cur.execute(f'SELECT * FROM usuarios WHERE email="{email}"'))[0]
        acc = {}
        acc['email'] = dados[0]
        acc['nome'] = dados[1]
        acc['saldo'] = dados[3]

        if debug:
            print(f'email: {acc["email"]}\nnome: {acc["nome"]}\nSaldo: R$ {acc["saldo"]}')

        #pegando transacoes
        transacoes = cur.execute(f'SELECT transacao FROM transacoes WHERE emailUsuario="{email}"')
        acc['transacoes'] = [transacao[0] for transacao in transacoes]

        if debug:
            print('TRANSAÇÕES:')
            for i in acc['transacoes']:
                print('\t', i)

        return acc
    else:
        if debug:
            print('Login nao realizado!')
        return None


if __name__ == '__main__':
    start_bd()
    #cadastrar('seila@gmail.com', 'josezin souza', 'hojesei')
    #alterar_senha('seila@gmail.com', 'hojesei', 'hojenaosei')
    #alterar_senha('seila@gmail.com', 'hojenaosei', 'hojesei')
    #print("LOGANDO! ", login('seila@gmail.com', 'hojesei'))
    #depositar('seila@gmail.com', 'hojesei', 100000)
    #transferir('seila@gmail.com', 'hojesei', 200, 'user1@gmail.com')
    #print(get_conta('seila@gmail.com', 'hojesei'))
