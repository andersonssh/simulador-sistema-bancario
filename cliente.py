import interfaceConsole
import socket
import ipaddress
from time import sleep
debug = False
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
        req = '1|' + str(valor)
        soc.send(req.encode())
        return aguardar_resposta()


    def sacar(valor):
        req = '2|' + str(valor)
        soc.send(req.encode())
        return aguardar_resposta()


    def transferir(valor, email_destino):
        req = '3|' + str(valor) + '|' + email_destino
        print(req)
        soc.send(req.encode())
        return aguardar_resposta()


    def alterar_senha(senha_antiga, senha_nova):
        req = '6|' + senha_antiga + '|' + senha_nova
        soc.send(req.encode())
        return aguardar_resposta()


    def mostrar_transacoes():
        for i in acc['transacoes']:
            print(i)

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
                acc['nome'] = dados[1]
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
        op = interfaceConsole.mostrar_menu(f'Logado como {acc["nome"].split(" ")[0]} SALDO: R$ {acc["saldo"]}',
                                      f'email:{acc["email"]}\n\n[ 1 ] DEPOSITAR\n[ 2 ] SACAR\n[ 3 ] TRANSFERIR\n[ 4 ] ALTERAR SENHA\n[ 5 ] VER HISTÓRICO DE TRANSAÇÕES\n[ 0 ] SAIR', 0, 5)
        interfaceConsole.limpar_console()
        if op == 1:
            print('\t\tDEPOSITAR')
            try:
                valor = float(input('\n\nDigite o valor (ex: 120.50): '))
            except ValueError:
                print('Valor Inválido! (pressione ENTER)')
                input('')
            else:
                if valor <= 0:
                    print('Você não pode depositar este valor! (pressione ENTER)')
                    input('')
                else:
                    if depositar(valor):
                        print('DEPOSITO REALIZADO! (pressione ENTER)')
                        input('')
                    else:
                        print('FALHA NO DEPOSITO! (pressione ENTER)')
                        input('')

        elif op == 2:
            try:
                valor = float(input('\n\nDigite o valor (ex: 120.50): '))
            except ValueError:
                print('Valor Inválido! (pressione ENTER)')
                input('')
            else:
                if valor > acc['saldo']:
                    print('Você não tem saldo suficiente para sacar essa quantia (pressione ENTER)')
                    input('')
                elif valor <= 0:
                    print('Você não pode sacar este valor! (pressione ENTER)')
                    print(input(''))
                else:
                    if sacar(valor):
                        print('SAQUE REALIZADO! (pressione ENTER)')
                        input('')
                    else:
                        print('FALHA NO SAQUE! (pressione ENTER)')
                        input('')
        elif op == 3:
            print('\t\tTRANSFERIR')
            try:
                valor = float(input('\n\nDigite o valor (ex: 120.50): '))
            except ValueError:
                print('Valor Inválido! (pressione ENTER)')
                input('')
            else:
                if valor > acc['saldo']:
                    print('Você não tem saldo suficiente para transferir essa quantia (pressione ENTER)')
                    input('')
                elif valor <= 0:
                    print('Você não pode transferir este valor! (pressione ENTER)')
                    print(input(''))
                else:
                    email_destinatario = input('Digite o email do destinatário: ')
                    if transferir(valor, email_destinatario):
                        print('TRANSFERENCIA REALIZADA! (pressione ENTER)')
                        input('')
                    else:
                        print('FALHA NA TRANSFERENCIA! O VERIFIQUE O EMAIL INFORMADO! (pressione ENTER)')
                        input('')
        elif op == 4:
            print('\t\tALTERAR SENHA')
            senha_antiga = input('\n\nDigite a senha atual: ')
            senha_nova = input('Digite a nova senha: ')
            if alterar_senha(senha_antiga, senha_nova):
                print('Senha alterada com sucesso! (pressione ENTER)')
                input('')
                painel()
                exit()
            else:
                print('A senha não foi alterada! (pressione ENTER)')
                input('')
        elif op == 5:
            print('\t\tTRANSAÇÕES')
            print('\n')
            mostrar_transacoes()
            print('')
            input('pressione ENTER')
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