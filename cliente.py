import interfaceConsole
import socket
import ipaddress
from time import sleep
debug = True
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
t_con = 5 #segundos para aguardar a conexao
soc.settimeout(t_con)
porta = 8888

def conectar_server():
    while True:
        #coletar IP
        while True:
            try:
                ip = ipaddress.ip_address(input('Digite o endereço ip do servidor: '))
                break
            except ValueError:
                interfaceConsole.limpar_console()
                print('O ip inserido não é valido! Digite o ip no formato x.x.x.x')

        #conectar
        try:
            ip = str(ip)
            soc.connect((str(ip), porta))
            #sai do loop principal
            break
        except Exception as e:
            sleep(t_con)
            print(e)

def aguardar_resposta():
    #retorna true se a resposta do servidor for positiva
    for i in range(2):
        if debug:
            print('Aguadando resposta do servidor!')
        resposta = soc.recv(2).decode()
        if resposta:
            if resposta == 'NO':
                return False
            elif resposta == 'SI':
                return True

    print('Tempo limite excedido')
    return False

def painel():
    def logar():
        """
        retorna login_sucess quando usuario for autenticado!
                cadastro_sucess para cadastro realizado!
                login_fail|cadastro_fail caso falhar
        """
        interfaceConsole.limpar_console()
        op = interfaceConsole.mostrar_menu('SIMULADOR BANCARIO', '[ 1 ] LOGIN\n[ 2 ] CADASTRO\n[ 0 ] SAIR', 0, 2)
        #SAIR
        if op == 0:
            soc.close()
            exit()
        #LOGIN
        elif op == 1:
            if debug:
                email = 'teste@gmail.com'
                senha = 'seila'
            else:
                email = input('email: ').strip()
                senha = input('senha: ')
            requisicao = '5|' + email + '|' + senha
            soc.send(requisicao.encode())

            if aguardar_resposta():
                if debug:
                    print('Login Sucesso!')
                return 'login_sucess'
            else:
                if debug:
                    print('Login Fracasso')
                return 'login_fail'
        #CADASTRO
        elif op == 2:
            nome = input('nome: ')
            email = input('email: ')
            senha = input('senha: ')
            requisicao = '4|' + email + '|' + nome + '|' + senha
            soc.send(requisicao.encode())
            if aguardar_resposta():
                if debug:
                    print('Cadastro Sucesso!')
                return 'cadastro_sucess'
            else:
                if debug:
                    print('Cadastro Fracasso')
                return 'cadastro_fail'
    def depositar(valor):
        pass
    def sacar(valor):
        pass
    def transferir(valor, email_destino):
        pass
    def alterar_senha(senha_antiga, senha_nova):
        pass
    def verificar_transacoes():
        pass

    while True:
        resultado = logar()
        if resultado == 'login_sucess':
            #vai para a conta do usuario
            break
        elif resultado == 'cadastro_sucess':
            print('\nCADASTRO REALIZADO! (pressione ENTER)')
            input('')
        elif resultado == 'cadastro_fail':
            ##################### PRECISA MELHORAR O TRATAMENTO DE ERROS PARA MELHOR ANALISE  #########
            print('\nUma conta com esse email já existe! (pressione ENTER)')
            input('')
        elif resultado == 'login_fail':
            print('\nEmail ou senha incorretos! (pressione ENTER)')
            input('')




    ########################################################################################
    #############################      sessao pós login       ##############################



    while True:
        #recebendo dados da conta e adicionando ao dicionario
        soc.send(b'7')
        while True:
            ########  INICIO DE REQUISICAO DE DADOS    #####
            dados = soc.recv(10000).decode()
            acc = {}
            if dados:
                if debug:
                    print('DADOS RECEBIDOS!')
                    print(dados)
                dados = dados.split('|')
                acc['email'] = dados[0]
                acc['usuario'] = dados[1]
                acc['saldo'] = float(dados[2])
                # _ é o separador usado para distinguir transacoes diferentes
                acc['transacoes'] = [i for i in dados[3].split('_')]
                print(acc)
                break
            elif dados == 'NO':
            #########
                print('Não foi possível se conectar ao servidor!')
                input('Pressione enter para relogar')
                start()
                exit()

            ############### FIM LOOP DE ATUALIZACAO DOS DADOS ##############
        op = interfaceConsole.mostrar_menu(f'Logado como {acc["nome"]} SALDO: R$ {acc["saldo"]}',
                                      f'{acc["email"]}\n[ 1 ] DEPOSITAR\n[ 2 ] SACAR\n [ 3 ] TRANSFERIR\n[ 4 ] ALTERAR SENHA\n[ 0 ] SAIR', 0, 4)
        interfaceConsole.limpar_console()
        if op == 1:
            print('\t\tDEPOSITAR')
        elif op == 2:
            print('\t\tSACAR')
            pass
        elif op == 3:
            print('\t\tTRANSFERIR')
            pass
        elif op == 4:
            print('\t\tALTERAR SENHA')
            pass
        elif op == 0:
            soc.close()
            exit()










def start():
    if debug:
        soc.connect(('10.0.0.117', porta))
    else:
        conectar_server()
    painel()

start()