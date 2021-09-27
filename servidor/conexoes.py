import socket
from threading import Thread
from hashlib import sha256
from . import crud

def start():
    crud.start_bd()
    debug = False
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('1.1.1.1', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = 'O endereço de ip não pôde ser definido! Descubra o endereço ip local manualmente: ifconfig para Linux e ipconfig para Windows'
        finally:
            s.close()
        return IP

    ip_ = get_ip()
    porta = 8888
    print(f'IP: {ip_}\nPORTA: {porta}')

    #adicionando host para toda a rede
    soc.bind(('0.0.0.0', porta))

    #formato {IP: {con: objCon, email: str, senha: str-hash}}

    sessoes_ativas = {}

    def gerenciar_conexoes():
        while True:
            soc.listen()
            con, addr = soc.accept()
            con.settimeout(0.2)
            sessoes_ativas[addr[0]] = {'con': con , 'email': '', 'senha': ''}
            if debug:
                print(f'Conexao com {addr[0]} estabelecida!')
                print('Mostrando sessoes ativas')
                print(sessoes_ativas)

    def requisicao(dados, ip):
        """
            TABELA DE REQUISICOES
            1|valor - DEPOSITAR - email|senha|valor via dict acc
            2|valor - SACAR - email|senha|valor via dict acc
            3|valor|email - TRANSFERIR - email|senha|valor|email via dict acc
            4|email|nome|senha - CADASTRAR
            5|email|senha - LOGIN
            6|senha_antiga|senha_nova - MUDAR SENHA email|senha_antiga|senha_nova via dict acc
            7 retorna conta atual

        """
        #respostas do servidor para o cliente
        POSITIVO = 'SI'.encode()
        NEGATIVO = 'NO'.encode()



        dados = dados.split('|')
        if debug:
            print('Mostrando dados!')
            print(dados)

        #depositar
        if dados[0] == '1':
            valor = float(dados[1])
            if crud.depositar(sessoes_ativas[ip]['email'], sessoes_ativas[ip]['senha'], valor):
                if debug:
                    print('DEPOSITO EFETUADO COM SUCESSO!')
                sessoes_ativas[ip]['con'].send(POSITIVO)
            else:
                if debug:
                    print('FRACASSO NO DEPOSITO!')
                sessoes_ativas[ip]['con'].send(NEGATIVO)
        #sacar
        elif dados[0] == '2':
            valor = float(dados[1])
            if crud.sacar(sessoes_ativas[ip]['email'], sessoes_ativas[ip]['senha'], valor):
                if debug:
                    print('SAQUE EFETUADO COM SUCESSO!')
                sessoes_ativas[ip]['con'].send(POSITIVO)
            else:
                if debug:
                    print('FRACASSO NO SAQUE!')
                sessoes_ativas[ip]['con'].send(NEGATIVO)
        #transferir
        elif dados[0] == '3':
            print('CONEXOES TRANSFERIR!!!')
            print(dados)
            valor = float(dados[1])
            email_dest = dados[2]
            if crud.transferir(sessoes_ativas[ip]['email'], sessoes_ativas[ip]['senha'],valor, email_dest):
                if debug:
                    print('TRANSFERENCIA EFETUADA COM SUCESSO!')
                sessoes_ativas[ip]['con'].send(POSITIVO)
            else:
                if debug:
                    print('FRACASSO NA TRANSFERENCIA!')
                sessoes_ativas[ip]['con'].send(NEGATIVO)
        #cadastro
        elif dados[0] == '4':
            email = dados[1]
            nome = dados[2]
            senha = dados[3]
            if crud.cadastrar(email, nome, senha):
                if debug:
                    print('CADASTRO REALIZADO COM SUCESSO!')
                sessoes_ativas[ip]['con'].send(POSITIVO)
            else:
                if debug:
                    print('FRACASSO NO CADASTRO!')
                sessoes_ativas[ip]['con'].send(NEGATIVO)
        #login
        elif dados[0] == '5':
            email = dados[1]
            #gera o hash da senha para comparacao no bd
            senha = sha256(dados[2].encode()).hexdigest()
            if crud.login(email, senha):
                #registra os dados na sessao!
                sessoes_ativas[ip]['email'] = email
                sessoes_ativas[ip]['senha'] = senha
                if debug:
                    print('LOGIN REALIZADO COM SUCESSO!')
                sessoes_ativas[ip]['con'].send(POSITIVO)
            else:
                if debug:
                    print('FRACASSO NO LOGIN!')
                sessoes_ativas[ip]['con'].send(NEGATIVO)
        elif dados[0] == '6':
            senha_antiga = sha256(dados[1].encode()).hexdigest()
            senha_nova = sha256(dados[2].encode()).hexdigest()
            if crud.alterar_senha(sessoes_ativas[ip]['email'], senha_antiga, senha_nova):
                if debug:
                    print('SENHA ALTERADA COM SUCESSO!')
                sessoes_ativas[ip]['con'].send(POSITIVO)
            else:
                if debug:
                    print('FALHA AO ALTERAR A SENHA!')
                sessoes_ativas[ip]['con'].send(NEGATIVO)
        elif dados[0] == '7':
            conta = crud.get_conta(sessoes_ativas[ip]['email'], sessoes_ativas[ip]['senha'])
            if conta:
                gtc = conta['email'] + '|' + conta['nome'] + '|' + str(conta['saldo']) + '|' + '_'.join([i for i in conta['transacoes']])
                if debug:
                    print(gtc)
                sessoes_ativas[ip]['con'].send(gtc.encode('utf-8'))
            else:
                sessoes_ativas[ip]['con'].send(NEGATIVO)
        else:
            if debug:
                print('o primeiro elemento da requisicao nao existe!')
            sessoes_ativas[ip]['con'].send(NEGATIVO)


    Thread(target=gerenciar_conexoes).start()
    if debug:
        print('Entrada de loop aguardando requisicoes')

    #fica em loop aguardando requisicoes
    while True:
        #varre todas as conexoes a procura de requisicoes
        chaves_sessoes_tivas = list(sessoes_ativas.keys())
        for ip in chaves_sessoes_tivas:
            obj_conexao = sessoes_ativas[ip]['con']
            try:
                try:
                    req = obj_conexao.recv(1024).decode()
                except socket.timeout:
                    continue
            except ConnectionResetError:
                del sessoes_ativas[ip]
                continue

            if req:
                if debug:
                    print('requisicao recebida, iniciando gerenciador de requisicoes!')
                try:
                    requisicao(req, ip)
                except Exception as e:
                    if debug:
                        print(e)
                        print('Cliente tentou violar regras')
                    sessoes_ativas[ip]['con'].send(b'NO')


if __name__ == '__main__':
    start()
